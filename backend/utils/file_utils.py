import uuid
import os
import shutil
from fastapi import UploadFile

def save_upload_file(upload_file: UploadFile, destination: str) -> str:
    document_id = f"doc_{uuid.uuid4().hex[:8]}"
    file_path = os.path.join(destination, f"{document_id}_{upload_file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return document_id, file_path
