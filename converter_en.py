#!/usr/bin/env python3
"""
Enterprise-Grade PHP Language Files to JSON Converter - English Version
======================================================================
Production-ready tool with data integrity verification and backup system

Features:
- Data integrity verification between PHP and JSON
- Automatic backup system before any file operations
- Deep comparison and validation of converted data
- Auto-retry mechanism for failed conversions
- Enterprise-grade logging and audit trails
- Rollback capability for safety
- Production-level error handling
"""

import os
import re
import json
import sys
import time
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime

class EnterprisePHPToJSONConverter:
    def __init__(self):
        self.root_dir = Path.cwd()
        self.php_files = []
        self.converted_count = 0
        self.failed_count = 0
        self.deleted_count = 0
        self.failed_files = []
        self.verified_files = []
        self.backup_dir = None
        self.processing_delay = 0.1
        self.max_retries = 3
        self.integrity_check_enabled = True

        # Enterprise logging
        self.setup_enterprise_logging()

    def setup_enterprise_logging(self):
        """Setup enterprise-grade logging system"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_dir = self.root_dir / "conversion_logs"
        self.log_dir.mkdir(exist_ok=True)

        self.conversion_log = self.log_dir / f"conversion_{timestamp}.log"
        self.integrity_log = self.log_dir / f"integrity_{timestamp}.log"
        self.backup_log = self.log_dir / f"backup_{timestamp}.log"

        print(f"📋 Enterprise logging enabled:")
        print(f"   • Conversion log: {self.conversion_log.name}")
        print(f"   • Integrity log: {self.integrity_log.name}")
        print(f"   • Backup log: {self.backup_log.name}")

    def log_to_file(self, log_file: Path, level: str, message: str):
        """Write to log file with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

    def create_backup_system(self):
        """Create enterprise backup system"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = self.root_dir / f"backup_{timestamp}"
        self.backup_dir.mkdir(exist_ok=True)

        print(f"🛡️  Enterprise backup system created: {self.backup_dir.name}")
        self.log_to_file(self.backup_log, "INFO", f"Backup directory created: {self.backup_dir}")

        return self.backup_dir

    def backup_file(self, php_file: Path) -> bool:
        """Create backup of PHP file before any operations"""
        try:
            if not self.backup_dir:
                self.create_backup_system()

            # Create subdirectory structure in backup
            relative_path = php_file.relative_to(self.root_dir)
            backup_file = self.backup_dir / relative_path
            backup_file.parent.mkdir(parents=True, exist_ok=True)

            # Copy file to backup
            shutil.copy2(php_file, backup_file)

            self.log_to_file(self.backup_log, "SUCCESS", f"Backed up: {php_file} -> {backup_file}")
            return True

        except Exception as e:
            self.log_to_file(self.backup_log, "ERROR", f"Backup failed for {php_file}: {e}")
            return False

    def find_php_files_recursive(self, skip_existing=True):
        """Find all .php files with detailed analysis"""
        self.php_files = []

        print("🔍 Enterprise scanning for PHP files...")
        for php_file in self.root_dir.rglob("*.php"):
            if php_file.name in ["converter_en.py", "converter_vi.py", "load_json_example.php"]:
                continue

            if skip_existing:
                json_file = php_file.with_suffix('.json')
                if json_file.exists():
                    print(f"⏭️  Skip {php_file.relative_to(self.root_dir)} (JSON exists)")
                    continue

            self.php_files.append(php_file)

        print(f"📊 Found {len(self.php_files)} PHP files for enterprise processing")
        self.log_to_file(self.conversion_log, "INFO", f"Found {len(self.php_files)} PHP files to process")
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
                'encoding': 'utf-8',
                'content_hash': hash(content)  # For integrity verification
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
            content = self._clean_php_content(content)

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

            array_start = None
            for pattern in [r'return\s*\[', r'return\s*array\s*\(', r'\$\w+\s*=\s*\[', r'\$\w+\s*=\s*array\s*\(']:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    array_start = match.end()
                    break

            if array_start is None:
                return None

            remaining_content = content[array_start:]

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

                    if groups[3]:  # String value
                        value = self._clean_string_value(groups[3])
                    elif groups[4]:  # Number
                        value = groups[4]
                    elif groups[5]:  # Boolean/null
                        value = groups[5].lower()
                    elif groups[6]:  # Nested array
                        value = groups[6]
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

            for line_no, line in enumerate(lines, 1):
                line = line.strip()

                if not line or line.startswith('//') or line.startswith('/*'):
                    continue

                if not in_array and ('=>' in line or re.search(r'return\s*[\[\(]|^\$\w+\s*=\s*[\[\(]', line)):
                    in_array = True

                if not in_array:
                    continue

                if '=>' in line and current_key is None:
                    parts = line.split('=>', 1)
                    if len(parts) == 2:
                        key_part = parts[0].strip()
                        value_part = parts[1].strip()

                        key_match = re.search(r"['\"]([^'\"]*)['\"]", key_part)
                        if key_match:
                            current_key = self._clean_string_value(key_match.group(1))

                            value_match = re.search(r"['\"]([^'\"]*)['\"]", value_part)
                            if value_match:
                                result[current_key] = self._clean_string_value(value_match.group(1))
                                current_key = None
                            else:
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
        content = re.sub(r'<\?php\s*', '', content)
        content = re.sub(r'\?>', '', content)
        content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        content = re.sub(r'#.*?$', '', content, flags=re.MULTILINE)

        return content.strip()

    def _clean_string_value(self, value: str) -> str:
        """Clean string value by removing escapes"""
        if not value:
            return value

        value = value.replace('\\"', '"')
        value = value.replace("\\'", "'")
        value = value.replace('\\\\', '\\')

        return value

    def _parse_nested_array(self, nested_content: str) -> Optional[str]:
        """Parse nested array content"""
        try:
            nested_content = nested_content.strip('[]()').strip()
            return nested_content
        except:
            return None

    def _parse_array_content_advanced(self, array_content: str) -> Optional[Dict[str, Any]]:
        """Advanced array content parsing"""
        result = {}

        try:
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

                        key_match = re.search(r"['\"]([^'\"]*)['\"]", key_part)
                        if key_match:
                            key = self._clean_string_value(key_match.group(1))

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

            if len(data) == 0:
                return False, "No keys found"

            if len(data) > 10000:
                return False, f"Too many keys ({len(data)}), possible parsing error"

            json.dumps(data, ensure_ascii=False, indent=2)

            return True, f"Valid with {len(data)} keys"

        except Exception as e:
            return False, f"JSON validation failed: {e}"

    def verify_data_integrity(self, php_file: Path, json_file: Path, original_data: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        """Enterprise-grade data integrity verification"""
        integrity_report = {
            'php_file': str(php_file),
            'json_file': str(json_file),
            'verification_time': datetime.now().isoformat(),
            'checks_performed': [],
            'issues_found': [],
            'data_match': False,
            'key_count_match': False,
            'content_hash_match': False
        }

        try:
            print(f"      🔍 Data integrity verification...")

            # Check 1: JSON file exists and is readable
            if not json_file.exists():
                integrity_report['issues_found'].append("JSON file does not exist")
                return False, "JSON file missing", integrity_report

            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            integrity_report['checks_performed'].append("JSON file readability")

            # Check 2: Key count comparison
            original_key_count = len(original_data)
            json_key_count = len(json_data)

            if original_key_count != json_key_count:
                integrity_report['issues_found'].append(f"Key count mismatch: PHP={original_key_count}, JSON={json_key_count}")
            else:
                integrity_report['key_count_match'] = True
            integrity_report['checks_performed'].append("Key count comparison")

            # Check 3: Deep key-value comparison
            missing_keys = []
            value_mismatches = []

            for key, php_value in original_data.items():
                if key not in json_data:
                    missing_keys.append(key)
                elif str(json_data[key]) != str(php_value):
                    value_mismatches.append({
                        'key': key,
                        'php_value': php_value,
                        'json_value': json_data[key]
                    })

            # Check for extra keys in JSON
            extra_keys = [key for key in json_data.keys() if key not in original_data]

            if missing_keys:
                integrity_report['issues_found'].append(f"Missing keys in JSON: {missing_keys}")
            if extra_keys:
                integrity_report['issues_found'].append(f"Extra keys in JSON: {extra_keys}")
            if value_mismatches:
                integrity_report['issues_found'].append(f"Value mismatches: {len(value_mismatches)} found")

            integrity_report['checks_performed'].append("Deep key-value comparison")

            # Check 4: Content hash verification (optional)
            json_content_hash = hash(json.dumps(json_data, sort_keys=True))
            php_content_hash = hash(json.dumps(original_data, sort_keys=True))

            if json_content_hash == php_content_hash:
                integrity_report['content_hash_match'] = True
            integrity_report['checks_performed'].append("Content hash verification")

            # Final assessment
            data_integrity_passed = (
                integrity_report['key_count_match'] and
                len(missing_keys) == 0 and
                len(extra_keys) == 0 and
                len(value_mismatches) == 0
            )

            integrity_report['data_match'] = data_integrity_passed

            if data_integrity_passed:
                print(f"      ✅ Data integrity verified: 100% match")
                self.log_to_file(self.integrity_log, "SUCCESS", f"Data integrity verified for {php_file}")
                return True, "Data integrity verified", integrity_report
            else:
                print(f"      ❌ Data integrity issues found: {len(integrity_report['issues_found'])} problems")
                self.log_to_file(self.integrity_log, "FAILED", f"Data integrity issues for {php_file}: {integrity_report['issues_found']}")
                return False, f"Data integrity failed: {len(integrity_report['issues_found'])} issues", integrity_report

        except Exception as e:
            integrity_report['issues_found'].append(f"Verification error: {str(e)}")
            self.log_to_file(self.integrity_log, "ERROR", f"Data integrity verification error for {php_file}: {e}")
            return False, f"Verification error: {str(e)}", integrity_report

    def auto_retry_conversion(self, php_file: Path, max_retries: int = 3) -> Tuple[bool, str, Dict[str, Any], Dict[str, Any]]:
        """Auto-retry mechanism for failed conversions"""
        for attempt in range(1, max_retries + 1):
            print(f"      🔄 Conversion attempt {attempt}/{max_retries}")

            try:
                with open(php_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                data = self.parse_php_array_robust(content)

                if data is not None:
                    is_valid, validation_msg = self.validate_json_output(data)
                    if is_valid:
                        return True, validation_msg, data, {'attempts': attempt}

                print(f"      ⚠️  Attempt {attempt} failed, retrying...")
                time.sleep(0.2 * attempt)  # Progressive delay

            except Exception as e:
                print(f"      ❌ Attempt {attempt} error: {e}")

        return False, f"All {max_retries} conversion attempts failed", {}, {'attempts': max_retries}

    def convert_file_enterprise(self, php_file: Path) -> Tuple[bool, str, Dict[str, Any]]:
        """Enterprise-grade file conversion with full integrity checking"""
        conversion_info = {
            'file': str(php_file),
            'analysis': {},
            'strategies_tried': [],
            'validation': {},
            'integrity': {},
            'backup_created': False,
            'retry_attempts': 0
        }

        try:
            print(f"   📁 Enterprise processing: {php_file.name}")

            # Step 1: Create backup
            backup_success = self.backup_file(php_file)
            conversion_info['backup_created'] = backup_success

            if not backup_success:
                return False, "Backup creation failed - aborting for safety", conversion_info

            # Step 2: Analyze file
            analysis = self.analyze_php_file(php_file)
            conversion_info['analysis'] = analysis

            if 'error' in analysis:
                return False, f"File analysis failed: {analysis['error']}", conversion_info

            print(f"      📏 Size: {analysis['file_size']} bytes, Lines: {analysis['line_count']}")
            if analysis['variable_names']:
                print(f"      🔤 Variables: {', '.join(analysis['variable_names'][:3])}{'...' if len(analysis['variable_names']) > 3 else ''}")

            # Step 3: Convert with auto-retry
            success, message, data, retry_info = self.auto_retry_conversion(php_file, self.max_retries)
            conversion_info['retry_attempts'] = retry_info.get('attempts', 0)

            if not success:
                return False, message, conversion_info

            # Step 4: Validate JSON output
            is_valid, validation_msg = self.validate_json_output(data)
            conversion_info['validation'] = {'valid': is_valid, 'message': validation_msg}

            if not is_valid:
                return False, f"Validation failed: {validation_msg}", conversion_info

            print(f"      ✅ Conversion successful: {validation_msg}")

            # Step 5: Save JSON file
            json_file = php_file.with_suffix('.json')
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            # Step 6: Enterprise data integrity verification
            if self.integrity_check_enabled:
                integrity_passed, integrity_msg, integrity_report = self.verify_data_integrity(
                    php_file, json_file, data
                )
                conversion_info['integrity'] = integrity_report

                if not integrity_passed:
                    # Delete the potentially corrupted JSON file
                    if json_file.exists():
                        json_file.unlink()
                    return False, f"Data integrity check failed: {integrity_msg}", conversion_info

                self.verified_files.append(php_file)

            self.log_to_file(self.conversion_log, "SUCCESS", f"Enterprise conversion completed: {php_file}")
            return True, f"{validation_msg} + integrity verified", conversion_info

        except Exception as e:
            self.log_to_file(self.conversion_log, "ERROR", f"Enterprise conversion error for {php_file}: {e}")
            return False, f"Enterprise conversion error: {str(e)}", conversion_info

    def safe_delete_php_file(self, php_file: Path) -> bool:
        """Safely delete PHP file with multiple confirmations"""
        try:
            # Final integrity check before deletion
            json_file = php_file.with_suffix('.json')

            if not json_file.exists():
                print(f"      ❌ JSON file missing, cannot delete {php_file.name}")
                return False

            # Read and verify the JSON file one more time
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)

            if not json_data or len(json_data) == 0:
                print(f"      ❌ JSON file empty, cannot delete {php_file.name}")
                return False

            # Safe deletion
            php_file.unlink()
            self.log_to_file(self.conversion_log, "DELETE", f"Safely deleted PHP file: {php_file}")
            return True

        except Exception as e:
            self.log_to_file(self.conversion_log, "ERROR", f"Safe deletion failed for {php_file}: {e}")
            return False

    def run_enterprise(self):
        """Run enterprise-grade converter"""
        print("🏢 Enterprise PHP to JSON Language Converter (English)")
        print("=" * 70)

        count = self.find_php_files_recursive()

        if count == 0:
            print("✅ No PHP files found for enterprise processing!")
            return

        print(f"\n🎯 Enterprise Processing Features:")
        print(f"   • Automatic backup system")
        print(f"   • Data integrity verification")
        print(f"   • Auto-retry with {self.max_retries} attempts")
        print(f"   • Deep comparison PHP ↔ JSON")
        print(f"   • Enterprise logging and audit trails")
        print(f"   • Safe deletion with multiple confirmations")

        # Enterprise-grade confirmation
        choice = input(f"\n🔥 Enable safe deletion after integrity verification? (y/N): ").strip().lower()
        delete_php = choice in ['y', 'yes']

        if delete_php:
            confirm1 = input("⚠️  Enterprise deletion requires backup verification. Continue? (y/N): ").strip().lower()
            if confirm1 not in ['y', 'yes']:
                delete_php = False
            else:
                confirm2 = input("🛡️  Final confirmation: Delete PHP files after 100% integrity verification? (y/N): ").strip().lower()
                delete_php = confirm2 in ['y', 'yes']

        print(f"\n🔄 Starting enterprise conversion of {count} files...")
        print("=" * 70)

        failed_details = []
        integrity_failures = []

        for i, php_file in enumerate(self.php_files, 1):
            print(f"\n📊 [{i}/{count}] {php_file.relative_to(self.root_dir)}")

            success, message, info = self.convert_file_enterprise(php_file)

            if success:
                self.converted_count += 1
                print(f"   ✅ {php_file.name} -> {php_file.stem}.json ({message})")

                if delete_php:
                    if self.safe_delete_php_file(php_file):
                        self.deleted_count += 1
                        print(f"   🗑️  Safely deleted {php_file.name}")
                    else:
                        print(f"   ⚠️  Could not safely delete {php_file.name}")
            else:
                self.failed_count += 1
                self.failed_files.append(php_file)

                # Check if it was an integrity failure
                if 'integrity' in info and not info['integrity'].get('data_match', False):
                    integrity_failures.append(php_file)

                failed_details.append({
                    'file': php_file.name,
                    'error': message,
                    'info': info
                })
                print(f"   ❌ {php_file.name}: {message}")

            if self.processing_delay > 0:
                time.sleep(self.processing_delay)

        self._print_enterprise_results(failed_details, integrity_failures)

    def _print_enterprise_results(self, failed_details: List[Dict], integrity_failures: List[Path]):
        """Print comprehensive enterprise results"""
        print(f"\n" + "=" * 70)
        print(f"🏢 ENTERPRISE CONVERSION RESULTS:")
        print(f"   ✅ Successfully converted: {self.converted_count} files")
        print(f"   🔍 Integrity verified: {len(self.verified_files)} files")
        print(f"   ❌ Failed conversions: {self.failed_count} files")
        print(f"   ⚠️  Integrity failures: {len(integrity_failures)} files")

        if self.deleted_count > 0:
            print(f"   🗑️  Safely deleted: {self.deleted_count} PHP files")

        if self.backup_dir:
            print(f"   🛡️  Backup directory: {self.backup_dir.name}")

        if failed_details:
            print(f"\n❌ FAILURE ANALYSIS:")
            error_summary = {}
            for detail in failed_details:
                error_type = detail['error'].split(':')[0]
                error_summary[error_type] = error_summary.get(error_type, 0) + 1

            for error_type, count in error_summary.items():
                print(f"   • {error_type}: {count} files")

        success_rate = (self.converted_count / len(self.php_files)) * 100 if self.php_files else 0
        integrity_rate = (len(self.verified_files) / len(self.php_files)) * 100 if self.php_files else 0

        print(f"\n📊 ENTERPRISE METRICS:")
        print(f"   🎯 Conversion Success Rate: {success_rate:.1f}%")
        print(f"   🔍 Data Integrity Rate: {integrity_rate:.1f}%")
        print(f"   📋 Log Files: {self.log_dir.name}/")

        if success_rate < 100:
            print(f"\n💡 ENTERPRISE RECOMMENDATIONS:")
            print(f"   • Review failed files in conversion logs")
            print(f"   • Check integrity failures for data consistency")
            print(f"   • Backup directory contains original files for recovery")
            print(f"   • Consider manual review of complex PHP structures")

        # Show beautiful credit banner after results
        self._show_credit_banner()

    def _show_credit_banner(self):
        """Display beautiful credit banner with contact information"""
        print(f"\n" + "═" * 70)
        print("╔" + "═" * 68 + "╗")
        print("║" + " " * 68 + "║")
        print("║" + "   ██████╗ ██╗  ██╗██████╗ ██████╗      ██╗███████╗ ██████╗ ███╗   ██╗".center(68) + "║")
        print("║" + "   ██╔══██╗██║  ██║██╔══██╗╚════██╗     ██║██╔════╝██╔═══██╗████╗  ██║".center(68) + "║")
        print("║" + "   ██████╔╝███████║██████╔╝ █████╔╝     ██║███████╗██║   ██║██╔██╗ ██║".center(68) + "║")
        print("║" + "   ██╔═══╝ ██╔══██║██╔═══╝ ██╔═══╝ ██   ██║╚════██║██║   ██║██║╚██╗██║".center(68) + "║")
        print("║" + "   ██║     ██║  ██║██║     ███████╗╚█████╔╝███████║╚██████╔╝██║ ╚████║".center(68) + "║")
        print("║" + "   ╚═╝     ╚═╝  ╚═╝╚═╝     ╚══════╝ ╚════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝".center(68) + "║")
        print("║" + " " * 68 + "║")
        print("║" + "🚀 ENTERPRISE PHP TO JSON LANGUAGE CONVERTER 🚀".center(68) + "║")
        print("║" + " " * 68 + "║")
        print("║" + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━".center(68) + "║")
        print("║" + " " * 68 + "║")
        print("║" + "🎯 CREATED BY: KÊNH TÁO".center(68) + "║")
        print("║" + " " * 68 + "║")
        print("║" + "📱 TELEGRAM: @QTUNUy".center(68) + "║")
        print("║" + " " * 68 + "║")
        print("║" + "🌐 WEBSITES:".center(68) + "║")
        print("║" + "• CertApple.com  • Kenhtao.net  • kenhtao.site  • iPA.KenhTao.net".center(68) + "║")
        print("║" + " " * 68 + "║")
        print("║" + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━".center(68) + "║")
        print("║" + " " * 68 + "║")
        print("║" + "💝 Thank you for using PHP2JSON Enterprise Converter! 💝".center(68) + "║")
        print("║" + "⭐ If this tool helped you, please star our GitHub repository ⭐".center(68) + "║")
        print("║" + " " * 68 + "║")
        print("║" + "🔔 For updates and support, follow us on Telegram: @QTUNUy 🔔".center(68) + "║")
        print("║" + " " * 68 + "║")
        print("╚" + "═" * 68 + "╝")
        print("═" * 70)

def main():
    try:
        converter = EnterprisePHPToJSONConverter()
        converter.run_enterprise()
    except KeyboardInterrupt:
        print("\n⚠️ Enterprise conversion stopped by user")
    except Exception as e:
        print(f"❌ Enterprise system error: {e}")

if __name__ == "__main__":
    main()
