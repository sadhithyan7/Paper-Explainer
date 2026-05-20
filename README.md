# Paper Explainer for Students

A tool designed for students to easily upload complex research papers (PDFs) and ask questions to understand them better. Built specifically to run efficiently using local vector embeddings and the free tier of Google's Gemini 1.5 Flash.

## Tech Stack
- **Backend:** FastAPI, Uvicorn
- **Frontend:** Streamlit
- **LLM Engine:** LangChain, Google Gemini 1.5 Flash
- **Vector Database:** ChromaDB
- **Embeddings:** HuggingFace sentence-transformers (Local)

## Setup Instructions

### 1. Clone or create the project folder
Navigate to your desired directory and ensure all project files are present.

### 2. Create and activate a virtual environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup environment variables
Copy `.env.example` to `.env` and add your free Gemini API key:
```bash
cp .env.example .env
```
Get your free API key from [Google AI Studio](https://aistudio.google.com).

### 5. Run the Backend API
In your first terminal:
```bash
cd backend
uvicorn main:app --reload
```

### 6. Run the Frontend UI
Open a second terminal, activate the virtual environment, and run:
```bash
cd frontend
streamlit run app.py
```

## How to Use
1. **Upload**: Open the Streamlit web interface and upload a `.pdf` research paper.
2. **Process**: Click "Process Paper" to chunk the text and create local embeddings.
3. **Ask**: Type a question about the paper and receive an AI-generated answer with page citations.

## Week 1 Features Implemented
- Basic FastAPI backend with `/health`, `/upload`, and `/ask` endpoints.
- Streamlit frontend with a simple, sequential step-by-step UI.
- Free local embeddings generation using `sentence-transformers`.
- Integration with Google Gemini free tier via `langchain-google-genai`.
- Document chunking, persisting to local ChromaDB, and RetrievalQA integration.

## GitHub Commit Checklist
1. `Initial commit: project structure and requirements`
2. `feat: add environment config and backend skeleton`
3. `feat: implement PDF ingestion and ChromaDB vector store`
4. `feat: implement LangChain QA retrieval with Gemini 1.5 Flash`
5. `feat: complete FastAPI endpoints and CORS setup`
6. `feat: add Streamlit frontend with API integration`
