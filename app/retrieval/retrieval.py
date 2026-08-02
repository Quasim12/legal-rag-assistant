from app.vectorstores.vector_factory import VectorStoreFactory


class Retriever:

    def __init__(self):

        if not VectorStoreFactory.exists():

            raise RuntimeError(
                "Vector stores are not initialized. Please upload a document first."
            )

    def vector_search(
        self,
        query: str,
        k: int = 10
    ):

        return VectorStoreFactory.search_vector(
            query=query,
            k=k
        )

    def keyword_search(
        self,
        query: str,
        k: int = 10
    ):

        return VectorStoreFactory.search_keyword(
            query=query,
            k=k
        )