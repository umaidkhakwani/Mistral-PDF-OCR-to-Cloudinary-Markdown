# PDF OCR & Cloudinary Uploader

## System Structure

```
app.py
requirements.txt
docs/
    physics1_removed.pdf
```

- **app.py**: Main script for OCR processing and image uploading.
- **requirements.txt**: Python dependencies.
- **docs/**: Contains input PDF files.

## Implementation

1. **Cloudinary Setup**: Configures Cloudinary for image hosting.
2. **Mistral OCR Integration**: Uses Mistral API to process the PDF and extract text/images.
3. **Image Handling**: Extracted images are decoded from base64 and uploaded to Cloudinary.
4. **Markdown Generation**: OCR text and images are combined into a markdown file, with image links replaced by Cloudinary URLs.
5. **Output**: The final markdown is printed and saved as `output.md`.

## Features

- Extracts text and images from PDFs using OCR.
- Uploads images to Cloudinary for optimized hosting.
- Generates a markdown document with embedded images.
- Handles errors gracefully and provides fallback image URLs.

## Tech Stack

- **Python** (see [requirements.txt](requirements.txt))
- **Mistral OCR API** (`mistralai`)
- **Cloudinary** (`cloudinary`)
- **Pillow** (for image handling)

## Requirements

Install dependencies with:

```sh
pip install -r requirements.txt
```

## Usage

1. Place your PDF in the `docs/` folder.
2. Run the script:

```sh
python app.py
```

3. The processed markdown will be saved as `output.md`.

## Notes

- Ensure your Cloudinary and Mistral API credentials are set correctly in `app.py`.
- The script expects the PDF file to be named `physics1_removed.pdf` in the