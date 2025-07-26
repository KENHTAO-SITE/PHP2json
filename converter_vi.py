#!/usr/bin/env python3
"""
Robust PHP Language Files to JSON Converter - Vietnamese Version
===============================================================
Công cụ cải tiến để chuyển đổi PHP sang JSON an toàn và toàn diện

Tính năng:
- Nhiều chiến lược parsing với fallbacks
- Logging lỗi chi tiết và validation
- Xử lý chậm hơn, an toàn hơn cho bộ file lớn
- Hỗ trợ cấu trúc PHP nâng cao
- Phân tích file toàn diện trước khi convert
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
        self.processing_delay = 0.1  # Delay nhỏ giữa các files để an toàn

    def find_php_files_recursive(self, skip_existing=True):
        """Tìm tất cả file .php với phân tích chi tiết"""
        self.php_files = []

        print("🔍 Đang quét thư mục tìm file PHP...")
        for php_file in self.root_dir.rglob("*.php"):
            if php_file.name in ["converter_en.py", "converter_vi.py", "load_json_example.php"]:
                continue

            if skip_existing:
                json_file = php_file.with_suffix('.json')
                if json_file.exists():
                    print(f"⏭️  Bỏ qua {php_file.relative_to(self.root_dir)} (JSON đã tồn tại)")
                    continue

            self.php_files.append(php_file)

        print(f"📊 Tìm thấy {len(self.php_files)} file PHP để xử lý")
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
                'encoding': 'utf-8'
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
            # Làm sạch content
            content = self._clean_php_content(content)

            # Mở rộng patterns cho các cấu trúc PHP khác nhau
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

            # Tìm điểm bắt đầu array
            array_start = None
            for pattern in [r'return\s*\[', r'return\s*array\s*\(', r'\$\w+\s*=\s*\[', r'\$\w+\s*=\s*array\s*\(']:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    array_start = match.end()
                    break

            if array_start is None:
                return None

            # Trích xuất key-value pairs với parsing tốt hơn
            remaining_content = content[array_start:]

            # Sử dụng regex cải tiến cho key-value extraction
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

                    # Xác định value
                    if groups[3]:  # String value
                        value = self._clean_string_value(groups[3])
                    elif groups[4]:  # Number
                        value = groups[4]
                    elif groups[5]:  # Boolean/null
                        value = groups[5].lower()
                    elif groups[6]:  # Nested array
                        value = groups[6]  # Giữ dưới dạng string tạm thời
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
            bracket_count = 0
            quote_char = None

            for line_no, line in enumerate(lines, 1):
                line = line.strip()

                if not line or line.startswith('//') or line.startswith('/*'):
                    continue

                # Bắt đầu array
                if not in_array and ('=>' in line or re.search(r'return\s*[\[\(]|^\$\w+\s*=\s*[\[\(]', line)):
                    in_array = True

                if not in_array:
                    continue

                # Xử lý dòng cho key-value pairs
                if '=>' in line and current_key is None:
                    parts = line.split('=>', 1)
                    if len(parts) == 2:
                        key_part = parts[0].strip()
                        value_part = parts[1].strip()

                        # Trích xuất key
                        key_match = re.search(r"['\"]([^'\"]*)['\"]", key_part)
                        if key_match:
                            current_key = self._clean_string_value(key_match.group(1))

                            # Trích xuất value
                            value_match = re.search(r"['\"]([^'\"]*)['\"]", value_part)
                            if value_match:
                                result[current_key] = self._clean_string_value(value_match.group(1))
                                current_key = None
                            else:
                                # Multi-line value có thể đang bắt đầu
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

            # Tìm tất cả top-level key-value pairs
            # Regex này xử lý nested structures bằng cách đếm brackets
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
                        # Thử parse nested array hoặc giữ dưới dạng string
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
        # Xóa PHP tags
        content = re.sub(r'<\?php\s*', '', content)
        content = re.sub(r'\?>', '', content)

        # Xóa comments (cải tiến)
        content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        content = re.sub(r'#.*?$', '', content, flags=re.MULTILINE)

        return content.strip()

    def _clean_string_value(self, value: str) -> str:
        """Làm sạch string value bằng cách xóa escapes"""
        if not value:
            return value

        # Xử lý escaped quotes
        value = value.replace('\\"', '"')
        value = value.replace("\\'", "'")
        value = value.replace('\\\\', '\\')

        return value

    def _parse_nested_array(self, nested_content: str) -> Optional[str]:
        """Parse nested array content"""
        # Tạm thời trả về dưới dạng formatted string
        # Có thể enhance để return actual nested dict
        try:
            # Làm sạch nested content
            nested_content = nested_content.strip('[]()').strip()
            return nested_content
        except:
            return None

    def _parse_array_content_advanced(self, array_content: str) -> Optional[Dict[str, Any]]:
        """Advanced array content parsing"""
        result = {}

        try:
            # Xử lý multi-line entries tốt hơn
            # Split bằng commas nhưng tôn trọng quotes và nested structures
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

                        # Trích xuất key
                        key_match = re.search(r"['\"]([^'\"]*)['\"]", key_part)
                        if key_match:
                            key = self._clean_string_value(key_match.group(1))

                            # Trích xuất value
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

            # Kiểm tra số lượng keys hợp lý
            if len(data) == 0:
                return False, "Không tìm thấy keys"

            if len(data) > 10000:  # Sanity check
                return False, f"Quá nhiều keys ({len(data)}), có thể lỗi parsing"

            # Test JSON serialization
            json.dumps(data, ensure_ascii=False, indent=2)

            return True, f"Hợp lệ với {len(data)} keys"

        except Exception as e:
            return False, f"JSON validation thất bại: {e}"

    def convert_file_robust(self, php_file: Path) -> Tuple[bool, str, Dict[str, Any]]:
        """Convert file PHP với robust error handling"""
        conversion_info = {
            'file': str(php_file),
            'analysis': {},
            'strategies_tried': [],
            'validation': {}
        }

        try:
            print(f"   📁 Đang xử lý: {php_file.name}")

            # Phân tích file trước
            analysis = self.analyze_php_file(php_file)
            conversion_info['analysis'] = analysis

            if 'error' in analysis:
                return False, f"Phân tích file thất bại: {analysis['error']}", conversion_info

            print(f"      📏 Kích thước: {analysis['file_size']} bytes, Dòng: {analysis['line_count']}")
            if analysis['variable_names']:
                print(f"      🔤 Biến: {', '.join(analysis['variable_names'][:3])}{'...' if len(analysis['variable_names']) > 3 else ''}")

            # Đọc nội dung file
            with open(php_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Thử parsing với nhiều chiến lược
            data = self.parse_php_array_robust(content)

            if data is None:
                return False, "Tất cả chiến lược parsing đều thất bại", conversion_info

            # Validate output
            is_valid, validation_msg = self.validate_json_output(data)
            conversion_info['validation'] = {'valid': is_valid, 'message': validation_msg}

            if not is_valid:
                return False, f"Validation thất bại: {validation_msg}", conversion_info

            print(f"      ✅ Đã parse: {validation_msg}")

            # Lưu JSON file
            json_file = php_file.with_suffix('.json')
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return True, validation_msg, conversion_info

        except Exception as e:
            return False, f"Lỗi conversion: {str(e)}", conversion_info

    def run_robust(self):
        """Chạy converter với enhanced robustness"""
        print("🌍 Robust PHP to JSON Language Converter (Tiếng Việt)")
        print("=" * 65)

        count = self.find_php_files_recursive()

        if count == 0:
            print("✅ Không tìm thấy file PHP nào để convert!")
            return

        print(f"\n🎯 Chiến lược xử lý:")
        print(f"   • Nhiều parsing fallbacks")
        print(f"   • Validation chi tiết")
        print(f"   • Xử lý an toàn với delay {self.processing_delay}s")
        print(f"   • Logging lỗi toàn diện")

        choice = input(f"\n🔥 Xóa file .php sau khi convert thành công? (y/N): ").strip().lower()
        delete_php = choice in ['y', 'yes']

        if delete_php:
            confirm = input("⚠️  Bạn có chắc chắn? Không thể hoàn tác (y/N): ").strip().lower()
            delete_php = confirm in ['y', 'yes']

        print(f"\n🔄 Bắt đầu robust conversion {count} files...")
        print("=" * 65)

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
                        print(f"   🗑️  Đã xóa {php_file.name}")
                    except Exception as e:
                        print(f"   ⚠️  Không thể xóa {php_file.name}: {e}")
            else:
                self.failed_count += 1
                self.failed_files.append(php_file)
                failed_details.append({
                    'file': php_file.name,
                    'error': message,
                    'info': info
                })
                print(f"   ❌ {php_file.name}: {message}")

            # Delay nhỏ để an toàn
            if self.processing_delay > 0:
                time.sleep(self.processing_delay)

        self._print_final_results(failed_details)

    def _print_final_results(self, failed_details: List[Dict]):
        """In kết quả cuối cùng toàn diện"""
        print(f"\n" + "=" * 65)
        print(f"📊 KẾT QUẢ CUỐI CÙNG:")
        print(f"   ✅ Thành công: {self.converted_count} files")
        print(f"   ❌ Thất bại: {self.failed_count} files")

        if self.deleted_count > 0:
            print(f"   🗑️  Đã xóa: {self.deleted_count} file PHP")

        if failed_details:
            print(f"\n❌ PHÂN TÍCH CÁC FILE THẤT BẠI:")
            error_summary = {}
            for detail in failed_details:
                error_type = detail['error'].split(':')[0]
                error_summary[error_type] = error_summary.get(error_type, 0) + 1

            for error_type, count in error_summary.items():
                print(f"   • {error_type}: {count} files")

        success_rate = (self.converted_count / len(self.php_files)) * 100 if self.php_files else 0
        print(f"\n🎯 Tỷ lệ thành công: {success_rate:.1f}%")

        if success_rate < 90:
            print(f"\n💡 KHUYẾN NGHỊ:")
            print(f"   • Kiểm tra các file thất bại thủ công để tìm PHP syntax bất thường")
            print(f"   • Một số file có thể cần convert thủ công")
            print(f"   • Hãy tạo issue trên GitHub với sample các file thất bại")

def main():
    try:
        converter = RobustPHPToJSONConverter()
        converter.run_robust()
    except KeyboardInterrupt:
        print("\n⚠️ Đã dừng bởi người dùng")
    except Exception as e:
        print(f"❌ Lỗi nghiêm trọng: {e}")

if __name__ == "__main__":
    main()
