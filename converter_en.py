#!/usr/bin/env python3
"""
Recursive PHP Language Files to JSON Converter - English Version
================================================================
Tool to convert multilingual language files from .php to .json format recursively

Usage:
1. Place this file in the root directory containing language directories (ar, bn, vi, en...)
2. Run: python converter_en.py
3. Choose whether to delete .php files after successful conversion

Features:
- Recursive scanning of all subdirectories
- Convert .php -> .json in the same directory
- Option to delete .php files after successful conversion
- Detailed reporting by directory
"""

import os
import re
import json
import sys
from pathlib import Path

class RecursivePHPToJSONConverter:
    def __init__(self):
        self.root_dir = Path.cwd()
        self.php_files = []
        self.converted_count = 0
        self.failed_count = 0
        self.deleted_count = 0
        self.results = {}

    def find_php_files_recursive(self, skip_existing=True):
        """Find all .php files in all subdirectories"""
        self.php_files = []

        for php_file in self.root_dir.rglob("*.php"):
            if php_file.name in ["converter_en.py", "converter_vi.py", "load_json_example.php"]:
                continue

            if skip_existing:
                json_file = php_file.with_suffix('.json')
                if json_file.exists():
                    print(f"⏭️  Skip {php_file.relative_to(self.root_dir)} (JSON already exists)")
                    continue

            self.php_files.append(php_file)

        return len(self.php_files)

    def parse_php_array(self, content):
        """Parse PHP array from file content with improved parsing"""
        # Remove comments
        content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        content = re.sub(r'<\?php', '', content)
        content = re.sub(r'\?>', '', content)
        content = content.strip()

        # Extended patterns to match more PHP formats
        patterns = [
            r'return\s*\[(.*?)\];',
            r'return\s*array\s*\((.*?)\);',
            r'\$lang\s*=\s*\[(.*?)\];',
            r'\$lang\s*=\s*array\s*\((.*?)\);',
            r'\$language\s*=\s*\[(.*?)\];',
            r'\$language\s*=\s*array\s*\((.*?)\);',
            r'\$data\s*=\s*\[(.*?)\];',
            r'\$data\s*=\s*array\s*\((.*?)\);',
            r'\$translations\s*=\s*\[(.*?)\];',
            r'\$translations\s*=\s*array\s*\((.*?)\);',
            r'\$messages\s*=\s*\[(.*?)\];',
            r'\$messages\s*=\s*array\s*\((.*?)\);',
        ]

        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                array_content = match.group(1)
                result = self.parse_array_content_improved(array_content)
                if result and len(result) > 0:
                    return result

        return None

    def parse_array_content_improved(self, array_content):
        """Improved array content parsing with better quote handling and nested support"""
        result = {}

        # Clean up the content
        array_content = array_content.strip()

        # Use regex to find all key-value pairs, handling nested structures
        # This regex handles: 'key' => 'value', "key" => "value", with proper quote escaping
        pattern = r"""
            (?:^|,|\n)\s*                       # Start of line or after comma
            (['"])((?:\\.|(?!\1)[^\\])*?)\1     # Quoted key with escape handling
            \s*=>\s*                            # Arrow operator
            (?:
                (['"])((?:\\.|(?!\3)[^\\])*?)\3  # Quoted value with escape handling
                |
                (\d+(?:\.\d+)?)                  # Numeric value
                |
                (true|false|null)                # Boolean/null values
                |
                (\[.*?\])                        # Nested array (simple)
            )
            (?=\s*(?:,|\n|$))                   # Followed by comma, newline, or end
        """

        matches = re.finditer(pattern, array_content, re.VERBOSE | re.DOTALL | re.IGNORECASE)

        for match in matches:
            key_quote, key, value_quote, value, numeric, boolean, nested = match.groups()

            # Clean key (remove escapes)
            clean_key = key.replace('\\"', '"').replace("\\'", "'")

            # Process value based on type
            if value is not None:
                # String value - remove escapes
                clean_value = value.replace('\\"', '"').replace("\\'", "'")
            elif numeric is not None:
                # Keep numeric as string for JSON compatibility
                clean_value = numeric
            elif boolean is not None:
                # Convert boolean to lowercase string
                clean_value = boolean.lower()
            elif nested is not None:
                # For now, convert nested arrays to string representation
                clean_value = nested
            else:
                continue

            result[clean_key] = clean_value

        # Fallback to line-by-line parsing if regex approach fails
        if not result:
            result = self.parse_array_content_fallback(array_content)

        return result

    def parse_array_content_fallback(self, array_content):
        """Fallback line-by-line parsing with improved quote handling"""
        result = {}
        lines = array_content.split('\n')

        for line in lines:
            line = line.strip()
            if not line or line.startswith('//') or line.startswith('/*'):
                continue

            # Remove trailing comma
            line = line.rstrip(',').strip()

            if '=>' in line:
                parts = line.split('=>', 1)
                if len(parts) == 2:
                    key_part = parts[0].strip()
                    value_part = parts[1].strip()

                    # Improved quote extraction
                    key_match = re.search(r"^['\"](.+?)['\"]$", key_part)
                    value_match = re.search(r"^['\"](.+?)['\"]$", value_part)

                    if key_match and value_match:
                        # Remove escaped quotes
                        key = key_match.group(1).replace('\\"', '"').replace("\\'", "'")
                        value = value_match.group(1).replace('\\"', '"').replace("\\'", "'")
                        result[key] = value
                    elif key_match:
                        # Handle non-quoted values (numbers, booleans)
                        key = key_match.group(1).replace('\\"', '"').replace("\\'", "'")
                        value = value_part.strip()
                        # Remove quotes if present but keep the content
                        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                            value = value[1:-1]
                        result[key] = value

        return result

    def convert_file(self, php_file):
        """Convert a PHP file to JSON"""
        try:
            with open(php_file, 'r', encoding='utf-8') as f:
                content = f.read()

            data = self.parse_php_array(content)

            if data is None or len(data) == 0:
                return False, "Cannot parse PHP array or empty array"

            json_file = php_file.with_suffix('.json')

            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return True, f"✅ {len(data)} keys"

        except Exception as e:
            return False, f"Error: {str(e)}"

    def run(self):
        """Run converter tool"""
        print("🌍 PHP to JSON Language Converter (English)")
        print("=" * 50)

        count = self.find_php_files_recursive()

        if count == 0:
            print("✅ No PHP files found to convert!")
            return

        print(f"🔍 Found {count} PHP files to convert")

        choice = input("\n🔥 Delete .php files after conversion? (y/N): ").strip().lower()
        delete_php = choice in ['y', 'yes']

        print("\n🔄 Starting conversion...")

        for php_file in self.php_files:
            success, message = self.convert_file(php_file)

            if success:
                self.converted_count += 1
                print(f"   ✅ {php_file.name} -> {php_file.stem}.json")

                if delete_php:
                    try:
                        php_file.unlink()
                        self.deleted_count += 1
                        print(f"   🗑️  Deleted {php_file.name}")
                    except Exception as e:
                        print(f"   ⚠️  Cannot delete {php_file.name}: {e}")
            else:
                self.failed_count += 1
                print(f"   ❌ {php_file.name}: {message}")

        print(f"\n📊 RESULTS:")
        print(f"   ✅ Success: {self.converted_count} files")
        print(f"   ❌ Failed: {self.failed_count} files")

        if delete_php and self.deleted_count > 0:
            print(f"   🗑️  Deleted: {self.deleted_count} PHP files")

def main():
    try:
        converter = RecursivePHPToJSONConverter()
        converter.run()
    except KeyboardInterrupt:
        print("\n⚠️ Stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
