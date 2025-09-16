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



with open("output.md", "w") as f:
    f.write(combined_markdown)
