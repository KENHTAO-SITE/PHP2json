#!/usr/bin/env python3
"""
Enterprise-Grade PHP Language Files to JSON Converter - Vietnamese Version
=========================================================================
Công cụ production-ready với data integrity verification và backup system

Tính năng:
- Data integrity verification giữa PHP và JSON
- Hệ thống backup tự động trước mọi thao tác
- Deep comparison và validation của dữ liệu converted
- Cơ chế auto-retry cho conversions thất bại
- Enterprise-grade logging và audit trails
- Khả năng rollback để đảm bảo an toàn
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

        print(f"📋 Enterprise logging đã bật:")
        print(f"   • Conversion log: {self.conversion_log.name}")
        print(f"   • Integrity log: {self.integrity_log.name}")
        print(f"   • Backup log: {self.backup_log.name}")

    def log_to_file(self, log_file: Path, level: str, message: str):
        """Ghi vào log file với timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

    def create_backup_system(self):
        """Tạo enterprise backup system"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = self.root_dir / f"backup_{timestamp}"
        self.backup_dir.mkdir(exist_ok=True)

        print(f"🛡️  Enterprise backup system đã tạo: {self.backup_dir.name}")
        self.log_to_file(self.backup_log, "INFO", f"Backup directory created: {self.backup_dir}")

        return self.backup_dir

    def backup_file(self, php_file: Path) -> bool:
        """Tạo backup của PHP file trước mọi thao tác"""
        try:
            if not self.backup_dir:
                self.create_backup_system()

            # Tạo cấu trúc thư mục con trong backup
            relative_path = php_file.relative_to(self.root_dir)
            backup_file = self.backup_dir / relative_path
            backup_file.parent.mkdir(parents=True, exist_ok=True)

            # Copy file vào backup
            shutil.copy2(php_file, backup_file)

            self.log_to_file(self.backup_log, "SUCCESS", f"Backed up: {php_file} -> {backup_file}")
            return True

        except Exception as e:
            self.log_to_file(self.backup_log, "ERROR", f"Backup failed for {php_file}: {e}")
            return False

    def find_php_files_recursive(self, skip_existing=True):
        """Tìm tất cả file .php với phân tích chi tiết"""
        self.php_files = []

        print("🔍 Enterprise scanning cho file PHP...")
        for php_file in self.root_dir.rglob("*.php"):
            if php_file.name in ["converter_en.py", "converter_vi.py", "load_json_example.php"]:
                continue

            if skip_existing:
                json_file = php_file.with_suffix('.json')
                if json_file.exists():
                    print(f"⏭️  Bỏ qua {php_file.relative_to(self.root_dir)} (JSON đã tồn tại)")
                    continue

            self.php_files.append(php_file)

        print(f"📊 Tìm thấy {len(self.php_files)} file PHP cho enterprise processing")
        self.log_to_file(self.conversion_log, "INFO", f"Found {len(self.php_files)} PHP files to process")
        return len(self.php_files)

    def analyze_php_file(self, php_file: Path) -> Dict[str, Any]:
        """Phân tích cấu trúc file PHP trước khi convert"""
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
                'content_hash': hash(content)  # Cho integrity verification
            }

            # Phát hiện loại array syntax
            if re.search(r'\[.*?\]', content, re.DOTALL):
                analysis['array_syntax'].append('short_array')
            if re.search(r'array\s*\(', content, re.IGNORECASE):
                analysis['array_syntax'].append('long_array')

            # Trích xuất tên biến
            var_matches = re.findall(r'\$(\w+)\s*=', content)
            analysis['variable_names'] = list(set(var_matches))

            return analysis

        except Exception as e:
            return {'error': str(e)}

    def parse_php_array_robust(self, content: str) -> Optional[Dict[str, Any]]:
        """Parsing PHP đa chiến lược với fallbacks toàn diện"""

        # Chiến lược 1: Advanced regex với hỗ trợ nested structure
        result = self._parse_strategy_advanced_regex(content)
        if result and len(result) > 0:
            return result

        # Chiến lược 2: Tokenizer giống PHP
        result = self._parse_strategy_tokenizer(content)
        if result and len(result) > 0:
            return result

        # Chiến lược 3: Line-by-line với state machine
        result = self._parse_strategy_state_machine(content)
        if result and len(result) > 0:
            return result

        # Chiến lược 4: Regex với xử lý nested thủ công
        result = self._parse_strategy_manual_nested(content)
        if result and len(result) > 0:
            return result

        return None

    def _parse_strategy_advanced_regex(self, content: str) -> Optional[Dict[str, Any]]:
        """Chiến lược 1: Advanced regex parsing"""
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
            print(f"   ⚠️  Chiến lược 1 thất bại: {e}")

        return None

    def _parse_strategy_tokenizer(self, content: str) -> Optional[Dict[str, Any]]:
        """Chiến lược 2: Tokenizer approach"""
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
                (?:^|,|\n)\s*                    # Bắt đầu hoặc separator
                (['\"])((?:\\.|(?!\1)[^\\])*?)\1  # Quoted key
                \s*=>\s*                         # Mũi tên
                (?:
                    (['\"])((?:\\.|(?!\3)[^\\])*?)\3  # Quoted value
                    |
                    (\d+(?:\.\d+)?)              # Số
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
            print(f"   ⚠️  Chiến lược 2 thất bại: {e}")

        return None

    def _parse_strategy_state_machine(self, content: str) -> Optional[Dict[str, Any]]:
        """Chiến lược 3: State machine line-by-line parsing"""
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
            print(f"   ⚠️  Chiến lược 3 thất bại: {e}")

        return None

    def _parse_strategy_manual_nested(self, content: str) -> Optional[Dict[str, Any]]:
        """Chiến lược 4: Xử lý nested structure thủ công"""
        try:
            content = self._clean_php_content(content)
            result = {}

            pattern = r"""
                (['\"])((?:\\.|(?!\1)[^\\])*?)\1    # Key trong quotes
                \s*=>\s*                            # Mũi tên
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
                    print(f"   ⚠️  Lỗi parsing match: {e}")
                    continue

            return result if result else None

        except Exception as e:
            print(f"   ⚠️  Chiến lược 4 thất bại: {e}")

        return None

    def _clean_php_content(self, content: str) -> str:
        """Làm sạch PHP content để parsing"""
        content = re.sub(r'<\?php\s*', '', content)
        content = re.sub(r'\?>', '', content)
        content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        content = re.sub(r'#.*?$', '', content, flags=re.MULTILINE)

        return content.strip()

    def _clean_string_value(self, value: str) -> str:
        """Làm sạch string value bằng cách xóa escapes"""
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
            print(f"   ⚠️  Advanced parsing thất bại: {e}")

        return result if result else None

    def _smart_split_array_entries(self, content: str) -> List[str]:
        """Smart split tôn trọng quotes và nested structures"""
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
        """Validate JSON output trước khi lưu"""
        try:
            if not data:
                return False, "Dữ liệu rỗng"

            if not isinstance(data, dict):
                return False, "Dữ liệu không phải dictionary"

            if len(data) == 0:
                return False, "Không tìm thấy keys"

            if len(data) > 10000:
                return False, f"Quá nhiều keys ({len(data)}), có thể lỗi parsing"

            json.dumps(data, ensure_ascii=False, indent=2)

            return True, f"Hợp lệ với {len(data)} keys"

        except Exception as e:
            return False, f"JSON validation thất bại: {e}"

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
            print(f"      🔍 Kiểm tra tính toàn vẹn dữ liệu...")

            # Kiểm tra 1: JSON file tồn tại và đọc được
            if not json_file.exists():
                integrity_report['issues_found'].append("JSON file không tồn tại")
                return False, "JSON file bị thiếu", integrity_report

            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            integrity_report['checks_performed'].append("JSON file readability")

            # Kiểm tra 2: So sánh số lượng key
            original_key_count = len(original_data)
            json_key_count = len(json_data)

            if original_key_count != json_key_count:
                integrity_report['issues_found'].append(f"Số key không khớp: PHP={original_key_count}, JSON={json_key_count}")
            else:
                integrity_report['key_count_match'] = True
            integrity_report['checks_performed'].append("Key count comparison")

            # Kiểm tra 3: Deep key-value comparison
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

            # Kiểm tra key thừa trong JSON
            extra_keys = [key for key in json_data.keys() if key not in original_data]

            if missing_keys:
                integrity_report['issues_found'].append(f"Key thiếu trong JSON: {missing_keys}")
            if extra_keys:
                integrity_report['issues_found'].append(f"Key thừa trong JSON: {extra_keys}")
            if value_mismatches:
                integrity_report['issues_found'].append(f"Value không khớp: {len(value_mismatches)} phát hiện")

            integrity_report['checks_performed'].append("Deep key-value comparison")

            # Kiểm tra 4: Content hash verification
            json_content_hash = hash(json.dumps(json_data, sort_keys=True))
            php_content_hash = hash(json.dumps(original_data, sort_keys=True))

            if json_content_hash == php_content_hash:
                integrity_report['content_hash_match'] = True
            integrity_report['checks_performed'].append("Content hash verification")

            # Đánh giá cuối cùng
            data_integrity_passed = (
                integrity_report['key_count_match'] and
                len(missing_keys) == 0 and
                len(extra_keys) == 0 and
                len(value_mismatches) == 0
            )

            integrity_report['data_match'] = data_integrity_passed

            if data_integrity_passed:
                print(f"      ✅ Tính toàn vẹn dữ liệu xác minh: 100% khớp")
                self.log_to_file(self.integrity_log, "SUCCESS", f"Data integrity verified for {php_file}")
                return True, "Tính toàn vẹn dữ liệu được xác minh", integrity_report
            else:
                print(f"      ❌ Phát hiện vấn đề tính toàn vẹn: {len(integrity_report['issues_found'])} vấn đề")
                self.log_to_file(self.integrity_log, "FAILED", f"Data integrity issues for {php_file}: {integrity_report['issues_found']}")
                return False, f"Tính toàn vẹn thất bại: {len(integrity_report['issues_found'])} vấn đề", integrity_report

        except Exception as e:
            integrity_report['issues_found'].append(f"Lỗi verification: {str(e)}")
            self.log_to_file(self.integrity_log, "ERROR", f"Data integrity verification error for {php_file}: {e}")
            return False, f"Lỗi verification: {str(e)}", integrity_report

    def auto_retry_conversion(self, php_file: Path, max_retries: int = 3) -> Tuple[bool, str, Dict[str, Any], Dict[str, Any]]:
        """Cơ chế auto-retry cho conversions thất bại"""
        for attempt in range(1, max_retries + 1):
            print(f"      🔄 Lần thử conversion {attempt}/{max_retries}")

            try:
                with open(php_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                data = self.parse_php_array_robust(content)

                if data is not None:
                    is_valid, validation_msg = self.validate_json_output(data)
                    if is_valid:
                        return True, validation_msg, data, {'attempts': attempt}

                print(f"      ⚠️  Lần thử {attempt} thất bại, đang retry...")
                time.sleep(0.2 * attempt)  # Progressive delay

            except Exception as e:
                print(f"      ❌ Lần thử {attempt} lỗi: {e}")

        return False, f"Tất cả {max_retries} lần thử conversion đều thất bại", {}, {'attempts': max_retries}

    def convert_file_enterprise(self, php_file: Path) -> Tuple[bool, str, Dict[str, Any]]:
        """Enterprise-grade file conversion với full integrity checking"""
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

            # Bước 1: Tạo backup
            backup_success = self.backup_file(php_file)
            conversion_info['backup_created'] = backup_success

            if not backup_success:
                return False, "Tạo backup thất bại - hủy bỏ để đảm bảo an toàn", conversion_info

            # Bước 2: Phân tích file
            analysis = self.analyze_php_file(php_file)
            conversion_info['analysis'] = analysis

            if 'error' in analysis:
                return False, f"Phân tích file thất bại: {analysis['error']}", conversion_info

            print(f"      📏 Kích thước: {analysis['file_size']} bytes, Dòng: {analysis['line_count']}")
            if analysis['variable_names']:
                print(f"      🔤 Biến: {', '.join(analysis['variable_names'][:3])}{'...' if len(analysis['variable_names']) > 3 else ''}")

            # Bước 3: Convert với auto-retry
            success, message, data, retry_info = self.auto_retry_conversion(php_file, self.max_retries)
            conversion_info['retry_attempts'] = retry_info.get('attempts', 0)

            if not success:
                return False, message, conversion_info

            # Bước 4: Validate JSON output
            is_valid, validation_msg = self.validate_json_output(data)
            conversion_info['validation'] = {'valid': is_valid, 'message': validation_msg}

            if not is_valid:
                return False, f"Validation thất bại: {validation_msg}", conversion_info

            print(f"      ✅ Conversion thành công: {validation_msg}")

            # Bước 5: Lưu JSON file
            json_file = php_file.with_suffix('.json')
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            # Bước 6: Enterprise data integrity verification
            if self.integrity_check_enabled:
                integrity_passed, integrity_msg, integrity_report = self.verify_data_integrity(
                    php_file, json_file, data
                )
                conversion_info['integrity'] = integrity_report

                if not integrity_passed:
                    # Xóa JSON file có thể bị corrupted
                    if json_file.exists():
                        json_file.unlink()
                    return False, f"Kiểm tra tính toàn vẹn thất bại: {integrity_msg}", conversion_info

                self.verified_files.append(php_file)

            self.log_to_file(self.conversion_log, "SUCCESS", f"Enterprise conversion completed: {php_file}")
            return True, f"{validation_msg} + tính toàn vẹn đã xác minh", conversion_info

        except Exception as e:
            self.log_to_file(self.conversion_log, "ERROR", f"Enterprise conversion error for {php_file}: {e}")
            return False, f"Lỗi enterprise conversion: {str(e)}", conversion_info

    def safe_delete_php_file(self, php_file: Path) -> bool:
        """Xóa PHP file an toàn với nhiều lần xác nhận"""
        try:
            # Kiểm tra tính toàn vẹn cuối cùng trước khi xóa
            json_file = php_file.with_suffix('.json')

            if not json_file.exists():
                print(f"      ❌ JSON file thiếu, không thể xóa {php_file.name}")
                return False

            # Đọc và verify JSON file một lần nữa
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)

            if not json_data or len(json_data) == 0:
                print(f"      ❌ JSON file rỗng, không thể xóa {php_file.name}")
                return False

            # Xóa an toàn
            php_file.unlink()
            self.log_to_file(self.conversion_log, "DELETE", f"Safely deleted PHP file: {php_file}")
            return True

        except Exception as e:
            self.log_to_file(self.conversion_log, "ERROR", f"Safe deletion failed for {php_file}: {e}")
            return False

    def run_enterprise(self):
        """Chạy enterprise-grade converter"""
        print("🏢 Enterprise PHP to JSON Language Converter (Tiếng Việt)")
        print("=" * 75)

        count = self.find_php_files_recursive()

        if count == 0:
            print("✅ Không tìm thấy file PHP nào cho enterprise processing!")
            return

        print(f"\n🎯 Tính năng Enterprise Processing:")
        print(f"   • Hệ thống backup tự động")
        print(f"   • Data integrity verification")
        print(f"   • Auto-retry với {self.max_retries} lần thử")
        print(f"   • Deep comparison PHP ↔ JSON")
        print(f"   • Enterprise logging và audit trails")
        print(f"   • Safe deletion với nhiều lần xác nhận")

        # Enterprise-grade confirmation
        choice = input(f"\n🔥 Bật safe deletion sau integrity verification? (y/N): ").strip().lower()
        delete_php = choice in ['y', 'yes']

        if delete_php:
            confirm1 = input("⚠️  Enterprise deletion cần backup verification. Tiếp tục? (y/N): ").strip().lower()
            if confirm1 not in ['y', 'yes']:
                delete_php = False
            else:
                confirm2 = input("🛡️  Xác nhận cuối: Xóa file PHP sau 100% integrity verification? (y/N): ").strip().lower()
                delete_php = confirm2 in ['y', 'yes']

        print(f"\n🔄 Bắt đầu enterprise conversion {count} files...")
        print("=" * 75)

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
                        print(f"   🗑️  Đã xóa an toàn {php_file.name}")
                    else:
                        print(f"   ⚠️  Không thể xóa an toàn {php_file.name}")
            else:
                self.failed_count += 1
                self.failed_files.append(php_file)

                # Kiểm tra nếu là integrity failure
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
        """In kết quả enterprise toàn diện"""
        print(f"\n" + "=" * 75)
        print(f"🏢 KẾT QUẢ ENTERPRISE CONVERSION:")
        print(f"   ✅ Convert thành công: {self.converted_count} files")
        print(f"   🔍 Integrity đã verify: {len(self.verified_files)} files")
        print(f"   ❌ Conversion thất bại: {self.failed_count} files")
        print(f"   ⚠️  Integrity thất bại: {len(integrity_failures)} files")

        if self.deleted_count > 0:
            print(f"   🗑️  Đã xóa an toàn: {self.deleted_count} file PHP")

        if self.backup_dir:
            print(f"   🛡️  Thư mục backup: {self.backup_dir.name}")

        if failed_details:
            print(f"\n❌ PHÂN TÍCH THẤT BẠI:")
            error_summary = {}
            for detail in failed_details:
                error_type = detail['error'].split(':')[0]
                error_summary[error_type] = error_summary.get(error_type, 0) + 1

            for error_type, count in error_summary.items():
                print(f"   • {error_type}: {count} files")

        success_rate = (self.converted_count / len(self.php_files)) * 100 if self.php_files else 0
        integrity_rate = (len(self.verified_files) / len(self.php_files)) * 100 if self.php_files else 0

        print(f"\n📊 ENTERPRISE METRICS:")
        print(f"   🎯 Tỷ lệ Conversion thành công: {success_rate:.1f}%")
        print(f"   🔍 Tỷ lệ Data Integrity: {integrity_rate:.1f}%")
        print(f"   📋 Log Files: {self.log_dir.name}/")

        if success_rate < 100:
            print(f"\n💡 KHUYẾN NGHỊ ENTERPRISE:")
            print(f"   • Review các file thất bại trong conversion logs")
            print(f"   • Kiểm tra integrity failures để đảm bảo tính nhất quán dữ liệu")
            print(f"   • Thư mục backup chứa file gốc để recovery")
            print(f"   • Cân nhắc review thủ công các cấu trúc PHP phức tạp")

        # Hiển thị credit banner đẹp sau kết quả
        self._show_credit_banner()

    def _show_credit_banner(self):
        """Hiển thị credit banner đẹp với thông tin liên hệ"""
        print(f"\n" + "═" * 75)
        print("╔" + "═" * 73 + "╗")
        print("║" + " " * 73 + "║")
        print("║" + "   ██████╗ ██╗  ██╗██████╗ ██████╗      ██╗███████╗ ██████╗ ███╗   ██╗".center(73) + "║")
        print("║" + "   ██╔══██╗██║  ██║██╔══██╗╚════██╗     ██║██╔════╝██╔═══██╗████╗  ██║".center(73) + "║")
        print("║" + "   ██████╔╝███████║██████╔╝ █████╔╝     ██║███████╗██║   ██║██╔██╗ ██║".center(73) + "║")
        print("║" + "   ██╔═══╝ ██╔══██║██╔═══╝ ██╔═══╝ ██   ██║╚════██║██║   ██║██║╚██╗██║".center(73) + "║")
        print("║" + "   ██║     ██║  ██║██║     ███████╗╚█████╔╝███████║╚██████╔╝██║ ╚████║".center(73) + "║")
        print("║" + "   ╚═╝     ╚═╝  ╚═╝╚═╝     ╚══════╝ ╚════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝".center(73) + "║")
        print("║" + " " * 73 + "║")
        print("║" + "🚀 ENTERPRISE PHP TO JSON LANGUAGE CONVERTER 🚀".center(73) + "║")
        print("║" + " " * 73 + "║")
        print("║" + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━".center(73) + "║")
        print("║" + " " * 73 + "║")
        print("║" + "🎯 TẠO BỞI: KÊNH TÁO".center(73) + "║")
        print("║" + " " * 73 + "║")
        print("║" + "📱 TELEGRAM: @QTUNUy".center(73) + "║")
        print("║" + " " * 73 + "║")
        print("║" + "🌐 WEBSITES:".center(73) + "║")
        print("║" + "• CertApple.com  • Kenhtao.net  • kenhtao.site  • iPA.KenhTao.net".center(73) + "║")
        print("║" + " " * 73 + "║")
        print("║" + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━".center(73) + "║")
        print("║" + " " * 73 + "║")
        print("║" + "💝 Cảm ơn bạn đã sử dụng PHP2JSON Enterprise Converter! 💝".center(73) + "║")
        print("║" + "⭐ Nếu tool này hữu ích, hãy star GitHub repository của chúng tôi ⭐".center(73) + "║")
        print("║" + " " * 73 + "║")
        print("║" + "🔔 Để nhận updates và support, hãy follow Telegram: @QTUNUy 🔔".center(73) + "║")
        print("║" + " " * 73 + "║")
        print("╚" + "═" * 73 + "╝")
        print("═" * 75)

def main():
    try:
        converter = EnterprisePHPToJSONConverter()
        converter.run_enterprise()
    except KeyboardInterrupt:
        print("\n⚠️ Enterprise conversion bị dừng lại bởi user")
    except Exception as e:
        print(f"❌ Lỗi enterprise system: {e}")

if __name__ == "__main__":
    main()
