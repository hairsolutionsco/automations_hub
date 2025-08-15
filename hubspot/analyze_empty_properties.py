#!/usr/bin/env python3
"""
Analyze HubSpot CRM objects to identify empty or mostly empty properties and
update each object's markdown documentation with a new section mirroring the
Notion analyzer output style.

Behavior:
- Discovers objects (schemas + core fallback)
- Fetches property definitions per object
- Samples up to MAX_RECORDS records per object using the Search API
- Determines per-property usage (empty vs filled)
- Classifies properties as completely empty (100%) or mostly empty (>= THRESHOLD)
- Updates hubspot/objects/<object>/properties.md with a new section

Auth:
- Uses HUBSPOT_ACCESS_TOKEN (or HUBSPOT_API_ACCESS_TOKEN) from env
"""

import asyncio
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

try:
    import httpx  # type: ignore
except Exception as e:
    print("Error: httpx is required. Install with: pip install httpx")
    raise

sys.path.append('.')

HUBSPOT_BASE_URL = 'https://api.hubapi.com'
MAX_RECORDS = int(os.getenv('HUBSPOT_ANALYZE_MAX_RECORDS', '500'))  # per object
PAGE_LIMIT = int(os.getenv('HUBSPOT_ANALYZE_PAGE_LIMIT', '100'))
MOSTLY_EMPTY_THRESHOLD = float(os.getenv('HUBSPOT_MOSTLY_EMPTY_THRESHOLD', '0.95'))


def get_access_token() -> Optional[str]:
    return os.getenv('HUBSPOT_ACCESS_TOKEN') or os.getenv('HUBSPOT_API_ACCESS_TOKEN')


async def hubspot_get(client: httpx.AsyncClient, path: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    token = get_access_token()
    if not token:
        print("❌ HUBSPOT_ACCESS_TOKEN not set. Please export HUBSPOT_ACCESS_TOKEN and retry.")
        return None
    url = f"{HUBSPOT_BASE_URL}{path}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    try:
        resp = await client.get(url, headers=headers, params=params, timeout=30.0)
    except Exception as e:
        print(f"   ❌ Request failed {path}: {e}")
        return None
    if resp.status_code == 200:
        try:
            return resp.json()
        except Exception:
            print(f"   ❌ Failed to parse JSON for {path}")
            return None
    else:
        text = resp.text
        if len(text) > 500:
            text = text[:500] + '...'
        print(f"   ❌ Error {resp.status_code} for {path}: {text}")
        return None


async def hubspot_post(client: httpx.AsyncClient, path: str, json_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    token = get_access_token()
    if not token:
        print("❌ HUBSPOT_ACCESS_TOKEN not set. Please export HUBSPOT_ACCESS_TOKEN and retry.")
        return None
    url = f"{HUBSPOT_BASE_URL}{path}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    try:
        resp = await client.post(url, headers=headers, json=json_body, timeout=30.0)
    except Exception as e:
        print(f"   ❌ Request failed {path}: {e}")
        return None
    if resp.status_code in (200, 207):  # 207 for some batch responses
        try:
            return resp.json()
        except Exception:
            print(f"   ❌ Failed to parse JSON for {path}")
            return None
    else:
        text = resp.text
        if len(text) > 500:
            text = text[:500] + '...'
        print(f"   ❌ Error {resp.status_code} for {path}: {text}")
        return None


async def get_all_schemas(client: httpx.AsyncClient) -> List[Dict[str, Any]]:
    data = await hubspot_get(client, "/crm/v3/schemas", params={"archived": "false"})
    if not data:
        return []
    return data.get('results') or []


async def get_properties_for_object(client: httpx.AsyncClient, schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return property definitions for an object using the best identifier."""
    candidates = [
        (schema.get('fullyQualifiedName') or '').strip(),
        (schema.get('objectTypeId') or '').strip(),
        (schema.get('name') or '').strip(),
    ]
    for ident in candidates:
        if not ident:
            continue
        data = await hubspot_get(client, f"/crm/v3/properties/{ident}")
        if data and data.get('results') is not None:
            return data.get('results') or []
    return []


def chunk_list(items: List[str], size: int) -> List[List[str]]:
    return [items[i:i+size] for i in range(0, len(items), size)]


async def search_objects(client: httpx.AsyncClient, object_name: str, properties: List[str], after: Optional[str] = None, limit: int = PAGE_LIMIT) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """Use CRM Search API to fetch a page of objects with specified properties."""
    body: Dict[str, Any] = {
        "limit": limit,
        "properties": properties,
    }
    if after:
        body["after"] = after
    data = await hubspot_post(client, f"/crm/v3/objects/{object_name}/search", body)
    if not data:
        return [], None
    results = data.get('results') or []
    after_next = None
    paging = data.get('paging') or {}
    next_info = paging.get('next') or {}
    if next_info:
        after_next = next_info.get('after')
    return results, after_next


def is_value_empty_hubspot(value: Optional[str], ptype: str, field_type: Optional[str]) -> bool:
    """Determine if a HubSpot property value (string-typed in API) is empty.

    - Empty if None or empty string
    - For boolean: only 'true' counts as filled; anything else considered empty (parity with Notion checkbox)
    - For numbers/dates/datetime/enumeration: non-empty string counts as filled (including '0')
    """
    if value is None:
        return True
    s = str(value).strip()
    if s == "":
        return True
    if ptype == 'bool' or (field_type == 'booleancheckbox'):
        return s.lower() != 'true'
    # For all other types, presence of a non-empty string is considered filled
    return False


def analyze_usage(records: List[Dict[str, Any]], properties: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
    """Compute usage counters per property across the provided records."""
    usage: Dict[str, Dict[str, int]] = {}
    # Initialize
    prop_meta: Dict[str, Tuple[str, Optional[str]]] = {}
    for p in properties:
        name = p.get('name') or ''
        if not name:
            continue
        prop_meta[name] = (p.get('type', 'unknown'), p.get('fieldType'))
        usage[name] = {"total": 0, "empty": 0, "filled": 0}

    for rec in records:
        rec_props = rec.get('properties') or {}
        for name, meta in prop_meta.items():
            ptype, field_type = meta
            usage[name]["total"] += 1
            val = rec_props.get(name)
            if is_value_empty_hubspot(val, ptype, field_type):
                usage[name]["empty"] += 1
            else:
                usage[name]["filled"] += 1

    return usage


def identify_empty_properties(usage: Dict[str, Dict[str, int]], threshold: float = MOSTLY_EMPTY_THRESHOLD):
    empty_props = []
    mostly_empty_props = []
    for name, counters in usage.items():
        total = counters.get('total', 0)
        empty = counters.get('empty', 0)
        filled = counters.get('filled', 0)
        if total == 0:
            continue
        empty_pct = empty / total
        if empty_pct == 1.0:
            empty_props.append({
                'name': name,
                'empty_percentage': empty_pct,
                'total': total,
            })
        elif empty_pct >= threshold:
            mostly_empty_props.append({
                'name': name,
                'empty_percentage': empty_pct,
                'total': total,
                'filled_count': filled,
            })
    return empty_props, mostly_empty_props


def safe_object_dir_name(name: str) -> str:
    return name.strip().lower().replace(' ', '_').replace('&', 'and').replace('/', '_').replace(':', '')


def update_markdown_file(obj_name: str, empty_props: List[Dict[str, Any]], mostly_empty_props: List[Dict[str, Any]], analyzed_count: int) -> bool:
    base_dir = "/workspaces/automations_hub/hubspot/objects"
    obj_dir = os.path.join(base_dir, safe_object_dir_name(obj_name))
    md_path = os.path.join(obj_dir, "properties.md")
    if not os.path.exists(md_path):
        print(f"   ⚠️ Markdown not found for {obj_name}: {md_path}")
        return False
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Build section
        section_lines: List[str] = []
        if empty_props or mostly_empty_props:
            section_lines.append("## 🚫 Empty & Unused Properties")
            section_lines.append("")
            section_lines.append(f"*Analysis based on approximately {analyzed_count} records*")
            section_lines.append("")
            if empty_props:
                section_lines.append(f"### Completely Empty Properties ({len(empty_props)})")
                section_lines.append("*These properties have no data in any analyzed record:*")
                section_lines.append("")
                for prop in sorted(empty_props, key=lambda x: x['name']):
                    section_lines.append(f"- `{prop['name']}`")
                section_lines.append("")
            if mostly_empty_props:
                section_lines.append(f"### Mostly Empty Properties ({len(mostly_empty_props)})")
                section_lines.append("*These properties have data in less than 5% of analyzed records:*")
                section_lines.append("")
                for prop in sorted(mostly_empty_props, key=lambda x: x['empty_percentage'], reverse=True):
                    section_lines.append(f"- `{prop['name']}` - {prop['empty_percentage']*100:.1f}% empty, only {prop['filled_count']} records with data")
                section_lines.append("")
        else:
            section_lines.append("## ✅ Property Usage Analysis")
            section_lines.append("")
            section_lines.append(f"*Analysis based on approximately {analyzed_count} records*")
            section_lines.append("")
            section_lines.append("**Great news!** All properties analyzed have data.")
            section_lines.append("")

        section = "\n".join(section_lines) + "\n"

        # Insert before the final generated-on footer
        footer_marker = "*Documentation generated on"
        insert_at = content.find(footer_marker)
        if insert_at == -1:
            # Fallback: append to end
            new_content = content
            if not new_content.endswith("\n\n"):
                new_content += "\n"
            new_content += section
        else:
            # Try to insert right before the preceding line '---\n'
            dash_idx = content.rfind("---\n", 0, insert_at)
            if dash_idx != -1:
                new_content = content[:dash_idx] + section + content[dash_idx:]
            else:
                new_content = content[:insert_at] + section + content[insert_at:]

        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    except Exception as e:
        print(f"   ❌ Error updating {md_path}: {e}")
        return False


async def analyze_object(client: httpx.AsyncClient, schema: Dict[str, Any]) -> Tuple[Optional[List[Dict[str, Any]]], Optional[List[Dict[str, Any]]], int]:
    obj_name = (schema.get('name') or '').strip()
    labels = schema.get('labels') or {}
    display_plural = labels.get('plural') or obj_name
    if not obj_name:
        return None, None, 0
    print(f"🔍 Analyzing: {display_plural} ({obj_name})")

    props = await get_properties_for_object(client, schema)
    if not props:
        print("   ❌ Could not fetch properties; skipping")
        return None, None, 0

    prop_names = [p.get('name') for p in props if p.get('name')]
    if not prop_names:
        return None, None, 0

    # Chunk properties to keep request bodies reasonable
    chunks = chunk_list(prop_names, 100)

    # We'll accumulate usage across a sampled set of records per chunk
    total_records_seen = 0
    combined_usage: Dict[str, Dict[str, int]] = {p.get('name'): {"total": 0, "empty": 0, "filled": 0} for p in props if p.get('name')}

    try:
        for idx, chunk in enumerate(chunks):
            after = None
            records_accum: List[Dict[str, Any]] = []
            while len(records_accum) < MAX_RECORDS:
                page, after = await search_objects(client, obj_name, chunk, after=after, limit=PAGE_LIMIT)
                if not page:
                    break
                records_accum.extend(page)
                if not after:
                    break
                await asyncio.sleep(0.15)

            # Cap to MAX_RECORDS
            if len(records_accum) > MAX_RECORDS:
                records_accum = records_accum[:MAX_RECORDS]

            if idx == 0:
                total_records_seen = len(records_accum)

            if records_accum:
                # Build minimal prop meta for this chunk
                chunk_props_meta = [p for p in props if p.get('name') in chunk]
                usage = analyze_usage(records_accum, chunk_props_meta)
                # Merge usage into combined_usage
                for name, counters in usage.items():
                    for k in ("total", "empty", "filled"):
                        combined_usage[name][k] += counters[k]

            # Pace between chunks
            await asyncio.sleep(0.2)

        # Classify
        empty_props, mostly_empty_props = identify_empty_properties(combined_usage, threshold=MOSTLY_EMPTY_THRESHOLD)
        print(f"   ❌ Completely empty: {len(empty_props)}")
        print(f"   ⚠️ Mostly empty (≥ {int(MOSTLY_EMPTY_THRESHOLD*100)}%): {len(mostly_empty_props)}")
        return empty_props, mostly_empty_props, total_records_seen
    except Exception as e:
        print(f"   ❌ Error analyzing {obj_name}: {e}")
        return None, None, 0


async def main() -> None:
    print("🚀 Starting empty properties analysis across HubSpot objects...")

    token = get_access_token()
    if not token:
        print("❌ HUBSPOT_ACCESS_TOKEN not set. Export it and re-run.")
        return

    success = 0
    errors = 0
    total_empty = 0
    total_mostly_empty = 0

    async with httpx.AsyncClient() as client:
        schemas = await get_all_schemas(client)
        # Always include core objects
        core = ["contacts", "companies", "deals", "tickets"]
        existing_names = {str((s.get('name') or '')).strip().lower() for s in schemas}
        for name in core:
            if name not in existing_names:
                schemas.append({"name": name, "labels": {"singular": name[:-1] if name.endswith('s') else name, "plural": name}})

        # De-dupe by name
        seen = set()
        deduped = []
        for s in schemas:
            n = (s.get('name') or '').strip().lower()
            if not n or n in seen:
                continue
            seen.add(n)
            deduped.append(s)

        print(f"📊 Analyzing {len(deduped)} objects for unused properties")
        print("")

        for schema in deduped:
            empty_props, mostly_empty_props, analyzed_count = await analyze_object(client, schema)
            obj_name = (schema.get('name') or '').strip()
            if empty_props is None or mostly_empty_props is None:
                errors += 1
                print("")
                continue

            if update_markdown_file(obj_name, empty_props, mostly_empty_props, analyzed_count):
                print("   ✅ Updated documentation file")
                success += 1
                total_empty += len(empty_props)
                total_mostly_empty += len(mostly_empty_props)
            else:
                print("   ❌ Failed to update documentation file")
                errors += 1
            print("")
            await asyncio.sleep(0.4)

    print("📊 Analysis Complete!")
    print(f"   ✅ Successfully analyzed: {success} objects")
    print(f"   ❌ Errors: {errors} objects")
    print(f"   🚫 Total completely empty properties found: {total_empty}")
    print(f"   ⚠️ Total mostly empty properties found: {total_mostly_empty}")
    print("")
    print("🎉 All object documentation files have been updated with empty property analysis!")
    print("📖 Check each object's properties.md for the new '🚫 Empty & Unused Properties' section.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted.")
