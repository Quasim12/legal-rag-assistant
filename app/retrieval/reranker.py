from typing import List

from sentence_transformers import CrossEncoder


class CrossEncoderReranker:

    _model = None

    @classmethod
    def get_model(cls):

        if cls._model is None:

            cls._model = CrossEncoder(
                "cross-encoder/ms-marco-MiniLM-L-6-v2"
            )

        return cls._model

    def rerank(
        self,
        query: str,
        documents: List,
        top_k: int = 5
    ):

        if not documents:
            return []

        model = self.get_model()

        pairs = [
            (query, doc.page_content)
            for doc in documents
        ]

        scores = model.predict(
            pairs
        )

        ranked_documents = sorted(
            zip(documents, scores),
            key=lambda item: item[1],
            reverse=True
        )

        return [
            document
            for document, _ in ranked_documents[:top_k]
        ]