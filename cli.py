#!/usr/bin/env python3
"""
PDF Compressor CLI - A powerful command-line tool for compressing PDF files.
"""

import os
import sys
import click
from colorama import init, Fore, Back, Style
from tqdm import tqdm
import time
from pdf_compressor import PDFCompressor

# Initialize colorama for cross-platform colored output
init(autoreset=True)

def print_splash_screen():
    """Display the atlverse brand splash screen with blue gradient."""
    splash_art = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║     █████  ████████ ██       ██    ██ ██████  ███████ ███████║
    ║    ██   ██    ██    ██       ██    ██ ██   ██ ██      ██     ║
    ║    ███████    ██    ██       ████████ ██████  █████   ███████║
    ║    ██   ██    ██    ██       ██    ██ ██   ██ ██           ██║
    ║    ██   ██    ██    ████████ ██    ██ ██   ██ ███████ ███████║
    ║                                                              ║
    ║                    PDF Compressor v1.0                       ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    
    # Blue gradient colors
    colors = [Fore.BLUE, Fore.CYAN, Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX]
    
    lines = splash_art.split('\n')
    for i, line in enumerate(lines):
        if line.strip():
            color = colors[i % len(colors)]
            print(f"{color}{line}")
        else:
            print(line)
    
    print(f"\n{Fore.LIGHTBLUE_EX}Welcome to atlverse PDF Compressor!")
    print(f"{Fore.CYAN}Efficient PDF compression made simple.\n")

def print_progress_bar(description: str, total: int):
    """Display a progress bar with the given description."""
    with tqdm(total=total, desc=description, 
              bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]') as pbar:
        for i in range(total):
            time.sleep(0.1)  # Simulate work
            pbar.update(1)

@click.group(invoke_without_command=True)
@click.version_option(version='1.0.0', prog_name='atlverse PDF Compressor')
@click.pass_context
def cli(ctx):
    """atlverse PDF Compressor - Efficient PDF compression tool."""
    print_splash_screen()
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())

@cli.command()
@click.argument('input_file', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument('output_file', type=click.Path())
@click.option('--level', '-l', 
              type=click.Choice(['low', 'medium', 'high'], case_sensitive=False),
              default='medium', 
              help='Compression level (low/medium/high)')
@click.option('--quality', '-q', 
              type=click.IntRange(1, 100), 
              default=85,
              help='Image quality (1-100)')
@click.option('--remove-metadata', '-r', 
              is_flag=True, 
              default=True,
              help='Remove PDF metadata')
@click.option('--verbose', '-v', 
              is_flag=True, 
              help='Verbose output')
def compress(input_file, output_file, level, quality, remove_metadata, verbose):
    """Compress a PDF file."""
    compressor = PDFCompressor()
    
    # Validate input file
    print(f"{Fore.YELLOW}Validating PDF file...")
    is_valid, message = compressor.validate_pdf(input_file)
    if not is_valid:
        print(f"{Fore.RED}❌ {message}")
        sys.exit(1)
    
    print(f"{Fore.GREEN}✅ PDF is valid")
    
    # Get file info
    if verbose:
        print(f"\n{Fore.CYAN}📄 File Information:")
        info = compressor.get_pdf_info(input_file)
        for key, value in info.items():
            if key != 'size':  # Skip raw size, show formatted
                print(f"   {key.replace('_', ' ').title()}: {value}")
    
    # Show compression settings
    print(f"\n{Fore.LIGHTBLUE_EX}⚙️  Compression Settings:")
    print(f"   Level: {level.upper()}")
    print(f"   Image Quality: {quality}%")
    print(f"   Remove Metadata: {'Yes' if remove_metadata else 'No'}")
    
    # Compress the file
    print(f"\n{Fore.YELLOW}🔄 Compressing PDF...")
    
    # Show progress bar
    print_progress_bar("Processing", 10)
    
    success, message = compressor.compress_pdf(
        input_file, output_file, level, quality, remove_metadata
    )
    
    if success:
        print(f"\n{Fore.GREEN}✅ {message}")
        print(f"\n{Fore.LIGHTGREEN_EX}🎉 Compression completed successfully!")
        print(f"   Output file: {output_file}")
    else:
        print(f"\n{Fore.RED}❌ {message}")
        sys.exit(1)

@cli.command()
@click.argument('file_path', type=click.Path(exists=True, file_okay=True, dir_okay=False))
def info(file_path):
    """Display detailed information about a PDF file."""
    compressor = PDFCompressor()
    
    print(f"{Fore.CYAN}📄 PDF Information for: {file_path}\n")
    
    # Validate file
    is_valid, message = compressor.validate_pdf(file_path)
    if not is_valid:
        print(f"{Fore.RED}❌ {message}")
        sys.exit(1)
    
    # Get and display info
    info = compressor.get_pdf_info(file_path)
    
    print(f"{Fore.LIGHTBLUE_EX}File Details:")
    print(f"   📏 Size: {info.get('size_formatted', 'Unknown')}")
    print(f"   📄 Pages: {info.get('pages', 'Unknown')}")
    
    print(f"\n{Fore.LIGHTBLUE_EX}Metadata:")
    print(f"   📝 Title: {info.get('title', 'Unknown')}")
    print(f"   👤 Author: {info.get('author', 'Unknown')}")
    print(f"   📋 Subject: {info.get('subject', 'Unknown')}")
    print(f"   🛠️  Creator: {info.get('creator', 'Unknown')}")
    print(f"   🏭 Producer: {info.get('producer', 'Unknown')}")
    print(f"   📅 Created: {info.get('creation_date', 'Unknown')}")
    print(f"   🔄 Modified: {info.get('modification_date', 'Unknown')}")

@cli.command()
@click.argument('input_file', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument('output_file', type=click.Path())
@click.option('--quality', '-q', 
              type=click.IntRange(1, 100), 
              default=85,
              help='Image quality (1-100)')
def compress_images(input_file, output_file, quality):
    """Compress images within a PDF file."""
    compressor = PDFCompressor()
    
    print(f"{Fore.YELLOW}🖼️  Compressing images in PDF...")
    
    # Show progress bar
    print_progress_bar("Processing images", 8)
    
    success, message = compressor.compress_images_in_pdf(input_file, output_file, quality)
    
    if success:
        print(f"\n{Fore.GREEN}✅ {message}")
        print(f"\n{Fore.LIGHTGREEN_EX}🎉 Image compression completed!")
        print(f"   Output file: {output_file}")
    else:
        print(f"\n{Fore.RED}❌ {message}")
        sys.exit(1)

@cli.command()
def batch():
    """Interactive batch compression mode."""
    print(f"{Fore.CYAN}🔄 Batch Compression Mode")
    print(f"{Fore.LIGHTBLUE_EX}Enter PDF files to compress (one per line, empty line to finish):\n")
    
    files = []
    while True:
        file_path = input(f"{Fore.YELLOW}📁 File path: ").strip()
        if not file_path:
            break
        if os.path.exists(file_path):
            files.append(file_path)
        else:
            print(f"{Fore.RED}❌ File not found: {file_path}")
    
    if not files:
        print(f"{Fore.YELLOW}No files to process.")
        return
    
    # Get compression settings
    print(f"\n{Fore.CYAN}⚙️  Compression Settings:")
    level = input(f"{Fore.YELLOW}Level (low/medium/high) [medium]: ").strip().lower() or 'medium'
    quality = input(f"{Fore.YELLOW}Image quality (1-100) [85]: ").strip() or '85'
    
    try:
        quality = int(quality)
    except ValueError:
        quality = 85
    
    compressor = PDFCompressor()
    
    print(f"\n{Fore.LIGHTBLUE_EX}🔄 Processing {len(files)} files...\n")
    
    for i, file_path in enumerate(files, 1):
        print(f"{Fore.CYAN}[{i}/{len(files)}] Processing: {os.path.basename(file_path)}")
        
        # Generate output filename
        name, ext = os.path.splitext(file_path)
        output_path = f"{name}_compressed{ext}"
        
        success, message = compressor.compress_pdf(file_path, output_path, level, quality, True)
        
        if success:
            print(f"{Fore.GREEN}   ✅ {message.split('!')[0]}!")
        else:
            print(f"{Fore.RED}   ❌ {message}")
    
    print(f"\n{Fore.LIGHTGREEN_EX}🎉 Batch processing completed!")

if __name__ == '__main__':
    cli() 