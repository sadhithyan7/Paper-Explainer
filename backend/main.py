import os
# pyrefly: ignore [missing-import]
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from ingest import ingest_pdf
from qa import get_answer

app = FastAPI(title="Paper Explainer API")

# allow frontend to hit backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# make sure uploads dir exists
os.makedirs("../uploads", exist_ok=True)

class QuestionRequest(BaseModel):
    question: str

@app.get("/health")
def health_check():
    """api health check"""
    return {"status": "running"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """handles pdf upload and starts ingestion"""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
    try:
        # save file locally
        file_path = os.path.join("../uploads", file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
            
        # process pdf and dump into chromadb
        result_message = ingest_pdf(file_path)
        
        # handle ingest errors
        if result_message.startswith("Error"):
            raise HTTPException(status_code=500, detail=result_message)
            
        return {"status": "success", "message": result_message}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")

@app.post("/ask")
def ask_question(req: QuestionRequest):
    """gets answer from llm based on user question"""
    try:
        result = get_answer(req.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get answer: {str(e)}")

# run backend
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
