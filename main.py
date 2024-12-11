from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse
import os
import uuid

app = FastAPI()

# Directory to store uploaded images
UPLOAD_DIR = "uploaded_images"
API_URL = "https://image-api-szan.onrender.com"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get('/')
def home():
    return "Welcome home!"

@app.post("/upload/")
async def upload_image(user_id: str = Form(...), file: UploadFile = File(...)):
    """
    Upload an image and associate it with a user ID.
    :param user_id: The user's unique identifier
    :param file: The uploaded image file
    :return: JSON with the image URL
    """
    # Create a unique filename: <user_id>_<uuid>.ext
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{user_id}_profile_pic_{uuid.uuid4().hex}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # Save the file
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Generate a URL/path to return
    file_url = f"{API_URL}/{unique_filename}"
    
    return JSONResponse({"url": file_url})

@app.get(f"/{UPLOAD_DIR}/{{filename}}")
async def serve_image(filename: str):
    """
    Serve images from the upload directory.
    """
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        return JSONResponse({"error": "File not found"}, status_code=404)
    return FileResponse(file_path)
