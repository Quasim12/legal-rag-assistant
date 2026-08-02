import streamlit as st

from vector_database import (
    upload_pdf,
    load_default_faiss,
    create_uploaded_pdf_faiss
)

from rag_pipeline import answer_query

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="AI Lawyer RAG",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ AI Lawyer RAG")

st.write(
    "Ask questions from the default Human Rights document or upload your own PDF."
)

# -----------------------------
# INPUTS
# -----------------------------

uploaded_file = st.file_uploader(
    "Upload PDF (Optional)",
    type=["pdf"]
)

user_query = st.text_area(
    "Ask your question",
    height=150
)

# -----------------------------
# BUTTON
# -----------------------------

if st.button("Ask AI Lawyer"):

    if not user_query.strip():
        st.warning("Please enter your question.")
        st.stop()

    with st.spinner("Thinking..."):

        try:

            # Uploaded PDF
            if uploaded_file is not None:

                file_path = upload_pdf(uploaded_file)

                faiss_db = create_uploaded_pdf_faiss(file_path)

            # Default PDF
            else:

                faiss_db = load_default_faiss()

            response = answer_query(
                faiss_db=faiss_db,
                query=user_query
            )

            st.chat_message("user").write(user_query)
            st.chat_message("assistant").write(response)

        except Exception as e:
            st.error(e)