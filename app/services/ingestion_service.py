from pathlib import Path

from app.loaders.pdf_loader import PDFLoader
from app.loaders.docx_loader import DocxLoader
from app.loaders.text_loader import TextLoader

from app.chunking.chunker import Chunker

from app.vectorstores.vector_factory import VectorStoreFactory
from app.services.document_service import DocumentService
from app.services.document_metadata_service import DocumentMetadataService

class IngestionService:

    def __init__(self):

        self.chunker = Chunker()

    def ingest(
        self,
        file_path: str,
        filename: str
    ):

        saved_file = DocumentService.save_document(
            source_file=file_path,
            filename=filename
        )

        extension = Path(saved_file).suffix.lower()

        if extension == ".pdf":

            documents = PDFLoader.load(
                str(saved_file)
            )

        elif extension == ".docx":

            documents = DocxLoader.load(
                str(saved_file)
            )

        elif extension == ".txt":

            documents = TextLoader.load(
                str(saved_file)
            )

        else:

            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        chunks = self.chunker.create_chunks(
            documents
        )

        # Add metadata
        for index, chunk in enumerate(chunks):

            chunk.metadata["chunk_id"] = f"{filename}_{index}"

            chunk.metadata["filename"] = filename

            chunk.metadata["source"] = filename

            chunk.metadata["page"] = chunk.metadata.get("page", 0)

        DocumentMetadataService.save(
            documents=documents,
            filename=filename
        )    

        VectorStoreFactory.create(
            chunks
        )

        return saved_file