import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings:

    # ==========================
    # Base Directories
    # ==========================

    BASE_DIR = BASE_DIR

    DATA_DIR = BASE_DIR / "data"

    UPLOADS_DIR = DATA_DIR / "uploads"

    VECTORSTORE_DIR = DATA_DIR / "vectorstore"

    METADATA_DIR = DATA_DIR / "metadata"

    # ==========================
    # Pinecone
    # ==========================

    PINECONE_API_KEY = os.getenv(
        "PINECONE_API_KEY"
    )

    PINECONE_INDEX_NAME = os.getenv(
        "PINECONE_INDEX_NAME"
    )

    # NEW
    PINECONE_NAMESPACE = os.getenv(
        "PINECONE_NAMESPACE",
        "lawyer-rag"
    )

    # ==========================
    # BM25
    # ==========================

    BM25_INDEX_PATH = (
        VECTORSTORE_DIR / "bm25.pkl"
    )

    # ==========================
    # Document Metadata
    # ==========================

    DOCUMENT_METADATA_PATH = (
        METADATA_DIR / "document_metadata.json"
    )
    # ==========================
    # Create Directories
    # ==========================

    @classmethod
    def create_directories(cls):

        cls.DATA_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        cls.UPLOADS_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        cls.VECTORSTORE_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        cls.METADATA_DIR.mkdir(
            parents=True,
            exist_ok=True
        )


settings = Settings()

settings.create_directories()