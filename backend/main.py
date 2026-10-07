from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import documents, questions

app = FastAPI(
    title="DocuProof AI",
    description="Multimodal Document Intelligence Backend",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router)
app.include_router(questions.router)

@app.get("/")
def read_root():
    return {"message": "DocuProof AI Backend is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
