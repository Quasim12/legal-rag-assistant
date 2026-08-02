import os

from app.core.config import settings

from app.vectorstores.pinecone_store import PineconeStore
from app.vectorstores.bm25_store import BM25Store


class VectorStoreFactory:

    _pinecone_store = None

    _bm25_store = None

    @classmethod
    def create(
        cls,
        chunks
    ):

        cls._pinecone_store = PineconeStore.create(
            chunks
        )

        cls._bm25_store = BM25Store.create(
            chunks
        )

        BM25Store.save(
            cls._bm25_store,
            settings.BM25_INDEX_PATH
        )

        return {
            "pinecone": cls._pinecone_store,
            "bm25": cls._bm25_store
        }

    @classmethod
    def exists(cls):

        return os.path.exists(
            settings.BM25_INDEX_PATH
        )

    @classmethod
    def load(cls):

        cls._pinecone_store = (
            PineconeStore.load()
        )

        if cls._bm25_store is None:

            cls._bm25_store = BM25Store.load(
                settings.BM25_INDEX_PATH
            )

        return {
            "pinecone": cls._pinecone_store,
            "bm25": cls._bm25_store
        }

    @classmethod
    def search_vector(
        cls,
        query: str,
        k: int = 10
    ):

        store = PineconeStore.load()

        return store.similarity_search(
            query=query,
            k=k
        )

    @classmethod
    def search_keyword(
        cls,
        query: str,
        k: int = 10
    ):

        if cls._bm25_store is None:

            cls._bm25_store = BM25Store.load(
                settings.BM25_INDEX_PATH
            )

        cls._bm25_store.k = k

        return cls._bm25_store.invoke(
            query
        )

    @classmethod
    def clear_cache(cls):

        cls._pinecone_store = None

        cls._bm25_store = None

    @classmethod
    def reload(cls):

        cls.clear_cache()

        return cls.load()

    @classmethod
    def delete_all(cls):

        PineconeStore.delete_all()

        if os.path.exists(
            settings.BM25_INDEX_PATH
        ):

            os.remove(
                settings.BM25_INDEX_PATH
            )

        cls.clear_cache()