import os
import base64
from pathlib import Path
from mistralai import Mistral, DocumentURLChunk
from mistralai.models import OCRResponse
import json
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
import io
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

# -------- Cloudinary Setup --------
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True
)

# -------- Mistral OCR Setup --------
api_key = MISTRAL_API_KEY
client = Mistral(api_key=api_key)

pdf_file = Path("docs/physics1_removed.pdf")
assert pdf_file.is_file(), "PDF file not found!"

uploaded_file = client.files.upload(
    file={
        "file_name": pdf_file.stem,
        "content": pdf_file.read_bytes(),
    },
    purpose="ocr",
)

signed_url = client.files.get_signed_url(file_id=uploaded_file.id, expiry=1)

pdf_response = client.ocr.process(
    document=DocumentURLChunk(document_url=signed_url.url),
    model="mistral-ocr-latest",
    include_image_base64=True
)
response_dict = json.loads(pdf_response.model_dump_json())

# -------- Upload Base64 to Cloudinary --------
def upload_base64_to_cloudinary(base64_data: str, img_id: str) -> str:
    """
    Uploads base64 image data to Cloudinary and returns the optimized image URL.
    """
    try:
        # Ensure base64 data is properly formatted
        if ',' in base64_data:
            base64_data = base64_data.split(',')[1]
        
        # Remove any extension from img_id
        img_id = os.path.splitext(img_id)[0]
        
        # Decode base64 data
        image_data = base64.b64decode(base64_data)
        
        # Save to temporary file first to ensure valid image
        temp_file = f"temp_{img_id}"
        with open(temp_file, "wb") as f:
            f.write(image_data)
        
        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(
            temp_file,
            public_id=f"ocr_images/{img_id}",
            resource_type="image",
            format="png"
        )
        
        # Clean up temporary file
        os.remove(temp_file)
        
        # Use the secure_url directly from the upload result
        return upload_result['secure_url']
        
    except Exception as e:
        print(f"Error uploading image {img_id}: {str(e)}")
        # Print base64 data length for debugging
        print(f"Base64 data length: {len(base64_data)}")
        return f"https://via.placeholder.com/150?text=Upload+Failed"

def replace_images_in_markdown(markdown_str: str, images_dict: dict) -> str:
    """
    Replace image placeholders in markdown with Cloudinary URLs.
    """
    for img_name, image_url in images_dict.items():
        markdown_str = markdown_str.replace(
            f"![{img_name}]({img_name})", f"![{img_name}]({image_url})"
        )
    return markdown_str


# -------- Generate and Save Markdown --------
combined_markdown = get_combined_markdown(pdf_response)

print(combined_markdown)

with open("output.md", "w") as f:
    f.write(combined_markdown)
