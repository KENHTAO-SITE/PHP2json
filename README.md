# PHP to JSON Language Converter

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub Release](https://img.shields.io/github/v/release/KENHTAO-SITE/PHP2json)](https://github.com/KENHTAO-SITE/PHP2json/releases)

🌍 **[English](#english)** | **[Tiếng Việt](#tiếng-việt)**

---

## English

### 📋 Overview

**PHP to JSON Language Converter** is a powerful automation tool designed to migrate multilingual internationalization systems from PHP format to JSON. Perfect for modernizing legacy web applications with multiple language support.

### ✨ Key Features

- 🔄 **Recursive Directory Scanning** - Automatically processes all language directories
- 📊 **Intelligent Status Analysis** - Detailed conversion reports by directory
- 🎯 **Smart Conversion Modes** - Incremental or force overwrite options
- 🛡️ **Safe File Management** - Double confirmation before file deletion
- 🔍 **Advanced Debug Mode** - Verbose output for troubleshooting
- 📝 **Production-Ready Code** - Auto-generates JSON loader classes
- 🌐 **UTF-8 Support** - Preserves international characters perfectly
- ⚡ **High Performance** - Processes 100-500 files per second
- 🐛 **Improved PHP Parsing** - Fixed quote handling and incomplete conversion issues
- 🔧 **Enhanced Compatibility** - Supports more PHP variable names and formats

### 🚀 Quick Start

#### Installation
```bash
# Extract the ZIP package
unzip PHP2JSON-v1.0.0.zip
cd PHP2JSON-v1.0.0

# No dependencies required - uses only Python standard library
```

#### Basic Usage
```bash
# English version
python3 converter_en.py

# Vietnamese version
python3 converter_vi.py
```

### 📁 Project Structure
```
your-project/
├── ar/
│   ├── messages.php
│   ├── errors.php
│   └── ...
├── en/
│   ├── messages.php
│   ├── errors.php
│   └── ...
├── vi/
│   ├── messages.php
│   ├── errors.php
│   └── ...
└── converter_en.py  # Place the tool here
```

### 💡 Usage Examples

#### Supported PHP Formats
```php
// Format 1: Return array
<?php
return [
    'welcome' => 'Welcome to our site',
    'menu' => [
        'home' => 'Home',
        'about' => 'About Us'
    ]
];

// Format 2: Variable assignment
<?php
$lang = array(
    'welcome' => 'Welcome to our site',
    'hello' => 'Hello {name}'
);

// Format 3: Multiple variable names (Enhanced Support)
$language = [...];
$data = [...];
$translations = [...];
$messages = [...];
```

### 🏢 Enterprise-Grade v1.0.3 - Production-Ready with Data Integrity

#### 🚀 Enterprise Features:
- **🔍 Data Integrity Verification**: 100% comparison between PHP and JSON data
- **🛡️ Automatic Backup System**: Creates backup before any file operations
- **📊 Deep Data Comparison**: Key-by-key and value-by-value verification
- **🔄 Auto-Retry Mechanism**: Up to 3 attempts for failed conversions
- **📋 Enterprise Logging**: Comprehensive audit trails with timestamps
- **⚡ Safe Deletion**: Multiple confirmations before removing PHP files
- **🏗️ Production-Level Error Handling**: Rollback capability for safety

#### 🔒 Data Integrity Checks:
1. **File Existence**: Verify JSON file was created successfully
2. **Key Count Matching**: Ensure same number of keys in PHP and JSON
3. **Deep Key-Value Comparison**: Compare every key-value pair exactly
4. **Content Hash Verification**: Mathematical verification of data integrity
5. **Extra/Missing Key Detection**: Identify any data loss or corruption

#### 📊 Enterprise Logging System:
- **Conversion Log**: Detailed record of all conversion operations
- **Integrity Log**: Results of all data verification checks
- **Backup Log**: Complete audit trail of backup operations
- **Timestamped Entries**: Every operation logged with precise timestamps

#### 🛡️ Safety Features:
- Automatic backup creation before any file modification
- Data integrity verification before allowing PHP file deletion
- Triple confirmation system for file deletion
- Complete rollback capability if issues detected
- Enterprise-grade error reporting and recommendations

#### 🔧 Advanced Parsing Strategies (Inherited from v1.0.2):
1. **Advanced Regex**: Enhanced pattern matching with nested structure support
2. **Tokenizer Approach**: PHP-like tokenization for complex structures
3. **State Machine**: Line-by-line parsing with context awareness
4. **Manual Nested**: Hand-crafted parsing for edge cases

#### 📱 Enterprise Processing Output Example:
```
🏢 Enterprise PHP to JSON Language Converter (English)
======================================================================

📋 Enterprise logging enabled:
   • Conversion log: conversion_20240726_143022.log
   • Integrity log: integrity_20240726_143022.log
   • Backup log: backup_20240726_143022.log

🔍 Enterprise scanning for PHP files...
📊 Found 408 PHP files for enterprise processing

🛡️ Enterprise backup system created: backup_20240726_143022

📊 [1/408] ar/messages.php
   📁 Enterprise processing: messages.php
      📏 Size: 2048 bytes, Lines: 45
      🔤 Variables: lang, language, data
      🔄 Conversion attempt 1/3
      ✅ Conversion successful: Valid with 23 keys
      🔍 Data integrity verification...
      ✅ Data integrity verified: 100% match
   ✅ messages.php -> messages.json (Valid with 23 keys + integrity verified)
   🗑️ Safely deleted messages.php

🏢 ENTERPRISE CONVERSION RESULTS:
   ✅ Successfully converted: 407 files
   🔍 Integrity verified: 407 files
   ❌ Failed conversions: 1 files
   ⚠️ Integrity failures: 0 files
   🗑️ Safely deleted: 407 PHP files
   🛡️ Backup directory: backup_20240726_143022

📊 ENTERPRISE METRICS:
   🎯 Conversion Success Rate: 99.8%
   🔍 Data Integrity Rate: 100.0%
   📋 Log Files: conversion_logs/
```

### 🐛 Previous Bug Fixes (v1.0.1)

#### Fixed Issues:
- **❌ Quote Handling Problem**: Resolved extra quotes in JSON output
- **❌ Incomplete Parsing**: Fixed missing translations due to limited PHP format recognition
- **❌ Escaped Characters**: Properly handle escaped quotes and special characters
- **❌ Multi-line Support**: Now correctly processes multi-line string values

#### Generated JSON Output
```json
{
  "welcome": "Welcome to our site",
  "menu": {
    "home": "Home",
    "about": "About Us"
  }
}
```

#### Auto-Generated Loader Class
```php
<?php
$lang = new LanguageLoader();

// Load complete file
$messages = $lang->load('en', 'messages');

// Get specific key with fallback
echo $lang->get('en', 'menu.home', 'messages', 'Home');
```

### 🔧 Conversion Modes

#### Mode 1: Incremental (Recommended)
- Converts only PHP files without corresponding JSON
- Safe, non-destructive approach
- Perfect for partial conversions

#### Mode 2: Force Overwrite
- Re-converts all PHP files
- Overwrites existing JSON files
- Use when complete refresh is needed

### 📊 Example Output
```
🔍 SCANNING STATUS...
========================================

📂 en:
   📄 PHP files: 12
   ✅ Converted: 7
   ⏳ Pending: 5
   📋 Pending files: error.php, footer.php, order.php

📂 Directory: en
   ✅ error.php -> error.json (23 keys)
   ✅ footer.php -> footer.json (8 keys)
   ✅ order.php -> order.json (45 keys)

📊 FINAL RESULTS:
   ✅ Success: 156 files
   ❌ Failed: 2 files
```

### 🛡️ Safety Features

- **Double Confirmation** before deleting PHP files
- **Backup Warnings** and recommendations
- **Atomic Operations** - complete conversion before cleanup
- **Error Isolation** - individual file failures don't stop process
- **UTF-8 Preservation** - maintains international characters

### 📋 Requirements

- Python 3.6 or higher
- UTF-8 file system support
- Read/write permissions in target directories

---

## Tiếng Việt

### 📋 Tổng quan

**PHP to JSON Language Converter** là công cụ tự động hóa mạnh mẽ được thiết kế để chuyển đổi hệ thống ngôn ngữ đa quốc gia từ format PHP sang JSON. Hoàn hảo cho việc modernize các ứng dụng web legacy với hỗ trợ đa ngôn ngữ.

### ✨ Tính năng nổi bật

- 🔄 **Quét thư mục đệ quy** - Tự động xử lý tất cả thư mục ngôn ngữ
- 📊 **Phân tích trạng thái thông minh** - Báo cáo chi tiết theo từng thư mục
- 🎯 **Chế độ convert thông minh** - Tùy chọn incremental hoặc force overwrite
- 🛡️ **Quản lý file an toàn** - Xác nhận 2 lần trước khi xóa file
- 🔍 **Chế độ debug nâng cao** - Output chi tiết để troubleshoot
- 📝 **Code production-ready** - Tự động tạo class loader JSON
- 🌐 **Hỗ trợ UTF-8** - Bảo toàn ký tự quốc tế hoàn hảo
- ⚡ **Hiệu suất cao** - Xử lý 100-500 file mỗi giây

### 🚀 Bắt đầu nhanh

#### Cài đặt
```bash
# Giải nén package ZIP
unzip PHP2JSON-v1.0.0.zip
cd PHP2JSON-v1.0.0

# Không cần dependencies - chỉ sử dụng Python standard library
```

#### Sử dụng cơ bản
```bash
# Phiên bản tiếng Anh
python3 converter_en.py

# Phiên bản tiếng Việt
python3 converter_vi.py
```

### 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 🐛 Issues & Support

- **Bug Reports**: [Open an issue](https://github.com/KENHTAO-SITE/PHP2json/issues)
- **Feature Requests**: [Discussions](https://github.com/KENHTAO-SITE/PHP2json/discussions)
- **Documentation**: [Wiki](https://github.com/KENHTAO-SITE/PHP2json/wiki)

---

## 👨‍💻 Credits & Author

**Created by**: **Kênh Táo**

### 📞 Contact Information
- 📱 **Telegram**: [@QTUNUy](https://t.me/QTUNUy)
- 🌐 **Websites**:
  - [CertApple.com](https://certapple.com)
  - [Kenhtao.net](https://kenhtao.net)
  - [kenhtao.site](https://kenhtao.site)
  - [iPA.KenhTao.net](https://ipa.kenhtao.net)

### 💝 Support the Project
If this tool helps you, please consider:
- ⭐ **Star** this repository
- 🔄 **Share** with your developer community
- 💬 **Follow** on Telegram for updates
- 🌟 **Visit** our websites for more tools

---

## ⭐ Star History

If this project helps you, please consider giving it a ⭐!

[![Star History Chart](https://api.star-history.com/svg?repos=KENHTAO-SITE/PHP2json&type=Date)](https://star-history.com/#KENHTAO-SITE/PHP2json&Date)
