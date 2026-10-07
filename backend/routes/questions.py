from fastapi import APIRouter, HTTPException
from models.schemas import QuestionRequest, QuestionResponse
from services.question_service import answer_question

router = APIRouter(prefix="/questions", tags=["Questions"])

@router.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    if not request.question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
        
    try:
        response = answer_question(request.document_id, request.question)
        return response
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to answer question: {str(e)}")
