from pinecone import Pinecone
from pinecone.exceptions import NotFoundException

from langchain_pinecone import PineconeVectorStore

from app.embeddings.huggingface import EmbeddingModel
from app.core.config import settings


class PineconeStore:

    _index = None
    _vector_store = None

    @classmethod
    def _get_index(cls):

        if cls._index is None:

            pc = Pinecone(
                api_key=settings.PINECONE_API_KEY
            )

            cls._index = pc.Index(
                settings.PINECONE_INDEX_NAME
            )

        return cls._index

    @classmethod
    def create(
        cls,
        documents
    ):

        embeddings = EmbeddingModel.get_model()

        index = cls._get_index()

        cls._vector_store = PineconeVectorStore(
            index=index,
            embedding=embeddings,
            text_key="text"
        )

        ids = [
            document.metadata["chunk_id"]
            for document in documents
        ]

        cls._vector_store.add_documents(
            documents=documents,
            ids=ids,
            namespace=settings.PINECONE_NAMESPACE
        )

        return cls._vector_store

    @classmethod
    def load(cls):

        if cls._vector_store is None:

            embeddings = EmbeddingModel.get_model()

            index = cls._get_index()

            cls._vector_store = PineconeVectorStore(
                index=index,
                embedding=embeddings,
                text_key="text"
            )

        return cls._vector_store

    @classmethod
    def similarity_search(
        cls,
        query,
        k=10
    ):

        store = cls.load()

        return store.similarity_search(
            query=query,
            k=k,
            namespace=settings.PINECONE_NAMESPACE
        )

    @classmethod
    def delete_all(cls):

        index = cls._get_index()

        try:

            index.delete(
                delete_all=True,
                namespace=settings.PINECONE_NAMESPACE
            )

        except NotFoundException:
            pass

        cls._vector_store = None