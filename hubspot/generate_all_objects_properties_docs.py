#!/usr/bin/env python3
"""
Generate comprehensive documentation for all HubSpot CRM objects' properties.
This script discovers all standard and custom objects, fetches their properties,
and writes individual markdown files per object with vertical, human-friendly formatting.

Output location:
- hubspot/objects/<object_name>/properties.md

Auth:
- Uses HUBSPOT_ACCESS_TOKEN from environment. If not set, exits with a helpful message.
"""

import asyncio
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional

try:
    import httpx  # type: ignore
except Exception as e:  # pragma: no cover
    print("Error: httpx is required. Install with: pip install httpx")
    raise


# Add repo root to path for consistency with other scripts
sys.path.append('.')


HUBSPOT_BASE_URL = 'https://api.hubapi.com'


def get_access_token() -> Optional[str]:
    """Get HubSpot Private App access token from env."""
    token = os.getenv('HUBSPOT_ACCESS_TOKEN') or os.getenv('HUBSPOT_API_ACCESS_TOKEN')
    return token


async def hubspot_get(client: httpx.AsyncClient, path: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """Perform an authenticated GET request to HubSpot API and return JSON or None on error."""
    token = get_access_token()
    if not token:
        print("❌ HUBSPOT_ACCESS_TOKEN not set. Please export HUBSPOT_ACCESS_TOKEN and retry.")
        return None

    url = f"{HUBSPOT_BASE_URL}{path}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    try:
        resp = await client.get(url, headers=headers, params=params, timeout=30.0)
    except Exception as e:  # network errors
        print(f"   ❌ Request failed {path}: {e}")
        return None

    if resp.status_code == 200:
        try:
            return resp.json()
        except Exception:
            print(f"   ❌ Failed to parse JSON for {path}")
            return None
    else:
        # Trim long error bodies
        text = resp.text
        if len(text) > 500:
            text = text[:500] + '...'
        print(f"   ❌ Error {resp.status_code} for {path}: {text}")
        return None


async def get_all_schemas(client: httpx.AsyncClient) -> List[Dict[str, Any]]:
    """Fetch all CRM object schemas (standard + custom)."""
    data = await hubspot_get(client, "/crm/v3/schemas", params={"archived": "false"})
    if not data:
        return []
    results = data.get('results') or []
    return results


async def get_properties_for_object(client: httpx.AsyncClient, object_identifier: str) -> List[Dict[str, Any]]:
    """Fetch property definitions for a given object identifier.

    The identifier may be a simple name for standard objects (contacts, companies, deals, tickets),
    or a fullyQualifiedName/objectTypeId for custom objects (e.g., "2-1234567" or "p12345_customobject").
    """
    data = await hubspot_get(client, f"/crm/v3/properties/{object_identifier}")
    if not data:
        return []
    results = data.get('results') or []
    return results


def safe_object_dir_name(name: str) -> str:
    return (
        name.strip().lower().replace(' ', '_').replace('&', 'and').replace('/', '_').replace(':', '')
    )


def label_or_name(prop: Dict[str, Any]) -> str:
    label = prop.get('label')
    if label and label.strip():
        return label
    return prop.get('name', '')


def format_options_vertically(options: List[Dict[str, Any]], indent: str = "  ") -> str:
    """Format select/enum options vertically; compress if too many."""
    if not options:
        return ""

    visible = [opt for opt in options if not opt.get('hidden')]
    if len(visible) > 20:
        first_label = visible[0].get('label') or visible[0].get('value', '')
        last_label = visible[-1].get('label') or visible[-1].get('value', '')
        return f"{indent}**{len(visible)} options** from `{first_label}` to `{last_label}`"

    lines = []
    for opt in visible:
        label = opt.get('label') or ''
        value = opt.get('value') or ''
        if label and value and label != value:
            lines.append(f"{indent}- {label} (`{value}`)")
        else:
            lines.append(f"{indent}- `{label or value}`")
    return "\n".join(lines)


def group_properties_by_type(properties: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """Group properties by 'type' (HubSpot schema type: string, number, date, datetime, bool, enumeration...)."""
    groups: Dict[str, List[str]] = {}
    for prop in properties:
        t = prop.get('type', 'unknown')
        groups.setdefault(t, []).append(label_or_name(prop))
    # Sort names in each group
    for k in groups:
        groups[k].sort()
    return groups


def generate_properties_overview(type_groups: Dict[str, List[str]]) -> str:
    """Generate the Properties Overview section similar to Notion's format."""
    lines: List[str] = ["## Properties Overview", ""]
    for prop_type in sorted(type_groups.keys()):
        props = type_groups[prop_type]
        lines.append(f"### {prop_type} ({len(props)})")
        for name in props:
            lines.append(f"- `{name}`")
        lines.append("")
    return "\n".join(lines)


def generate_detailed_documentation(properties: List[Dict[str, Any]]) -> str:
    """Generate detailed documentation per property with description, fieldType, options, etc."""
    # Sort by display label/name
    props_sorted = sorted(properties, key=lambda p: label_or_name(p).lower())
    lines: List[str] = ["## Detailed Property Documentation", ""]

    for prop in props_sorted:
        name = prop.get('name', '')
        display = label_or_name(prop) or name
        ptype = prop.get('type', 'unknown')
        field_type = prop.get('fieldType')
        description = prop.get('description') or ''
        options = prop.get('options') or []
        calculated = prop.get('calculated') or False
        has_unique = prop.get('hasUniqueValue') or False
        archived = prop.get('archived') or False

        lines.append(f"### {display}")
        if name and name != display:
            lines.append(f"- **Name:** `{name}`")
        lines.append(f"- **Type:** `{ptype}`")
        if field_type:
            lines.append(f"- **Field Type:** `{field_type}`")
        if calculated:
            lines.append("- **Calculated:** `true`")
        if has_unique:
            lines.append("- **Unique:** `true`")
        if archived:
            lines.append("- **Archived:** `true`")
        if description:
            lines.append(f"- **Description:** {description}")

        if ptype == 'enumeration' and options:
            lines.append("- **Options:")
            lines.append(format_options_vertically(options))
        lines.append("")

    return "\n".join(lines)


def generate_markdown_for_object(schema: Dict[str, Any], properties: List[Dict[str, Any]]) -> str:
    """Build the markdown content for a given object's properties."""
    obj_name = schema.get('name') or ''  # API name used in endpoints
    labels = schema.get('labels') or {}
    label_singular = labels.get('singular') or obj_name
    label_plural = labels.get('plural') or f"{label_singular}s"
    object_type_id = schema.get('objectTypeId') or ''
    created_at = schema.get('createdAt') or ''
    updated_at = schema.get('updatedAt') or ''

    type_groups = group_properties_by_type(properties)

    lines: List[str] = []
    lines.append(f"# {label_plural} Properties")
    lines.append("")
    lines.append(f"**Object Name:** `{obj_name}`")
    if object_type_id:
        lines.append("")
        lines.append(f"**Object Type ID:** `{object_type_id}`")
    if created_at:
        lines.append(f"\n**Created:** {created_at}")
    if updated_at:
        lines.append(f"\n**Last Modified:** {updated_at}")
    lines.append(f"\n**Total Properties:** {len(properties)}\n")
    lines.append("---\n")

    # Overview
    lines.append(generate_properties_overview(type_groups))
    lines.append("---\n")

    # Detailed
    lines.append(generate_detailed_documentation(properties))

    lines.append("---\n")
    lines.append(f"*Documentation generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

    return "\n".join(lines)


async def main() -> None:
    print("🚀 Starting HubSpot objects property documentation generation...")

    token = get_access_token()
    if not token:
        print("❌ HUBSPOT_ACCESS_TOKEN not set. Export it and re-run. Example:")
        print("   export HUBSPOT_ACCESS_TOKEN=your_private_app_token")
        return

    # Ensure base dir exists
    base_dir = "/workspaces/automations_hub/hubspot/objects"
    os.makedirs(base_dir, exist_ok=True)

    success = 0
    errors = 0

    async with httpx.AsyncClient() as client:
        schemas = await get_all_schemas(client)
        if not schemas:
            print("⚠️ Could not list schemas. Will fallback to core objects: contacts, companies, deals, tickets")
            fallback = [
                {"name": name, "labels": {"singular": name[:-1] if name.endswith('s') else name, "plural": name}}
                for name in ["contacts", "companies", "deals", "tickets"]
            ]
            schemas = fallback
        else:
            # Always include core objects even if /schemas omits them
            core = ["contacts", "companies", "deals", "tickets"]
            existing_names = {str((s.get('name') or '')).strip().lower() for s in schemas}
            for name in core:
                if name not in existing_names:
                    schemas.append({
                        "name": name,
                        "labels": {
                            "singular": name[:-1] if name.endswith('s') else name,
                            "plural": name
                        }
                    })

        print(f"📊 Found {len(schemas)} objects to process")
        print("")

        # De-dupe by object API name while preserving order
        seen = set()
        deduped = []
        for schema in schemas:
            obj_name_key = (schema.get('name') or '').strip().lower()
            if not obj_name_key or obj_name_key in seen:
                continue
            seen.add(obj_name_key)
            deduped.append(schema)

        for schema in deduped:
            obj_name = schema.get('name') or ''
            display_plural = (schema.get('labels') or {}).get('plural') or obj_name
            if not obj_name:
                continue

            print(f"📋 Processing: {display_plural} ({obj_name})")
            try:
                # Try best-known identifiers first for custom objects
                identifier_candidates = [
                    (schema.get('fullyQualifiedName') or '').strip(),
                    (schema.get('objectTypeId') or '').strip(),
                    obj_name.strip(),
                ]
                props: List[Dict[str, Any]] = []
                for ident in identifier_candidates:
                    if not ident:
                        continue
                    data = await hubspot_get(client, f"/crm/v3/properties/{ident}")
                    if data and isinstance(data, dict) and data.get('results') is not None:
                        props = data.get('results') or []
                        break

                # Some custom objects may return 404 if not licensed/accessible; skip gracefully
                if props is None:
                    print(f"   ❌ Skipped: unable to fetch properties for {obj_name}")
                    errors += 1
                    continue

                content = generate_markdown_for_object(schema, props)

                # Determine output path: hubspot/objects/<object_name>/properties.md
                obj_dir = os.path.join(base_dir, safe_object_dir_name(obj_name))
                os.makedirs(obj_dir, exist_ok=True)
                out_path = os.path.join(obj_dir, "properties.md")

                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                print(f"   ✅ Generated {os.path.relpath(out_path, start=base_dir)} ({len(props)} properties)")
                success += 1

            except Exception as e:
                print(f"   ❌ Error processing {obj_name}: {e}")
                errors += 1

            await asyncio.sleep(0.3)  # polite pacing

    print("\n📊 Generation Summary:")
    print(f"   ✅ Successful: {success}")
    print(f"   ❌ Errors: {errors}")
    print(f"   📁 Files saved under: {base_dir}/<object>/properties.md")
    if success:
        print("\n🎉 HubSpot property documentation complete.")
        print("📖 Each object has:")
        print("   • Vertical property listings grouped by type")
        print("   • Detailed field documentation with options")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted.")
