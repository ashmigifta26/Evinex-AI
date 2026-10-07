from pydantic import BaseModel
from typing import List, Optional, Any, Dict

class TableData(BaseModel):
    page: int
    table: List[List[str]]

class ImageData(BaseModel):
    page: int
    image_id: str

class PageData(BaseModel):
    page_number: int
    text: str
    tables: List[TableData] = []
    images: List[ImageData] = []

class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    total_pages: int
    pages: List[PageData]

class QuestionRequest(BaseModel):
    document_ids: List[str]
    question: str

class Evidence(BaseModel):
    page: int
    content: str
    type: str = "text"

class Source(BaseModel):
    document: str
    page: int

class QuestionResponse(BaseModel):
    answer: str
    sources: List[Source]
    evidence: List[Evidence]
    conflict_detected: bool = False
    message: Optional[str] = None
    confidence: Optional[str] = None
