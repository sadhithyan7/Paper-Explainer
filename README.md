# Paper Explainer for Students

A tool for students to upload research papers (PDFs) and ask questions to make them easier to understand. Built using FastAPI for the backend, Streamlit for the frontend, and Google Gemini for the brain.

## Tech Stack
- **Backend:** FastAPI, Uvicorn
- **Frontend:** Streamlit
- **LLM & Embeddings:** Google Gemini 2.5 Flash & gemini-embedding-2
- **Vector DB:** ChromaDB (queried natively to keep it fast)
- **PDF Parsing:** PyMuPDF (fast and doesn't crash on complex layouts)

## Setup Instructions

### 1. Set up virtual environment
Create a Python virtual environment so package dependencies don't conflict:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 2. Install dependencies
Install all the required Python packages:
```bash
pip install -r requirements.txt
```

### 3. Setup environment variables
Copy `.env.example` to `.env` and add your free Gemini API key:
```bash
# Copy the file manually or run:
cp .env.example .env
```
You can get a free API key from [Google AI Studio](https://aistudio.google.com).

### 4. Run the backend API
Open a terminal, activate your virtual environment, and run the backend server:
```bash
cd backend
python main.py
```

### 5. Run the frontend UI
Open a second terminal, activate the virtual environment, and start the Streamlit app:
```bash
cd frontend
streamlit run app.py
```

## Features Implemented
- FastAPI backend endpoints (`/health`, `/upload`, `/ask`).
- Step-by-step Streamlit interface for uploading and questioning.
- PyMuPDF to extract text from papers quickly without format crashes.
- Google Cloud embeddings to keep local RAM usage at 0MB.
- Native ChromaDB client integration to avoid LangChain wrapper issues.
- Quick answers using Gemini 2.5 Flash.
