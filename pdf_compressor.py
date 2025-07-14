import os
import PyPDF2
from PIL import Image
import io
import tempfile
from typing import Optional, Tuple
import logging

class PDFCompressor:
    """
    A comprehensive PDF compression utility that can reduce file size
    through various optimization techniques.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def compress_pdf(self, input_path: str, output_path: str, 
                    compression_level: str = 'medium',
                    image_quality: int = 85,
                    remove_metadata: bool = True) -> Tuple[bool, str]:
        """
        Compress a PDF file using various optimization techniques.
        
        Args:
            input_path: Path to the input PDF file
            output_path: Path where the compressed PDF will be saved
            compression_level: 'low', 'medium', or 'high'
            image_quality: JPEG quality for image compression (1-100)
            remove_metadata: Whether to remove PDF metadata
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Validate input file
            if not os.path.exists(input_path):
                return False, f"Input file not found: {input_path}"
            
            # Get original file size
            original_size = os.path.getsize(input_path)
            
            # Read the original PDF
            with open(input_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                writer = PyPDF2.PdfWriter()
                
                # Copy pages with compression
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    
                    # Apply compression based on level
                    if compression_level == 'high':
                        page.compress_content_streams()
                    
                    writer.add_page(page)
                
                # Remove metadata if requested
                if remove_metadata:
                    writer.remove_links()
                    # Note: PyPDF2 doesn't have direct metadata removal
                    # but we can minimize it by not copying metadata
                
                # Write compressed PDF
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
            
            # Get compressed file size
            compressed_size = os.path.getsize(output_path)
            
            # Calculate compression ratio
            compression_ratio = ((original_size - compressed_size) / original_size) * 100
            
            success_message = (
                f"Compression completed successfully!\n"
                f"Original size: {self._format_size(original_size)}\n"
                f"Compressed size: {self._format_size(compressed_size)}\n"
                f"Space saved: {self._format_size(original_size - compressed_size)} "
                f"({compression_ratio:.1f}%)"
            )
            
            return True, success_message
            
        except Exception as e:
            self.logger.error(f"Error compressing PDF: {str(e)}")
            return False, f"Error compressing PDF: {str(e)}"
    
    def compress_images_in_pdf(self, input_path: str, output_path: str, 
                             quality: int = 85) -> Tuple[bool, str]:
        """
        Compress images within a PDF file.
        
        Args:
            input_path: Path to the input PDF file
            output_path: Path where the compressed PDF will be saved
            quality: JPEG quality for image compression (1-100)
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # This is a simplified version - in a full implementation,
            # you would extract images from PDF, compress them, and re-insert
            # For now, we'll use the basic compression method
            return self.compress_pdf(input_path, output_path, 'high', quality, True)
            
        except Exception as e:
            self.logger.error(f"Error compressing images in PDF: {str(e)}")
            return False, f"Error compressing images in PDF: {str(e)}"
    
    def get_pdf_info(self, file_path: str) -> dict:
        """
        Get information about a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Dictionary containing PDF information
        """
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                info = {
                    'pages': len(reader.pages),
                    'size': os.path.getsize(file_path),
                    'size_formatted': self._format_size(os.path.getsize(file_path)),
                    'title': reader.metadata.get('/Title', 'Unknown'),
                    'author': reader.metadata.get('/Author', 'Unknown'),
                    'subject': reader.metadata.get('/Subject', 'Unknown'),
                    'creator': reader.metadata.get('/Creator', 'Unknown'),
                    'producer': reader.metadata.get('/Producer', 'Unknown'),
                    'creation_date': reader.metadata.get('/CreationDate', 'Unknown'),
                    'modification_date': reader.metadata.get('/ModDate', 'Unknown')
                }
                
                return info
                
        except Exception as e:
            self.logger.error(f"Error getting PDF info: {str(e)}")
            return {}
    
    def _format_size(self, size_bytes: int) -> str:
        """Convert bytes to human readable format."""
        if size_bytes == 0:
            return "0B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f}{size_names[i]}"
    
    def validate_pdf(self, file_path: str) -> Tuple[bool, str]:
        """
        Validate if a file is a valid PDF.
        
        Args:
            file_path: Path to the file to validate
            
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        try:
            with open(file_path, 'rb') as file:
                # Check if file starts with PDF signature
                header = file.read(4)
                if header != b'%PDF':
                    return False, "File is not a valid PDF (missing PDF signature)"
                
                # Try to read with PyPDF2
                file.seek(0)
                reader = PyPDF2.PdfReader(file)
                if len(reader.pages) == 0:
                    return False, "PDF appears to be empty or corrupted"
                
                return True, "PDF is valid"
                
        except Exception as e:
            return False, f"Error validating PDF: {str(e)}" 