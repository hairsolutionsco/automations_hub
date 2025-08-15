#!/usr/bin/env python3
"""
Property Matcher: Extract and Match Properties from Notion and HubSpot

This script extracts all properties/fields from Notion databases and HubSpot contacts,
then intelligently matches them based on naming patterns, types, and semantic similarity.
The results are exported to a comprehensive markdown report.
"""

import asyncio
import os
import sys
import httpx
import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from difflib import SequenceMatcher
from collections import defaultdict

# Add current directory to Python path
sys.path.append('.')

# Configuration
NOTION_API_VERSION = '2022-06-28'
HUBSPOT_BASE_URL = 'https://api.hubapi.com'
OUTPUT_FILE = '/workspaces/automations_hub/property_matching_report.md'

class PropertyMatcher:
    def __init__(self):
        self.notion_api_key = os.getenv('NOTION_API_KEY')
        self.hubspot_token = os.getenv('HUBSPOT_API_ACCESS_TOKEN') or os.getenv('HUBSPOT_ACCESS_TOKEN')
        
        if not self.notion_api_key:
            raise ValueError("NOTION_API_KEY environment variable is required")
        if not self.hubspot_token:
            raise ValueError("HUBSPOT_API_ACCESS_TOKEN environment variable is required")
            
        self.notion_properties = {}
        self.hubspot_properties = {}
        self.matches = []
        
    async def fetch_notion_databases(self, client: httpx.AsyncClient) -> List[Dict]:
        """Fetch all accessible Notion databases"""
        print("🔍 Fetching Notion databases...")
        
        # Known database IDs - we'll focus on contacts for now
        database_ids = {
            'contacts': '226f4e0d-84e0-814c-ad70-d478cebeee30'
        }
        
        databases = []
        headers = {
            'Authorization': f'Bearer {self.notion_api_key}',
            'Content-Type': 'application/json',
            'Notion-Version': NOTION_API_VERSION
        }
        
        for db_name, db_id in database_ids.items():
            try:
                print(f"  📡 Fetching live data for {db_name} database...")
                response = await client.get(
                    f'https://api.notion.com/v1/databases/{db_id}',
                    headers=headers,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    db_data = response.json()
                    databases.append({
                        'name': db_name,
                        'id': db_id,
                        'data': db_data,
                        'properties': db_data.get('properties', {})
                    })
                    print(f"    ✅ Live data fetched for {db_name}")
                else:
                    print(f"    ❌ Failed to fetch {db_name}: {response.status_code} {response.text}")
                    # Fallback to documentation if API fails
                    fallback_path = f'/workspaces/automations_hub/notion/databases/{db_name}.md'
                    if os.path.exists(fallback_path):
                        with open(fallback_path, 'r') as f:
                            content = f.read()
                            databases.append({
                                'name': db_name,
                                'file_path': fallback_path,
                                'content': content,
                                'is_fallback': True
                            })
                        print(f"    ⚠️  Using documentation fallback for {db_name}")
                        
            except Exception as e:
                print(f"    ❌ Exception fetching {db_name}: {e}")
                # Fallback to documentation
                fallback_path = f'/workspaces/automations_hub/notion/databases/{db_name}.md'
                if os.path.exists(fallback_path):
                    with open(fallback_path, 'r') as f:
                        content = f.read()
                        databases.append({
                            'name': db_name,
                            'file_path': fallback_path,
                            'content': content,
                            'is_fallback': True
                        })
                    print(f"    ⚠️  Using documentation fallback for {db_name}")
        
        return databases
    
    async def extract_notion_properties(self, client: httpx.AsyncClient):
        """Extract properties from Notion databases"""
        print("📊 Extracting Notion properties...")
        
        databases = await self.fetch_notion_databases(client)
        
        for db in databases:
            db_name = db['name']
            
            if 'properties' in db and not db.get('is_fallback', False):
                # Live API data
                properties = self._parse_notion_properties_from_api(db['properties'])
                self.notion_properties[db_name] = properties
                print(f"  ✅ {db_name}: {len(properties)} properties (live data)")
            elif 'content' in db:
                # Fallback to documentation
                content = db['content']
                properties = self._parse_notion_properties_from_docs(content)
                self.notion_properties[db_name] = properties
                print(f"  ✅ {db_name}: {len(properties)} properties (from docs)")
            else:
                print(f"  ⚠️  {db_name}: No properties found")
                
    def _parse_notion_properties_from_api(self, properties_data: Dict) -> Dict[str, Dict]:
        """Parse Notion properties from live API data"""
        properties = {}
        
        for prop_name, prop_data in properties_data.items():
            prop_type = prop_data.get('type', 'unknown')
            prop_id = prop_data.get('id', '')
            
            # Extract additional details based on property type
            details = []
            if prop_type == 'select' and 'select' in prop_data:
                options = prop_data['select'].get('options', [])
                if options:
                    details.append(f"Options: {', '.join([opt.get('name', '') for opt in options])}")
                    
            elif prop_type == 'multi_select' and 'multi_select' in prop_data:
                options = prop_data['multi_select'].get('options', [])
                if options:
                    details.append(f"Options: {', '.join([opt.get('name', '') for opt in options])}")
                    
            elif prop_type == 'relation' and 'relation' in prop_data:
                related_db = prop_data['relation'].get('database_id', '')
                if related_db:
                    details.append(f"Related to: {related_db}")
                    
            elif prop_type == 'formula' and 'formula' in prop_data:
                expression = prop_data['formula'].get('expression', '')
                if expression:
                    details.append(f"Formula: {expression}")
            
            properties[prop_name] = {
                'type': prop_type,
                'id': prop_id,
                'details': details
            }
        
        return properties
    
    def _parse_notion_properties_from_docs(self, content: str) -> Dict[str, Dict]:
        """Parse Notion properties from markdown documentation"""
        properties = {}
        
        # Look for property sections in the documentation
        lines = content.split('\n')
        current_property = None
        in_property_section = False
        
        for line in lines:
            # Check if we're in a property documentation section
            if '### ' in line and not line.startswith('####'):
                # This might be a property name
                prop_name = line.replace('### ', '').strip()
                if prop_name and not any(skip in prop_name.lower() for skip in ['overview', 'documentation', 'summary', 'details']):
                    current_property = prop_name
                    properties[current_property] = {'type': 'unknown', 'details': []}
                    in_property_section = True
                    
            elif current_property and in_property_section:
                if line.startswith('- **Type:**'):
                    prop_type = line.replace('- **Type:**', '').strip().replace('`', '')
                    properties[current_property]['type'] = prop_type
                elif line.startswith('- **'):
                    # Other property details
                    properties[current_property]['details'].append(line.strip())
                elif line.strip() == '' and len(properties[current_property]['details']) > 0:
                    # End of property section
                    in_property_section = False
                    
        # Also look for type groupings in overview sections
        type_section_pattern = r'### (\w+) \((\d+)\)'
        matches = re.findall(type_section_pattern, content)
        
        for prop_type, count in matches:
            # Find properties of this type
            if f"### {prop_type}" in content:
                section_start = content.find(f"### {prop_type}")
                section_end = content.find('###', section_start + 1)
                if section_end == -1:
                    section_end = len(content)
                    
                section_content = content[section_start:section_end]
                prop_names = re.findall(r'- `([^`]+)`', section_content)
                
                for prop_name in prop_names:
                    if prop_name not in properties:
                        properties[prop_name] = {'type': prop_type, 'details': []}
        
        return properties
    
    async def fetch_hubspot_contact_properties(self, client: httpx.AsyncClient) -> List[Dict]:
        """Fetch HubSpot contact properties"""
        print("🔍 Fetching HubSpot contact properties...")
        
        headers = {
            'Authorization': f'Bearer {self.hubspot_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = await client.get(
                f'{HUBSPOT_BASE_URL}/crm/v3/properties/contacts',
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('results', [])
            else:
                print(f"❌ Error fetching HubSpot properties: {response.status_code} {response.text}")
                return []
                
        except Exception as e:
            print(f"❌ Exception fetching HubSpot properties: {e}")
            return []
    
    async def extract_hubspot_properties(self, client: httpx.AsyncClient):
        """Extract and process HubSpot contact properties"""
        print("📊 Extracting HubSpot contact properties...")
        
        properties = await self.fetch_hubspot_contact_properties(client)
        
        for prop in properties:
            name = prop.get('name', '')
            label = prop.get('label', name)
            prop_type = prop.get('type', 'unknown')
            field_type = prop.get('fieldType', '')
            description = prop.get('description', '')
            group_name = prop.get('groupName', '')
            
            self.hubspot_properties[name] = {
                'name': name,
                'label': label,
                'type': prop_type,
                'field_type': field_type,
                'description': description,
                'group': group_name,
                'hubspot_defined': prop.get('hubspotDefined', False),
                'calculated': prop.get('calculated', False),
                'options': prop.get('options', [])
            }
        
        print(f"  ✅ Extracted {len(self.hubspot_properties)} HubSpot contact properties")
    
    def calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings"""
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    
    def normalize_name(self, name: str) -> str:
        """Normalize property names for better matching"""
        # Remove common prefixes/suffixes and normalize
        normalized = re.sub(r'[_\-\s]+', '_', name.lower())
        normalized = re.sub(r'^(hs_|contact_|customer_|client_)', '', normalized)
        normalized = re.sub(r'(_id|_key|_value|_field)$', '', normalized)
        return normalized.strip('_')
    
    def match_by_semantic_similarity(self, notion_name: str, hubspot_names: List[str]) -> List[Tuple[str, float]]:
        """Find HubSpot properties that are semantically similar to Notion property"""
        matches = []
        notion_normalized = self.normalize_name(notion_name)
        
        for hs_name in hubspot_names:
            hs_normalized = self.normalize_name(hs_name)
            
            # Direct name similarity
            name_similarity = self.calculate_similarity(notion_normalized, hs_normalized)
            
            # Label similarity (if available)
            hs_prop = self.hubspot_properties[hs_name]
            label_similarity = self.calculate_similarity(notion_normalized, self.normalize_name(hs_prop['label']))
            
            # Take the higher similarity
            max_similarity = max(name_similarity, label_similarity)
            
            if max_similarity > 0.6:  # Threshold for potential matches
                matches.append((hs_name, max_similarity))
        
        return sorted(matches, key=lambda x: x[1], reverse=True)
    
    def match_by_type_compatibility(self, notion_type: str, hubspot_type: str, hubspot_field_type: str) -> float:
        """Calculate type compatibility score"""
        # Type mapping for compatibility
        type_mappings = {
            'title': ['string', 'text'],
            'rich_text': ['string', 'text', 'textarea'],
            'number': ['number', 'enumeration'],
            'select': ['enumeration', 'radio', 'select'],
            'multi_select': ['enumeration', 'checkbox'],
            'date': ['date', 'datetime'],
            'checkbox': ['bool', 'boolean'],
            'email': ['string'],
            'phone_number': ['phonenumber', 'string'],
            'url': ['string'],
            'people': ['enumeration'],
            'relation': ['enumeration'],
            'rollup': ['number', 'string'],
            'formula': ['number', 'string', 'text']
        }
        
        notion_compatible = type_mappings.get(notion_type.lower(), [notion_type.lower()])
        
        if hubspot_type.lower() in notion_compatible or hubspot_field_type.lower() in notion_compatible:
            return 1.0
        
        # Partial compatibility
        if any(comp in hubspot_type.lower() or comp in hubspot_field_type.lower() for comp in notion_compatible):
            return 0.7
            
        return 0.0
    
    def perform_matching(self):
        """Perform intelligent matching between Notion and HubSpot properties"""
        print("🔄 Performing property matching...")
        
        hubspot_names = list(self.hubspot_properties.keys())
        
        for db_name, notion_props in self.notion_properties.items():
            for notion_prop_name, notion_prop_data in notion_props.items():
                notion_type = notion_prop_data.get('type', 'unknown')
                
                # Find potential matches
                semantic_matches = self.match_by_semantic_similarity(notion_prop_name, hubspot_names)
                
                for hs_name, similarity in semantic_matches[:3]:  # Top 3 matches
                    hs_prop = self.hubspot_properties[hs_name]
                    
                    # Calculate type compatibility
                    type_compatibility = self.match_by_type_compatibility(
                        notion_type, hs_prop['type'], hs_prop['field_type']
                    )
                    
                    # Overall match score
                    overall_score = (similarity * 0.7) + (type_compatibility * 0.3)
                    
                    if overall_score > 0.5:  # Threshold for valid matches
                        match_quality = 'High' if overall_score > 0.8 else 'Medium' if overall_score > 0.65 else 'Low'
                        
                        self.matches.append({
                            'notion_database': db_name,
                            'notion_property': notion_prop_name,
                            'notion_type': notion_type,
                            'hubspot_property': hs_name,
                            'hubspot_label': hs_prop['label'],
                            'hubspot_type': hs_prop['type'],
                            'hubspot_field_type': hs_prop['field_type'],
                            'hubspot_group': hs_prop['group'],
                            'semantic_similarity': round(similarity, 3),
                            'type_compatibility': round(type_compatibility, 3),
                            'overall_score': round(overall_score, 3),
                            'match_quality': match_quality,
                            'hubspot_description': hs_prop['description']
                        })
        
        # Sort matches by overall score
        self.matches.sort(key=lambda x: x['overall_score'], reverse=True)
        print(f"  ✅ Found {len(self.matches)} potential property matches")
    
    def generate_markdown_report(self):
        """Generate comprehensive markdown report"""
        print("📝 Generating markdown report...")
        
        report = f"""# Property Matching Report: Notion ↔ HubSpot
        
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

This report analyzes and matches properties between Notion databases and HubSpot contact properties, providing insights for data synchronization and integration planning.

### Statistics
- **Notion Databases Analyzed:** {len(self.notion_properties)}
- **Total Notion Properties:** {sum(len(props) for props in self.notion_properties.values())}
- **HubSpot Contact Properties:** {len(self.hubspot_properties)}
- **Potential Matches Found:** {len(self.matches)}
- **High-Quality Matches:** {len([m for m in self.matches if m['match_quality'] == 'High'])}
- **Medium-Quality Matches:** {len([m for m in self.matches if m['match_quality'] == 'Medium'])}

## Matching Methodology

The matching algorithm uses a combination of:
1. **Semantic Similarity (70% weight):** String similarity between property names and labels
2. **Type Compatibility (30% weight):** Data type compatibility between systems
3. **Normalization:** Removes common prefixes/suffixes and standardizes naming

### Match Quality Levels
- **High (>0.8):** Strong confidence, likely direct mapping candidates
- **Medium (0.65-0.8):** Good candidates requiring validation
- **Low (0.5-0.65):** Possible matches requiring careful review

"""
        
        # Add high-quality matches section
        high_matches = [m for m in self.matches if m['match_quality'] == 'High']
        if high_matches:
            report += "\n## 🟢 High-Quality Matches (Strong Candidates)\n\n"
            for match in high_matches:
                report += self._format_match_entry(match)
        
        # Add medium-quality matches section
        medium_matches = [m for m in self.matches if m['match_quality'] == 'Medium']
        if medium_matches:
            report += "\n## 🟡 Medium-Quality Matches (Good Candidates)\n\n"
            for match in medium_matches:
                report += self._format_match_entry(match)
        
        # Add low-quality matches section
        low_matches = [m for m in self.matches if m['match_quality'] == 'Low']
        if low_matches:
            report += "\n## 🟠 Low-Quality Matches (Requires Review)\n\n"
            for match in low_matches:
                report += self._format_match_entry(match)
        
        # Add database breakdown
        report += "\n## Database-by-Database Breakdown\n\n"
        for db_name, properties in self.notion_properties.items():
            db_matches = [m for m in self.matches if m['notion_database'] == db_name]
            report += f"### {db_name.replace('_', ' ').title()}\n"
            report += f"- **Total Properties:** {len(properties)}\n"
            report += f"- **Matches Found:** {len(db_matches)}\n"
            report += f"- **Match Rate:** {(len(db_matches) / len(properties) * 100):.1f}%\n\n"
            
            if db_matches:
                for match in db_matches[:5]:  # Top 5 matches per database
                    report += f"  - `{match['notion_property']}` → `{match['hubspot_property']}` ({match['match_quality']})\n"
                if len(db_matches) > 5:
                    report += f"  - ... and {len(db_matches) - 5} more matches\n"
            report += "\n"
        
        # Add unmapped properties sections
        report += self._generate_unmapped_sections()
        
        # Add property type analysis
        report += self._generate_type_analysis()
        
        # Add recommendations
        report += self._generate_recommendations()
        
        # Write to file
        with open(OUTPUT_FILE, 'w') as f:
            f.write(report)
        
        print(f"  ✅ Report saved to: {OUTPUT_FILE}")
    
    def _format_match_entry(self, match: Dict) -> str:
        """Format a single match entry for the report"""
        return f"""### {match['notion_database']} → HubSpot Contact

**Notion Property:** `{match['notion_property']}` ({match['notion_type']})  
**HubSpot Property:** `{match['hubspot_property']}` ({match['hubspot_type']})  
**HubSpot Label:** {match['hubspot_label']}  
**HubSpot Group:** {match['hubspot_group']}  

**Match Scores:**
- Semantic Similarity: {match['semantic_similarity']}
- Type Compatibility: {match['type_compatibility']}
- Overall Score: {match['overall_score']} ({match['match_quality']})

**HubSpot Description:** {match['hubspot_description'] or 'No description available'}

---

"""
    
    def _generate_unmapped_sections(self) -> str:
        """Generate sections for unmapped properties"""
        report = "\n## Unmapped Properties Analysis\n\n"
        
        # Notion properties without matches
        matched_notion = set((m['notion_database'], m['notion_property']) for m in self.matches)
        unmapped_notion = []
        
        for db_name, properties in self.notion_properties.items():
            for prop_name in properties:
                if (db_name, prop_name) not in matched_notion:
                    unmapped_notion.append((db_name, prop_name, properties[prop_name]))
        
        if unmapped_notion:
            report += f"### Notion Properties Without Matches ({len(unmapped_notion)})\n\n"
            for db, prop, data in unmapped_notion[:20]:  # Limit to first 20
                report += f"- **{db}**: `{prop}` ({data.get('type', 'unknown')})\n"
            if len(unmapped_notion) > 20:
                report += f"- ... and {len(unmapped_notion) - 20} more\n"
            report += "\n"
        
        # HubSpot properties without matches
        matched_hubspot = set(m['hubspot_property'] for m in self.matches)
        unmapped_hubspot = [name for name in self.hubspot_properties if name not in matched_hubspot]
        
        if unmapped_hubspot:
            report += f"### HubSpot Properties Without Matches ({len(unmapped_hubspot)})\n\n"
            for prop_name in unmapped_hubspot[:20]:  # Limit to first 20
                prop = self.hubspot_properties[prop_name]
                report += f"- `{prop_name}` ({prop['type']}) - {prop['label']}\n"
            if len(unmapped_hubspot) > 20:
                report += f"- ... and {len(unmapped_hubspot) - 20} more\n"
            report += "\n"
        
        return report
    
    def _generate_type_analysis(self) -> str:
        """Generate property type analysis"""
        report = "\n## Property Type Analysis\n\n"
        
        # Notion type distribution
        notion_types = defaultdict(int)
        for properties in self.notion_properties.values():
            for prop_data in properties.values():
                notion_types[prop_data.get('type', 'unknown')] += 1
        
        report += "### Notion Property Types\n"
        for ptype, count in sorted(notion_types.items(), key=lambda x: x[1], reverse=True):
            report += f"- **{ptype}**: {count} properties\n"
        report += "\n"
        
        # HubSpot type distribution
        hubspot_types = defaultdict(int)
        for prop in self.hubspot_properties.values():
            hubspot_types[prop['type']] += 1
        
        report += "### HubSpot Property Types\n"
        for ptype, count in sorted(hubspot_types.items(), key=lambda x: x[1], reverse=True):
            report += f"- **{ptype}**: {count} properties\n"
        report += "\n"
        
        return report
    
    def _generate_recommendations(self) -> str:
        """Generate recommendations section"""
        high_matches = len([m for m in self.matches if m['match_quality'] == 'High'])
        medium_matches = len([m for m in self.matches if m['match_quality'] == 'Medium'])
        
        return f"""## Recommendations

### Immediate Actions
1. **Implement High-Quality Matches ({high_matches})**: These mappings have strong confidence and can be implemented with minimal validation.

2. **Validate Medium-Quality Matches ({medium_matches})**: Review these mappings for business logic compatibility before implementation.

3. **Custom Property Strategy**: Consider creating custom HubSpot properties for unmapped Notion fields that are business-critical.

### Integration Strategy
1. **Start with Contact Synchronization**: Focus on the strongest matches for contact data first.
2. **Implement Bi-directional Sync**: Consider which direction should be the source of truth for each property.
3. **Data Validation**: Implement validation rules to ensure data integrity during synchronization.
4. **Regular Reviews**: Properties and business needs evolve; schedule quarterly reviews of mappings.

### Technical Considerations
1. **Data Type Conversion**: Plan for type conversions (e.g., multi-select to single values).
2. **Field Length Limits**: HubSpot has character limits for different field types.
3. **API Rate Limits**: Plan synchronization frequency considering API limitations.
4. **Error Handling**: Implement robust error handling for failed synchronizations.

---

*Report generated by Property Matcher v1.0*
"""

    async def run(self):
        """Main execution method"""
        print("🚀 Starting Property Matching Analysis...\n")
        
        async with httpx.AsyncClient() as client:
            # Extract properties from both systems
            await self.extract_notion_properties(client)
            await self.extract_hubspot_properties(client)
            
            # Perform matching
            self.perform_matching()
            
            # Generate report
            self.generate_markdown_report()
        
        print("\n✅ Property matching analysis complete!")
        print(f"📄 Full report available at: {OUTPUT_FILE}")

async def main():
    """Main entry point"""
    try:
        matcher = PropertyMatcher()
        await matcher.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
