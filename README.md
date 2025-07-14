# atlverse PDF Compressor

> **Important:**
> This app requires [Ghostscript](https://www.ghostscript.com/) to be installed on your system.
>
> - **macOS:** `brew install ghostscript`
> - **Ubuntu/Debian:** `sudo apt-get install ghostscript`
> - **Windows:** Download and install from the [official site](https://www.ghostscript.com/download/gsdnld.html)

A powerful and efficient PDF compression tool built with Python, featuring both command-line interface and modern web application.

![atlverse PDF Compressor](https://img.shields.io/badge/atlverse-PDF%20Compressor-blue)
![Python](https://img.shields.io/badge/Python-3.7+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- **Multiple Compression Levels**: Low, Medium, and High compression options
- **Image Quality Control**: Adjustable image compression quality (1-100%)
- **Metadata Removal**: Option to remove PDF metadata for smaller file sizes
- **File Validation**: Automatic PDF validation before processing
- **Progress Tracking**: Real-time progress indicators
- **Batch Processing**: Process multiple files at once
- **File Information**: Detailed PDF metadata and statistics
- **Modern Web Interface**: Beautiful, responsive web UI with drag-and-drop
- **Command Line Interface**: Powerful CLI with colored output and progress bars

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd PDFcompressor
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**

   **Web Interface:**
   ```bash
   python web_app.py
   ```
   Then open your browser to `http://localhost:5000`

   **Command Line:**
   ```bash
   python cli.py --help
   ```

## 📖 Usage

### Command Line Interface

#### Basic Compression
```bash
# Compress a single PDF file
python cli.py compress input.pdf output_compressed.pdf

# With specific compression level
python cli.py compress input.pdf output.pdf --level high

# With custom image quality
python cli.py compress input.pdf output.pdf --quality 75
```

#### Get PDF Information
```bash
python cli.py info document.pdf
```

#### Compress Images in PDF
```bash
python cli.py compress-images input.pdf output.pdf --quality 80
```

#### Batch Processing
```bash
python cli.py batch
```

#### Available Options
- `--level, -l`: Compression level (low/medium/high)
- `--quality, -q`: Image quality (1-100)
- `--remove-metadata, -r`: Remove PDF metadata
- `--verbose, -v`: Verbose output

### Web Interface

1. **Open the web application** in your browser
2. **Drag and drop** a PDF file or click to browse
3. **Adjust compression settings**:
   - Compression Level: Low, Medium, or High
   - Image Quality: 1-100%
   - Remove Metadata: Check to remove PDF metadata
4. **Click "Compress PDF"** to start processing
5. **Download** the compressed file when complete

## 🛠️ Technical Details

### Compression Techniques

- **Content Stream Compression**: Optimizes PDF content streams
- **Image Compression**: Reduces image quality and resolution
- **Metadata Removal**: Strips unnecessary PDF metadata
- **Font Optimization**: Compresses embedded fonts
- **Object Deduplication**: Removes duplicate objects

### Supported Formats

- **Input**: PDF files only
- **Output**: Compressed PDF files
- **Maximum File Size**: 50MB (web interface)

### Performance

- **Compression Ratio**: Typically 20-60% size reduction
- **Processing Speed**: Varies by file size and compression level
- **Memory Usage**: Optimized for large files

## 📁 Project Structure

```
PDFcompressor/
├── pdf_compressor.py      # Core compression engine
├── cli.py                # Command-line interface
├── web_app.py            # Flask web application
├── templates/
│   └── index.html        # Web interface template
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── uploads/             # Temporary upload directory
└── compressed/          # Output directory for compressed files
```

## 🔧 Configuration

### Web Application Settings

Edit `web_app.py` to modify:
- Maximum file size (default: 50MB)
- Upload/compressed directories
- Server host and port
- File cleanup intervals

### CLI Settings

The CLI uses sensible defaults but can be customized:
- Progress bar style
- Color schemes
- Output formatting

## 🐛 Troubleshooting

### Common Issues

1. **"File not found" error**
   - Ensure the PDF file exists and is accessible
   - Check file permissions

2. **"Invalid PDF" error**
   - Verify the file is a valid PDF
   - Try opening the file in a PDF viewer

3. **Compression fails**
   - Check available disk space
   - Ensure the output directory is writable
   - Try a different compression level

4. **Web interface not loading**
   - Check if Flask is installed: `pip install flask`
   - Verify port 5000 is available
   - Check firewall settings

### Debug Mode

Enable debug mode for detailed error messages:

```bash
# Web application
export FLASK_DEBUG=1
python web_app.py

# CLI with verbose output
python cli.py compress input.pdf output.pdf --verbose
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **PyPDF2**: PDF manipulation library
- **Flask**: Web framework
- **Click**: CLI framework
- **Colorama**: Cross-platform colored terminal output
- **Font Awesome**: Icons for the web interface

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the documentation

---

**Made with ❤️ by atlverse**