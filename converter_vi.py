#!/usr/bin/env python3
"""
Recursive PHP Language Files to JSON Converter - Vietnamese Version
===================================================================
Công cụ convert file ngôn ngữ từ .php sang .json theo cấu trúc thư mục đệ quy

Cách sử dụng:
1. Đặt file này vào thư mục root chứa các thư mục ngôn ngữ (ar, bn, vi, en...)
2. Chạy: python converter_vi.py
3. Chọn có xóa file .php sau khi convert thành công không

Tính năng:
- Quét đệ quy tất cả thư mục con
- Convert .php -> .json trong cùng thư mục
- Tùy chọn xóa file .php sau khi convert thành công
- Báo cáo chi tiết theo từng thư mục
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
        """Tìm tất cả file .php trong tất cả thư mục con"""
        self.php_files = []
        
        for php_file in self.root_dir.rglob("*.php"):
            if php_file.name in ["converter_en.py", "converter_vi.py", "load_json_example.php"]:
                continue
                
            if skip_existing:
                json_file = php_file.with_suffix('.json')
                if json_file.exists():
                    print(f"⏭️  Bỏ qua {php_file.relative_to(self.root_dir)} (JSON đã tồn tại)")
                    continue
                    
            self.php_files.append(php_file)
        
        return len(self.php_files)

    def parse_php_array(self, content):
        """Parse PHP array từ nội dung file"""
        content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        content = re.sub(r'<\?php', '', content)
        content = re.sub(r'\?>', '', content)
        content = content.strip()
        
        patterns = [
            r'return\s*\[(.*?)\];',
            r'return\s*array\s*\((.*?)\);',
            r'\$lang\s*=\s*\[(.*?)\];',
            r'\$lang\s*=\s*array\s*\((.*?)\);',
            r'\$language\s*=\s*\[(.*?)\];',
            r'\$language\s*=\s*array\s*\((.*?)\);',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                array_content = match.group(1)
                result = self.parse_array_content(array_content)
                if result and len(result) > 0:
                    return result
        
        return None

    def parse_array_content(self, array_content):
        """Parse nội dung array"""
        result = {}
        lines = array_content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
                
            if '=>' in line:
                parts = line.split('=>', 1)
                if len(parts) == 2:
                    key_part = parts[0].strip()
                    value_part = parts[1].strip()
                    
                    key_match = re.search(r"['\""]([^'\""]*)[\"'""]", key_part)
                    value_match = re.search(r"['\""]([^'\""]*)[\"'""]", value_part)
                    
                    if key_match and value_match:
                        result[key_match.group(1)] = value_match.group(1)
        
        return result

    def convert_file(self, php_file):
        """Convert một file PHP sang JSON"""
        try:
            with open(php_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            data = self.parse_php_array(content)
            
            if data is None or len(data) == 0:
                return False, "Không thể parse PHP array hoặc array rỗng"
            
            json_file = php_file.with_suffix('.json')
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True, f"✅ {len(data)} keys"
            
        except Exception as e:
            return False, f"Lỗi: {str(e)}"

    def run(self):
        """Chạy tool converter"""
        print("🌍 PHP to JSON Language Converter (Tiếng Việt)")
        print("=" * 55)
        
        count = self.find_php_files_recursive()
        
        if count == 0:
            print("✅ Không tìm thấy file PHP nào để convert!")
            return
        
        print(f"🔍 Tìm thấy {count} file PHP để convert")
        
        choice = input("\n🔥 Xóa file .php sau khi convert? (y/N): ").strip().lower()
        delete_php = choice in ['y', 'yes']
        
        print("\n🔄 Bắt đầu convert...")
        
        for php_file in self.php_files:
            success, message = self.convert_file(php_file)
            
            if success:
                self.converted_count += 1
                print(f"   ✅ {php_file.name} -> {php_file.stem}.json")
                
                if delete_php:
                    try:
                        php_file.unlink()
                        self.deleted_count += 1
                        print(f"   🗑️  Đã xóa {php_file.name}")
                    except Exception as e:
                        print(f"   ⚠️  Không thể xóa {php_file.name}: {e}")
            else:
                self.failed_count += 1
                print(f"   ❌ {php_file.name}: {message}")
        
        print(f"\n📊 KẾT QUẢ:")
        print(f"   ✅ Thành công: {self.converted_count} files")
        print(f"   ❌ Thất bại: {self.failed_count} files")
        
        if delete_php and self.deleted_count > 0:
            print(f"   🗑️  Đã xóa: {self.deleted_count} file PHP")

def main():
    try:
        converter = RecursivePHPToJSONConverter()
        converter.run()
    except KeyboardInterrupt:
        print("\n⚠️ Đã dừng bởi người dùng")
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    main()
