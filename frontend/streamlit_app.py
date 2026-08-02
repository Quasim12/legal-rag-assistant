import os
import tempfile

import streamlit as st

from app.services.chat_service import ChatService
from app.services.ingestion_service import IngestionService
from app.services.document_service import DocumentService
from app.vectorstores.vector_factory import VectorStoreFactory


st.set_page_config(
    page_title="LegalMind AI",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ LegalMind AI")
st.write("AI-Powered Legal Research & Document Assistant")


# ==========================
# Session State
# ==========================

if "chat_service" not in st.session_state:
    st.session_state.chat_service = ChatService()

if "document_loaded" not in st.session_state:
    st.session_state.document_loaded = VectorStoreFactory.exists()

if "upload_done" not in st.session_state:
    st.session_state.upload_done = False

ingestion_service = IngestionService()


# ==========================
# Current Document
# ==========================

current_document = DocumentService.current_document()

if current_document:

    st.success(f"📄 Current Document : {current_document}")

    if st.button("🗑 Delete Current Document"):

        DocumentService.delete_document()

        st.session_state.document_loaded = False
        st.session_state.upload_done = False

        st.success("Document deleted successfully.")

        st.rerun()


# ==========================
# Upload
# ==========================

uploaded_file = st.file_uploader(
    "Upload Document",
    type=["pdf", "docx", "txt"]
)

if uploaded_file is not None:

    if (
        st.session_state.upload_done
        and current_document == uploaded_file.name
    ):
        pass

    else:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=os.path.splitext(uploaded_file.name)[1]
        ) as temp_file:

            temp_file.write(uploaded_file.getvalue())
            temp_path = temp_file.name

        with st.spinner("Creating Vector Database..."):

            ingestion_service.ingest(
                file_path=temp_path,
                filename=uploaded_file.name
            )

        st.session_state.document_loaded = True
        st.session_state.upload_done = True

        os.remove(temp_path)

        st.success("Document indexed successfully.")

        st.rerun()


# ==========================
# Question
# ==========================

user_query = st.text_area(
    "Ask your question",
    height=150
)

if st.button("Ask AI Lawyer"):

    if not user_query.strip():

        st.warning("Please enter a question.")
        st.stop()

    if not st.session_state.document_loaded:

        st.warning("Please upload a document first.")
        st.stop()

    with st.spinner("Thinking..."):

        try:

            answer = (
                st.session_state
                .chat_service
                .chat(user_query)
            )

            st.chat_message("user").write(user_query)
            st.chat_message("assistant").write(answer)

        except Exception as e:

            st.error(str(e))