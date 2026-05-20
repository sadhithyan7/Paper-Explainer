import os
import chromadb
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv(dotenv_path="../.env")
load_dotenv()

COLLECTION_NAME = "paper_explainer"

def get_answer(question: str) -> dict:
    """query chromadb and use gemini for the answer"""
    db_path = os.path.abspath("../chroma_db")
    if not os.path.exists(db_path):
        return {
            "answer": "No documents found. Please upload and process a PDF first!",
            "sources": []
        }

    try:
        # connect to chroma
        client = chromadb.PersistentClient(path=db_path)
        collection = client.get_collection(COLLECTION_NAME)

        # embed user question
        embed_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2")
        query_embedding = embed_model.embed_query(question)

        # get top 5 chunks
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5
        )

        # extract docs and metadata
        docs = results["documents"][0]
        metas = results["metadatas"][0]

        formatted_context = "\n\n".join(docs)
        sources = list(set(f"Page {m.get('page', 'Unknown')}" for m in metas))

        # use gemini flash for fast response
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.2
        )

        template = """You are an expert research paper assistant for students.
You MUST answer using ONLY the context provided below from the research paper.
Be specific, direct, and concise. Extract exact information like titles, authors, dates, and key findings.

Context from the research paper:
{context}

Student's Question: {question}

Answer (be specific and cite exact details from the context):"""

        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | llm | StrOutputParser()

        answer = chain.invoke({
            "context": formatted_context,
            "question": question
        })

        return {"answer": answer, "sources": sources}

    except Exception as e:
        if "does not exist" in str(e):
            return {
                "answer": "No processed paper found. Please upload and process a PDF first.",
                "sources": []
            }
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            return {
                "answer": "Google API rate limit hit. Please wait 60 seconds and try again.",
                "sources": []
            }
        return {
            "answer": f"Error: {str(e)}",
            "sources": []
        }
