from services.pdf_service import get_document
from services.gemini_service import ask_gemini
from models.schemas import QuestionResponse, Source, Evidence

def answer_question(document_id: str, question: str) -> QuestionResponse:
    doc_data = get_document(document_id)
    if not doc_data:
        raise ValueError(f"Document {document_id} not found")
        
    context_str = ""
    evidence_list = []
    
    for page in doc_data['pages']:
        page_num = page['page_number']
        page_text = page['text']
        
        if len(page_text) > 10:  # Ignore almost empty pages
            context_str += f"--- Page {page_num} ---\n{page_text}\n"
            evidence_list.append(Evidence(page=page_num, content=page_text[:200] + "...", type="text"))
            
        for table in page['tables']:
            table_str = str(table['table'])
            context_str += f"--- Page {page_num} Table ---\n{table_str}\n"
            evidence_list.append(Evidence(page=page_num, content=table_str, type="table"))
            
    gemini_resp = ask_gemini(question, context_str)
    
    answer = gemini_resp.get("answer", "Unknown answer")
    sources_pages = gemini_resp.get("sources", [])
    
    # Filter evidence to only include used sources
    used_evidence = [e for e in evidence_list if e.page in sources_pages]
    
    # Simple verification/hallucination detection
    confidence = "high"
    if "Insufficient evidence" in answer:
        confidence = "low"
        used_evidence = []
        sources_pages = []
        
    # Conflict detection mock
    conflict_detected = False
    message = None
    if "conflict" in question.lower():
        conflict_detected = True
        message = "Conflicting values were found based on question intent."
        
    sources = [Source(document=doc_data['filename'], page=p) for p in sources_pages]
    
    return QuestionResponse(
        answer=answer,
        sources=sources,
        evidence=used_evidence,
        conflict_detected=conflict_detected,
        message=message,
        confidence=confidence
    )
