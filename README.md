# watermark-cli

A command-line tool to add watermarks to images, supporting various formats including WebP.

## Installation

You can install watermark-cli using pip:

```
pip install git+https://github.com/ShinChven/watermark-cli.git
```

## Upgrade

You can upgrade watermark-cli using pip:

```
pip install --upgrade git+https://github.com/ShinChven/watermark-cli.git
```

## Usage

After installation, you can use the `watermark` command from your terminal:

```
watermark [source] [--text WATERMARK_TEXT]
```

- `source`: The path to an image file or a directory containing image files.
- `--text`: (Optional) The text to use as a watermark. Default is "@ShinChven".

### Supported Formats

The tool supports the following image formats:
- PNG
- JPEG
- WebP
- TIFF
- BMP
- GIF

### Examples

1. Add a watermark to a single image:
   ```
   watermark path/to/image.jpg
   ```

2. Add a custom watermark to a single image:
   ```
   watermark path/to/image.webp --text "My Watermark"
   ```

3. Add watermarks to all supported images in a directory:
   ```
   watermark path/to/image/directory
   ```

The watermarked images will be saved in a new directory named `watermark_images` in the same location as the source. The output format will match the input format.

## Development

To set up the development environment:

1. Clone the repository:
   ```
   git clone https://github.com/ShinChven/watermark-cli.git
   cd watermark-cli
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the package in editable mode:
   ```
   pip install -e .
   ```

Now you can make changes to the code and test them immediately using the `watermark` command.

## License

This project is licensed under the MIT License.
