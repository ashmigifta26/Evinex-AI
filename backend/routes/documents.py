from fastapi import APIRouter, UploadFile, File, HTTPException
from models.schemas import DocumentUploadResponse
from utils.file_utils import save_upload_file
from services.pdf_service import process_pdf, get_document
from config import UPLOAD_DIR

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
    document_id, file_path = save_upload_file(file, UPLOAD_DIR)
    
    try:
        response = process_pdf(document_id, file_path, file.filename)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

@router.get("/{document_id}", response_model=DocumentUploadResponse)
async def retrieve_document(document_id: str):
    doc = get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc
