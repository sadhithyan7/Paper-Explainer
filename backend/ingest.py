import os
import chromadb
from dotenv import load_dotenv
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv(dotenv_path="../.env")
load_dotenv()

COLLECTION_NAME = "paper_explainer"

def ingest_pdf(file_path: str) -> str:
    """loads pdf, chunks it, embeds and stores in chroma"""
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"
    
    try:
        # load pdf
        loader = PyMuPDFLoader(file_path)
        documents = loader.load()
        
        if not documents:
            return "Error: Could not extract text from this PDF."
        
        # split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=100
        )
        chunks = text_splitter.split_documents(documents)
        
        # embed chunks using gemini
        embed_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2")
        texts = [chunk.page_content for chunk in chunks]
        embeddings = [embed_model.embed_query(text) for text in texts]
        
        # store in chromadb directly
        db_path = os.path.abspath("../chroma_db")
        client = chromadb.PersistentClient(path=db_path)
        
        # wipe old db collection to avoid conflicts on re-upload
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass
        
        collection = client.create_collection(COLLECTION_NAME)
        
        # insert everything into chroma
        collection.add(
            ids=[f"chunk_{i}" for i in range(len(chunks))],
            embeddings=embeddings,
            documents=texts,
            metadatas=[chunk.metadata for chunk in chunks]
        )
        
        return f"Successfully processed {len(chunks)} chunks from {len(documents)} pages."
        
    except Exception as e:
        return f"Error processing PDF: {str(e)}"
