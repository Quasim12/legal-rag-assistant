import json
import shutil

from app.core.config import settings
from app.vectorstores.vector_factory import VectorStoreFactory


class DocumentService:

    METADATA_FILE = (
        settings.METADATA_DIR / "current_document.json"
    )

    @classmethod
    def save_document(
        cls,
        source_file: str,
        filename: str
    ):

        cls.delete_document()

        destination = (
            settings.UPLOADS_DIR / filename
        )

        shutil.copy2(
            source_file,
            destination
        )

        cls.METADATA_FILE.write_text(
            json.dumps(
                {
                    "filename": filename
                },
                indent=4
            )
        )

        return destination

    @classmethod
    def current_document(cls):

        if not cls.METADATA_FILE.exists():

            return None

        data = json.loads(
            cls.METADATA_FILE.read_text()
        )

        return data.get("filename")

    @classmethod
    def delete_document(cls):

        filename = cls.current_document()

        if filename:

            file_path = (
                settings.UPLOADS_DIR / filename
            )

            if file_path.exists():

                file_path.unlink()

        # Delete all vectors from Pinecone
        VectorStoreFactory.delete_all()

        # Delete BM25 index
        if settings.BM25_INDEX_PATH.exists():

            settings.BM25_INDEX_PATH.unlink()

        # Delete metadata
        if cls.METADATA_FILE.exists():

            cls.METADATA_FILE.unlink()

        VectorStoreFactory.clear_cache()