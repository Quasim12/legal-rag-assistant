import pickle

from langchain_community.retrievers import BM25Retriever


class BM25Store:

    @staticmethod
    def create(
        documents,
        k=5
    ):

        retriever = BM25Retriever.from_documents(
            documents
        )

        retriever.k = k

        return retriever

    @staticmethod
    def save(
        retriever,
        save_path
    ):

        with open(save_path, "wb") as file:

            pickle.dump(
                retriever,
                file
            )

    @staticmethod
    def load(
        save_path
    ):

        with open(save_path, "rb") as file:

            return pickle.load(file)