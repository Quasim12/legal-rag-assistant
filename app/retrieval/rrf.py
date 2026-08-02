from collections import defaultdict
from typing import List


class ReciprocalRankFusion:

    def __init__(
        self,
        k: int = 60
    ):
        self.k = k

    def _get_document_id(
        self,
        document
    ):

        metadata = getattr(document, "metadata", {})

        if "chunk_id" in metadata:
            return metadata["chunk_id"]

        if "id" in metadata:
            return metadata["id"]

        if "source" in metadata and "page" in metadata:
            return f"{metadata['source']}_{metadata['page']}_{hash(document.page_content)}"

        return str(hash(document.page_content))

    def fuse(
        self,
        vector_results: List,
        keyword_results: List
    ):

        scores = defaultdict(float)

        documents = {}

        for rank, document in enumerate(vector_results, start=1):

            doc_id = self._get_document_id(document)

            documents[doc_id] = document

            scores[doc_id] += 1 / (self.k + rank)

        for rank, document in enumerate(keyword_results, start=1):

            doc_id = self._get_document_id(document)

            documents[doc_id] = document

            scores[doc_id] += 1 / (self.k + rank)

        ranked = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True
        )

        return [
            documents[doc_id]
            for doc_id, _ in ranked
        ]