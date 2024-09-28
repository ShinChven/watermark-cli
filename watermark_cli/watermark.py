#!/usr/bin/env python3

import argparse
import os
from PIL import Image, ImageDraw, ImageFont

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

def main():
    parser = argparse.ArgumentParser(description="Add watermark to images")
    parser.add_argument("source", help="Source directory or image file path")
    parser.add_argument("--text", default="@ShinChven", help="Watermark text (default: @ShinChven)")
    args = parser.parse_args()

    process_images(args.source, args.text)

if __name__ == "__main__":
    main()