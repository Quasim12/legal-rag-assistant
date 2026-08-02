from app.retrieval.retrieval import Retriever
from app.retrieval.rrf import ReciprocalRankFusion
from app.retrieval.reranker import CrossEncoderReranker


class HybridSearch:

    def __init__(self):

        self.retriever = Retriever()

        self.rrf = ReciprocalRankFusion()

        self.reranker = CrossEncoderReranker()

    def search(
        self,
        query: str,
        retrieval_k: int = 20,
        rerank_top_k: int = 5
    ):

        vector_results = self.retriever.vector_search(
            query=query,
            k=retrieval_k
        )

        keyword_results = self.retriever.keyword_search(
            query=query,
            k=retrieval_k
        )

        if not vector_results and not keyword_results:

            return []

        fused_documents = self.rrf.fuse(
            vector_results=vector_results,
            keyword_results=keyword_results
        )

        reranked_documents = self.reranker.rerank(
            query=query,
            documents=fused_documents,
            top_k=rerank_top_k
        )

        return reranked_documents