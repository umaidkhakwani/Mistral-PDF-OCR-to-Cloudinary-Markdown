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


# -------- Generate and Save Markdown --------
combined_markdown = get_combined_markdown(pdf_response)

print(combined_markdown)

with open("output.md", "w") as f:
    f.write(combined_markdown)
