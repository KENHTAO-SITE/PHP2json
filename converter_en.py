#!/usr/bin/env python3
"""
Robust PHP Language Files to JSON Converter - English Version
============================================================
Enhanced tool for safe and comprehensive PHP to JSON conversion

Features:
- Multiple parsing strategies with fallbacks
- Detailed error logging and validation
- Slower, safer processing for large file sets
- Advanced PHP structure support
- Comprehensive file analysis before conversion
"""

import os
import re
import json
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List

class RobustPHPToJSONConverter:
    def __init__(self):
        self.root_dir = Path.cwd()
        self.php_files = []
        self.converted_count = 0
        self.failed_count = 0
        self.deleted_count = 0
        self.failed_files = []
        self.processing_delay = 0.1  # Small delay between files for safety

    def find_php_files_recursive(self, skip_existing=True):
        """Find all .php files with detailed analysis"""
        self.php_files = []

        print("🔍 Scanning directories for PHP files...")
        for php_file in self.root_dir.rglob("*.php"):
            if php_file.name in ["converter_en.py", "converter_vi.py", "load_json_example.php"]:
                continue

            if skip_existing:
                json_file = php_file.with_suffix('.json')
                if json_file.exists():
                    print(f"⏭️  Skip {php_file.relative_to(self.root_dir)} (JSON exists)")
                    continue

            self.php_files.append(php_file)

        print(f"📊 Found {len(self.php_files)} PHP files to process")
        return len(self.php_files)

    def analyze_php_file(self, php_file: Path) -> Dict[str, Any]:
        """Analyze PHP file structure before conversion"""
        try:
            with open(php_file, 'r', encoding='utf-8') as f:
                content = f.read()

            analysis = {
                'file_size': len(content),
                'line_count': content.count('\n') + 1,
                'has_php_tags': '<?php' in content or '<?=' in content,
                'has_return_statement': re.search(r'\breturn\s+', content, re.IGNORECASE) is not None,
                'has_variable_assignment': re.search(r'\$\w+\s*=', content) is not None,
                'array_syntax': [],
                'variable_names': [],
                'encoding': 'utf-8'
            }

            # Detect array syntax types
            if re.search(r'\[.*?\]', content, re.DOTALL):
                analysis['array_syntax'].append('short_array')
            if re.search(r'array\s*\(', content, re.IGNORECASE):
                analysis['array_syntax'].append('long_array')

            # Extract variable names
            var_matches = re.findall(r'\$(\w+)\s*=', content)
            analysis['variable_names'] = list(set(var_matches))

            return analysis

        except Exception as e:
            return {'error': str(e)}

    def parse_php_array_robust(self, content: str) -> Optional[Dict[str, Any]]:
        """Multiple-strategy PHP parsing with comprehensive fallbacks"""

        # Strategy 1: Advanced regex with nested structure support
        result = self._parse_strategy_advanced_regex(content)
        if result and len(result) > 0:
            return result

        # Strategy 2: PHP-like tokenizer approach
        result = self._parse_strategy_tokenizer(content)
        if result and len(result) > 0:
            return result

        # Strategy 3: Line-by-line with state machine
        result = self._parse_strategy_state_machine(content)
        if result and len(result) > 0:
            return result

        # Strategy 4: Regex with manual nested handling
        result = self._parse_strategy_manual_nested(content)
        if result and len(result) > 0:
            return result

        return None

    def _parse_strategy_advanced_regex(self, content: str) -> Optional[Dict[str, Any]]:
        """Strategy 1: Advanced regex parsing"""
        try:
            # Clean content
            content = self._clean_php_content(content)

            # Extended patterns for various PHP structures
            patterns = [
                r'return\s*\[(.*?)\];',
                r'return\s*array\s*\((.*?)\);',
                r'\$(?:lang|language|data|translations|messages|text|strings)\s*=\s*\[(.*?)\];',
                r'\$(?:lang|language|data|translations|messages|text|strings)\s*=\s*array\s*\((.*?)\);',
            ]

            for pattern in patterns:
                match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
                if match:
                    array_content = match.group(1)
                    result = self._parse_array_content_advanced(array_content)
                    if result:
                        return result

        except Exception as e:
            print(f"   ⚠️  Strategy 1 failed: {e}")

        return None

    def _parse_strategy_tokenizer(self, content: str) -> Optional[Dict[str, Any]]:
        """Strategy 2: Tokenizer-like approach"""
        try:
            content = self._clean_php_content(content)
            result = {}

            # Find array start
            array_start = None
            for pattern in [r'return\s*\[', r'return\s*array\s*\(', r'\$\w+\s*=\s*\[', r'\$\w+\s*=\s*array\s*\(']:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    array_start = match.end()
                    break

            if array_start is None:
                return None

            # Extract key-value pairs with better parsing
            remaining_content = content[array_start:]

            # Use improved regex for key-value extraction
            kv_pattern = r"""
                (?:^|,|\n)\s*                    # Start or separator
                (['\"])((?:\\.|(?!\1)[^\\])*?)\1  # Quoted key
                \s*=>\s*                         # Arrow
                (?:
                    (['\"])((?:\\.|(?!\3)[^\\])*?)\3  # Quoted value
                    |
                    (\d+(?:\.\d+)?)              # Number
                    |
                    (true|false|null)            # Boolean/null
                    |
                    (\[(?:[^\[\]]|(?7))*\])      # Simple nested array
                )
            """

            matches = re.finditer(kv_pattern, remaining_content, re.VERBOSE | re.DOTALL | re.IGNORECASE)

            for match in matches:
                groups = match.groups()
                if len(groups) >= 4:
                    key = self._clean_string_value(groups[1])

                    # Determine value
                    if groups[3]:  # String value
                        value = self._clean_string_value(groups[3])
                    elif groups[4]:  # Number
                        value = groups[4]
                    elif groups[5]:  # Boolean/null
                        value = groups[5].lower()
                    elif groups[6]:  # Nested array
                        value = groups[6]  # Keep as string for now
                    else:
                        continue

                    result[key] = value

            return result if result else None

        except Exception as e:
            print(f"   ⚠️  Strategy 2 failed: {e}")

        return None

    def _parse_strategy_state_machine(self, content: str) -> Optional[Dict[str, Any]]:
        """Strategy 3: State machine line-by-line parsing"""
        try:
            content = self._clean_php_content(content)
            lines = content.split('\n')
            result = {}

            in_array = False
            current_key = None
            current_value = ""
            bracket_count = 0
            quote_char = None

            for line_no, line in enumerate(lines, 1):
                line = line.strip()

                if not line or line.startswith('//') or line.startswith('/*'):
                    continue

                # Start of array
                if not in_array and ('=>' in line or re.search(r'return\s*[\[\(]|^\$\w+\s*=\s*[\[\(]', line)):
                    in_array = True

                if not in_array:
                    continue

                # Process line for key-value pairs
                if '=>' in line and current_key is None:
                    parts = line.split('=>', 1)
                    if len(parts) == 2:
                        key_part = parts[0].strip()
                        value_part = parts[1].strip()

                        # Extract key
                        key_match = re.search(r"['\"]([^'\"]*)['\"]", key_part)
                        if key_match:
                            current_key = self._clean_string_value(key_match.group(1))

                            # Extract value
                            value_match = re.search(r"['\"]([^'\"]*)['\"]", value_part)
                            if value_match:
                                result[current_key] = self._clean_string_value(value_match.group(1))
                                current_key = None
                            else:
                                # Multi-line value might be starting
                                current_value = value_part

            return result if result else None

        except Exception as e:
            print(f"   ⚠️  Strategy 3 failed: {e}")

        return None

    def _parse_strategy_manual_nested(self, content: str) -> Optional[Dict[str, Any]]:
        """Strategy 4: Manual nested structure handling"""
        try:
            content = self._clean_php_content(content)
            result = {}

            # Find all top-level key-value pairs
            # This regex handles nested structures by counting brackets
            pattern = r"""
                (['\"])((?:\\.|(?!\1)[^\\])*?)\1    # Key in quotes
                \s*=>\s*                            # Arrow
                (?:
                    (['\"])((?:\\.|(?!\3)[^\\])*?)\3 # Simple quoted value
                    |
                    (\d+(?:\.\d+)?)                 # Numeric value
                    |
                    (true|false|null)               # Boolean/null
                    |
                    (\[(?:[^\[\]]++|(?7))*+\])      # Nested array (possessive)
                )
            """

            matches = re.finditer(pattern, content, re.VERBOSE | re.DOTALL | re.IGNORECASE)

            for match in matches:
                try:
                    key_quote, key, value_quote, value, numeric, boolean, nested = match.groups()

                    clean_key = self._clean_string_value(key)

                    if value is not None:
                        clean_value = self._clean_string_value(value)
                    elif numeric is not None:
                        clean_value = numeric
                    elif boolean is not None:
                        clean_value = boolean.lower()
                    elif nested is not None:
                        # Try to parse nested array or keep as string
                        clean_value = self._parse_nested_array(nested) or nested
                    else:
                        continue

                    result[clean_key] = clean_value

                except Exception as e:
                    print(f"   ⚠️  Error parsing match: {e}")
                    continue

            return result if result else None

        except Exception as e:
            print(f"   ⚠️  Strategy 4 failed: {e}")

        return None

    def _clean_php_content(self, content: str) -> str:
        """Clean PHP content for parsing"""
        # Remove PHP tags
        content = re.sub(r'<\?php\s*', '', content)
        content = re.sub(r'\?>', '', content)

        # Remove comments (improved)
        content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        content = re.sub(r'#.*?$', '', content, flags=re.MULTILINE)

        return content.strip()

    def _clean_string_value(self, value: str) -> str:
        """Clean string value by removing escapes"""
        if not value:
            return value

        # Handle escaped quotes
        value = value.replace('\\"', '"')
        value = value.replace("\\'", "'")
        value = value.replace('\\\\', '\\')

        return value

    def _parse_nested_array(self, nested_content: str) -> Optional[str]:
        """Parse nested array content"""
        # For now, return as formatted string
        # Could be enhanced to return actual nested dict
        try:
            # Clean up the nested content
            nested_content = nested_content.strip('[]()').strip()
            return nested_content
        except:
            return None

    def _parse_array_content_advanced(self, array_content: str) -> Optional[Dict[str, Any]]:
        """Advanced array content parsing"""
        result = {}

        try:
            # Handle multi-line entries better
            # Split by commas but respect quotes and nested structures
            entries = self._smart_split_array_entries(array_content)

            for entry in entries:
                entry = entry.strip()
                if not entry or entry.startswith('//'):
                    continue

                if '=>' in entry:
                    parts = entry.split('=>', 1)
                    if len(parts) == 2:
                        key_part = parts[0].strip()
                        value_part = parts[1].strip()

                        # Extract key
                        key_match = re.search(r"['\"]([^'\"]*)['\"]", key_part)
                        if key_match:
                            key = self._clean_string_value(key_match.group(1))

                            # Extract value
                            value_match = re.search(r"['\"]([^'\"]*)['\"]", value_part)
                            if value_match:
                                value = self._clean_string_value(value_match.group(1))
                                result[key] = value

        except Exception as e:
            print(f"   ⚠️  Advanced parsing failed: {e}")

        return result if result else None

    def _smart_split_array_entries(self, content: str) -> List[str]:
        """Smart split that respects quotes and nested structures"""
        entries = []
        current_entry = ""
        in_quotes = False
        quote_char = None
        bracket_depth = 0

        i = 0
        while i < len(content):
            char = content[i]

            if char in ['"', "'"] and (i == 0 or content[i-1] != '\\'):
                if not in_quotes:
                    in_quotes = True
                    quote_char = char
                elif char == quote_char:
                    in_quotes = False
                    quote_char = None

            elif not in_quotes:
                if char in ['[', '(']:
                    bracket_depth += 1
                elif char in [']', ')']:
                    bracket_depth -= 1
                elif char == ',' and bracket_depth == 0:
                    entries.append(current_entry)
                    current_entry = ""
                    i += 1
                    continue

            current_entry += char
            i += 1

        if current_entry.strip():
            entries.append(current_entry)

        return entries

    def validate_json_output(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate JSON output before saving"""
        try:
            if not data:
                return False, "Empty data"

            if not isinstance(data, dict):
                return False, "Data is not a dictionary"

            # Check for reasonable number of keys
            if len(data) == 0:
                return False, "No keys found"

            if len(data) > 10000:  # Sanity check
                return False, f"Too many keys ({len(data)}), possible parsing error"

            # Test JSON serialization
            json.dumps(data, ensure_ascii=False, indent=2)

            return True, f"Valid with {len(data)} keys"

        except Exception as e:
            return False, f"JSON validation failed: {e}"

    def convert_file_robust(self, php_file: Path) -> Tuple[bool, str, Dict[str, Any]]:
        """Convert a PHP file with robust error handling"""
        conversion_info = {
            'file': str(php_file),
            'analysis': {},
            'strategies_tried': [],
            'validation': {}
        }

        try:
            print(f"   📁 Processing: {php_file.name}")

            # Analyze file first
            analysis = self.analyze_php_file(php_file)
            conversion_info['analysis'] = analysis

            if 'error' in analysis:
                return False, f"File analysis failed: {analysis['error']}", conversion_info

            print(f"      📏 Size: {analysis['file_size']} bytes, Lines: {analysis['line_count']}")
            if analysis['variable_names']:
                print(f"      🔤 Variables: {', '.join(analysis['variable_names'][:3])}{'...' if len(analysis['variable_names']) > 3 else ''}")

            # Read file content
            with open(php_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Try parsing with multiple strategies
            data = self.parse_php_array_robust(content)

            if data is None:
                return False, "All parsing strategies failed", conversion_info

            # Validate output
            is_valid, validation_msg = self.validate_json_output(data)
            conversion_info['validation'] = {'valid': is_valid, 'message': validation_msg}

            if not is_valid:
                return False, f"Validation failed: {validation_msg}", conversion_info

            print(f"      ✅ Parsed: {validation_msg}")

            # Save JSON file
            json_file = php_file.with_suffix('.json')
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return True, validation_msg, conversion_info

        except Exception as e:
            return False, f"Conversion error: {str(e)}", conversion_info

    def run_robust(self):
        """Run converter with enhanced robustness"""
        print("🌍 Robust PHP to JSON Language Converter (English)")
        print("=" * 60)

        count = self.find_php_files_recursive()

        if count == 0:
            print("✅ No PHP files found to convert!")
            return

        print(f"\n🎯 Processing Strategy:")
        print(f"   • Multiple parsing fallbacks")
        print(f"   • Detailed validation")
        print(f"   • Safe processing with {self.processing_delay}s delay")
        print(f"   • Comprehensive error logging")

        choice = input(f"\n🔥 Delete .php files after successful conversion? (y/N): ").strip().lower()
        delete_php = choice in ['y', 'yes']

        if delete_php:
            confirm = input("⚠️  Are you sure? This cannot be undone (y/N): ").strip().lower()
            delete_php = confirm in ['y', 'yes']

        print(f"\n🔄 Starting robust conversion of {count} files...")
        print("=" * 60)

        failed_details = []

        for i, php_file in enumerate(self.php_files, 1):
            print(f"\n📊 [{i}/{count}] {php_file.relative_to(self.root_dir)}")

            success, message, info = self.convert_file_robust(php_file)

            if success:
                self.converted_count += 1
                print(f"   ✅ {php_file.name} -> {php_file.stem}.json ({message})")

                if delete_php:
                    try:
                        php_file.unlink()
                        self.deleted_count += 1
                        print(f"   🗑️  Deleted {php_file.name}")
                    except Exception as e:
                        print(f"   ⚠️  Cannot delete {php_file.name}: {e}")
            else:
                self.failed_count += 1
                self.failed_files.append(php_file)
                failed_details.append({
                    'file': php_file.name,
                    'error': message,
                    'info': info
                })
                print(f"   ❌ {php_file.name}: {message}")

            # Small delay for safety
            if self.processing_delay > 0:
                time.sleep(self.processing_delay)

        self._print_final_results(failed_details)

    def _print_final_results(self, failed_details: List[Dict]):
        """Print comprehensive final results"""
        print(f"\n" + "=" * 60)
        print(f"📊 FINAL RESULTS:")
        print(f"   ✅ Success: {self.converted_count} files")
        print(f"   ❌ Failed: {self.failed_count} files")

        if self.deleted_count > 0:
            print(f"   🗑️  Deleted: {self.deleted_count} PHP files")

        if failed_details:
            print(f"\n❌ FAILED FILES ANALYSIS:")
            error_summary = {}
            for detail in failed_details:
                error_type = detail['error'].split(':')[0]
                error_summary[error_type] = error_summary.get(error_type, 0) + 1

            for error_type, count in error_summary.items():
                print(f"   • {error_type}: {count} files")

        success_rate = (self.converted_count / len(self.php_files)) * 100 if self.php_files else 0
        print(f"\n🎯 Success Rate: {success_rate:.1f}%")

        if success_rate < 90:
            print(f"\n💡 RECOMMENDATIONS:")
            print(f"   • Check failed files manually for unusual PHP syntax")
            print(f"   • Some files might need manual conversion")
            print(f"   • Consider creating issue on GitHub with sample failed files")

def main():
    try:
        converter = RobustPHPToJSONConverter()
        converter.run_robust()
    except KeyboardInterrupt:
        print("\n⚠️ Stopped by user")
    except Exception as e:
        print(f"❌ Critical error: {e}")

if __name__ == "__main__":
    main()
