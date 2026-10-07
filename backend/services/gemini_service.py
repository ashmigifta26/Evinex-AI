import google.generativeai as genai
from config import GEMINI_API_KEY
import json
import PIL.Image

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def ask_gemini(question: str, context: str, image_paths: list = None):
    if not GEMINI_API_KEY:
        return {
            "answer": "Error: Gemini API key not configured.",
            "sources": [],
            "confidence": "low"
        }
        
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    You are DocuProof AI, a document answering assistant.
    You must answer the user's question based ONLY on the provided document context and images.
    If the context does not contain enough information to answer the question, say "Insufficient evidence found in the uploaded documents."
    Distinguish between information directly stated and information calculated.
    If you make a calculation, show it.
    If you find conflicting evidence between tables and charts, point it out.
    
    Format your response strictly as JSON with these keys:
    - answer (string): The answer to the question.
    - sources (list of ints): The page numbers from the context used to answer.
    
    Context:
    {context}
    
    Question: {question}
    """
    
    contents = [prompt]
    if image_paths:
        for img_path in image_paths:
            try:
                img = PIL.Image.open(img_path)
                contents.append(img)
            except Exception as e:
                print(f"Error loading image {img_path}: {e}")
    
    try:
        response = model.generate_content(contents, generation_config={"response_mime_type": "application/json"})
        return json.loads(response.text)
    except Exception as e:
        print(f"Gemini error: {e}")
        return {
            "answer": "Failed to generate answer due to an internal error.",
            "sources": [],
            "confidence": "low"
        }
