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

### 🐛 Recent Bug Fixes (v1.0.1)

#### Fixed Issues:
- **❌ Quote Handling Problem**: Resolved extra quotes in JSON output (e.g., `"example"` instead of `example`)
- **❌ Incomplete Parsing**: Fixed missing translations due to limited PHP format recognition
- **❌ Escaped Characters**: Properly handle escaped quotes and special characters
- **❌ Multi-line Support**: Now correctly processes multi-line string values

#### Improvements:
- **✅ Enhanced Regex Parsing**: Advanced pattern matching for complex PHP structures
- **✅ Better Quote Extraction**: Intelligent quote removal without content loss
- **✅ Extended Variable Support**: Recognition of `$data`, `$translations`, `$messages` variables
- **✅ Fallback Mechanism**: Dual parsing approach for maximum compatibility

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
