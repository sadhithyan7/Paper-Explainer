import streamlit as st
# pyrefly: ignore [missing-import]
import requests

# api url
API_URL = "http://localhost:8000"

st.set_page_config(page_title="Paper Explainer for Students", page_icon="📄")

st.title("Paper Explainer for Students")
st.write("Upload a research paper and ask questions to understand it better!")

# setup session state for chat
if "paper_loaded" not in st.session_state:
    st.session_state["paper_loaded"] = False
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

st.header("Step 1: Upload Paper")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    if st.button("Process Paper"):
        with st.spinner("Processing PDF and generating embeddings..."):
            try:
                # post file to backend
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                response = requests.post(f"{API_URL}/upload", files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"Success! {data['message']}")
                    st.session_state["paper_loaded"] = True
                else:
                    error_detail = response.json().get("detail", "Unknown error occurred")
                    st.error(f"Error processing paper: {error_detail}")
            except requests.exceptions.ConnectionError:
                st.error("Error: Could not connect to backend. Is the FastAPI server running?")

if st.session_state["paper_loaded"]:
    st.header("Step 2: Ask Questions")
    
    # question input
    question = st.text_input("What would you like to know about the paper?")
    
    if st.button("Ask"):
        if question.strip() == "":
            st.warning("Please enter a question.")
        else:
            with st.spinner("Thinking..."):
                try:
                    # ask backend
                    response = requests.post(f"{API_URL}/ask", json={"question": question})
                    
                    if response.status_code == 200:
                        data = response.json()
                        answer = data["answer"]
                        sources = data["sources"]
                        
                        # prepend to history
                        st.session_state["chat_history"].insert(0, {
                            "question": question,
                            "answer": answer,
                            "sources": sources
                        })
                    else:
                        st.error("Error generating answer. Please try again.")
                except requests.exceptions.ConnectionError:
                    st.error("Error: Could not connect to backend.")

    # render chat
    if st.session_state["chat_history"]:
        st.subheader("Chat History")
        for chat in st.session_state["chat_history"]:
            with st.container():
                st.info(f"**Q:** {chat['question']}")
                st.write(chat['answer'])
                if chat['sources']:
                    st.caption(f"Sources: {', '.join(chat['sources'])}")
                st.divider()
