import fitz
import os
from models.schemas import PageData, TableData, ImageData, DocumentUploadResponse
from services.table_service import extract_tables
from services.image_service import extract_images
from config import UPLOAD_DIR

# Simple in-memory store for documents during the hackathon
DOCUMENT_STORE = {}

def process_pdf(document_id: str, file_path: str, filename: str) -> DocumentUploadResponse:
    doc = fitz.open(file_path)
    total_pages = len(doc)
    
    tables_by_page = extract_tables(file_path)
    images_by_page = extract_images(file_path, UPLOAD_DIR, document_id)
    
    pages_data = []
    for i in range(total_pages):
        page = doc[i]
        text = page.get_text()
        page_num = i + 1
        
        page_tables = []
        if page_num in tables_by_page:
            for table in tables_by_page[page_num]:
                # Clean up None values
                clean_table = [[str(cell) if cell is not None else "" for cell in row] for row in table]
                page_tables.append(TableData(page=page_num, table=clean_table))
                
        page_images = []
        if page_num in images_by_page:
            for img_id in images_by_page[page_num]:
                page_images.append(ImageData(page=page_num, image_id=img_id))
        
        pages_data.append(PageData(
            page_number=page_num,
            text=text.strip(),
            tables=page_tables,
            images=page_images
        ))
        
    response = DocumentUploadResponse(
        document_id=document_id,
        filename=filename,
        total_pages=total_pages,
        pages=pages_data
    )
    
    DOCUMENT_STORE[document_id] = response.model_dump()
    return response

def get_document(document_id: str):
    return DOCUMENT_STORE.get(document_id)
