#!/usr/bin/env python3
"""
PDF Compressor Web Application - A modern web interface for PDF compression.
"""

import os
import tempfile
import uuid
from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from pdf_compressor import PDFCompressor
import logging
from subprocess import run, CalledProcessError
import zipfile
import io

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'atlverse-pdf-compressor-secret-key-2024'

# Configuration
UPLOAD_FOLDER = 'uploads'
COMPRESSED_FOLDER = 'compressed'
ALLOWED_EXTENSIONS = {'pdf'}

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COMPRESSED_FOLDER'] = COMPRESSED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

GS_QUALITY_MAP = {
    'screen': '/screen',
    'ebook': '/ebook',
    'printer': '/printer',
    'prepress': '/prepress',
    'default': '/default',
}

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_size(file_path):
    """Get file size in human readable format."""
    size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"

@app.route('/')
def index():
    """Main page with upload form."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and compression."""
    try:
        files = request.files.getlist('file')
        if not files:
            return jsonify({'error': 'No file selected'}), 400
        results = []
        for file in files:
            if file.filename == '':
                continue
            if not allowed_file(file.filename):
                continue
            gs_quality = request.form.get('gs_quality', 'ebook')
            filename = secure_filename(file.filename)
            name, ext = os.path.splitext(filename)
            output_filename = f"{name}_compressed{ext}"
            output_path = os.path.join(app.config['COMPRESSED_FOLDER'], f"{uuid.uuid4().hex}_{output_filename}")
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4().hex}_{filename}")
            file.save(input_path)
            gs_quality_flag = GS_QUALITY_MAP.get(gs_quality, '/ebook')
            gs_cmd = [
                'gs',
                '-sDEVICE=pdfwrite',
                '-dCompatibilityLevel=1.4',
                f'-dPDFSETTINGS={gs_quality_flag}',
                '-dNOPAUSE',
                '-dQUIET',
                '-dBATCH',
                f'-sOutputFile={output_path}',
                input_path
            ]
            try:
                run(gs_cmd, capture_output=True, check=True)
                # Get stats
                original_size = os.path.getsize(input_path)
                compressed_size = os.path.getsize(output_path)
                space_saved = original_size - compressed_size
                compression_ratio = (space_saved / original_size) * 100 if original_size else 0
                results.append({
                    'success': True,
                    'original_filename': filename,
                    'compressed_filename': output_filename,
                    'download_path': f'/download/{os.path.basename(output_path)}?download_name={output_filename}',
                    'stats': {
                        'original_size': f'{original_size/1024:.1f} KB',
                        'compressed_size': f'{compressed_size/1024:.1f} KB',
                        'space_saved': f'{space_saved/1024:.1f} KB',
                        'compression_ratio': f'{compression_ratio:.1f}%'
                    }
                })
            except CalledProcessError as e:
                results.append({
                    'success': False,
                    'original_filename': filename,
                    'error': f'Ghostscript compression failed: {e.stderr.decode() if e.stderr else str(e)}'
                })
            finally:
                os.remove(input_path)
        return jsonify({'results': results})
    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download compressed PDF file."""
    try:
        file_path = os.path.join(app.config['COMPRESSED_FOLDER'], filename)
        download_name = request.args.get('download_name', filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=download_name)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logger.error(f"Error downloading file: {str(e)}")
        return jsonify({'error': 'Download failed'}), 500

@app.route('/download-zip', methods=['POST'])
def download_zip():
    try:
        data = request.get_json()
        files = data.get('files', [])
        mem_zip = io.BytesIO()
        with zipfile.ZipFile(mem_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
            for url in files:
                # Extract filename from url
                filename = url.split('download_name=')[-1]
                # Find the actual file in compressed folder
                for f in os.listdir(app.config['COMPRESSED_FOLDER']):
                    if f.endswith(filename):
                        file_path = os.path.join(app.config['COMPRESSED_FOLDER'], f)
                        zf.write(file_path, arcname=filename)
                        break
        mem_zip.seek(0)
        return send_file(mem_zip, as_attachment=True, download_name='compressed_pdfs.zip', mimetype='application/zip')
    except Exception as e:
        logger.error(f"Error creating zip: {str(e)}")
        return jsonify({'error': 'Failed to create zip'}), 500

@app.route('/info', methods=['POST'])
def get_file_info():
    """Get information about uploaded PDF file."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file selected'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f"temp_{uuid.uuid4().hex}_{filename}")
        file.save(temp_path)
        
        # Get file info
        compressor = PDFCompressor()
        is_valid, message = compressor.validate_pdf(temp_path)
        
        if not is_valid:
            os.remove(temp_path)
            return jsonify({'error': message}), 400
        
        info = compressor.get_pdf_info(temp_path)
        
        # Clean up
        os.remove(temp_path)
        
        return jsonify({
            'success': True,
            'info': info
        })
        
    except Exception as e:
        logger.error(f"Error getting file info: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/cleanup', methods=['POST'])
def cleanup_files():
    """Clean up old compressed files."""
    try:
        import time
        current_time = time.time()
        max_age = 3600  # 1 hour
        
        cleaned_count = 0
        for filename in os.listdir(app.config['COMPRESSED_FOLDER']):
            file_path = os.path.join(app.config['COMPRESSED_FOLDER'], filename)
            if os.path.isfile(file_path):
                file_age = current_time - os.path.getmtime(file_path)
                if file_age > max_age:
                    os.remove(file_path)
                    cleaned_count += 1
        
        return jsonify({
            'success': True,
            'message': f'Cleaned up {cleaned_count} old files'
        })
        
    except Exception as e:
        logger.error(f"Error cleaning up files: {str(e)}")
        return jsonify({'error': 'Cleanup failed'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 