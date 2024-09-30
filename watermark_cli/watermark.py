#!/usr/bin/env python3

import argparse
import os
import json
from PIL import Image, ImageDraw, ImageFont

CONFIG_FILE = os.path.expanduser("~/.watermark-cli/config.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def add_watermark(image_path, output_path, watermark_text):
    with Image.open(image_path) as img:
        # Create a transparent layer for the watermark
        watermark = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)

        # Use a default font (you may need to specify a font file path for custom fonts)
        font = ImageFont.load_default()

        # Calculate text size and position
        text_width, text_height = draw.textsize(watermark_text, font)
        x = (img.width - text_width) // 2
        y = (img.height - text_height) // 2

        # Draw the watermark text
        draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 77))

        # Combine the original image with the watermark
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            # If the image has an alpha channel or transparency, use alpha_composite
            watermarked = Image.alpha_composite(img.convert('RGBA'), watermark)
        else:
            # If the image is not transparent, paste the watermark
            watermarked = img.copy()
            watermarked.paste(watermark, (0, 0), watermark)

        # Save the watermarked image
        if img.format == 'JPEG':
            # For JPEG, we need to remove the alpha channel and use high quality
            watermarked = watermarked.convert('RGB')
            watermarked.save(output_path, quality=95, optimize=True)
        elif img.format == 'WEBP':
            # For WebP, we can save with lossless compression
            watermarked.save(output_path, format='WEBP', lossless=True)
        else:
            # For other formats (like PNG), save with original format and mode
            watermarked.save(output_path, format=img.format)
    
    print(f"Watermarked {image_path} to {output_path}")

def process_images(source_path, watermark_text):
    supported_formats = ('.png', '.jpg', '.jpeg', '.webp', '.tiff', '.bmp', '.gif')
    if os.path.isfile(source_path):
        if source_path.lower().endswith(supported_formats):
            output_dir = os.path.join(os.path.dirname(source_path), 'watermark_images')
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, os.path.basename(source_path))
            add_watermark(source_path, output_path, watermark_text)
        else:
            print(f"Error: {source_path} is not a supported image file")
    elif os.path.isdir(source_path):
        output_dir = os.path.join(source_path, 'watermark_images')
        os.makedirs(output_dir, exist_ok=True)
        for filename in os.listdir(source_path):
            if filename.lower().endswith(supported_formats):
                input_path = os.path.join(source_path, filename)
                output_path = os.path.join(output_dir, filename)
                add_watermark(input_path, output_path, watermark_text)
    else:
        print(f"Error: {source_path} is not a valid file or directory")

def set_config(default_text):
    config = load_config()
    config['default_text'] = default_text
    save_config(config)
    print(f"Default watermark text set to: {default_text}")

def main():
    config = load_config()
    default_text = config.get('default_text', '')

    parser = argparse.ArgumentParser(description="Add watermark to images")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Config command
    config_parser = subparsers.add_parser("config", help="Set default watermark text")
    config_parser.add_argument("--default-text", help="Default watermark text to set")

    # Watermark command
    watermark_parser = subparsers.add_parser("watermark", help="Add watermark to images")
    watermark_parser.add_argument("source", help="Source directory or image file path")
    watermark_parser.add_argument("--text", default=default_text, help="Watermark text (overrides default)")

    args = parser.parse_args()

    if args.command == "config":
        set_config(args.default_text)
    elif args.command == "watermark":
        if not args.text:
            print("Error: No watermark text provided. Please use --text or set a default text with the 'config' command")
            return
        process_images(args.source, args.text)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()