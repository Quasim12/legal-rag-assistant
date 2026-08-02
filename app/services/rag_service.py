from app.retrieval.hybrid_search import HybridSearch

from app.prompts.prompt_templates import PromptTemplates
from app.llms.llm_factory import LLMFactory


class RAGService:

    def __init__(self):

        # Lazy initialization
        self.hybrid_search = None

        self.llm = LLMFactory.get_llm()

    @staticmethod
    def build_context(documents):

        return "\n\n".join(
            document.page_content
            for document in documents
        )

    def answer(
        self,
        question: str
    ):

        if self.hybrid_search is None:

            self.hybrid_search = HybridSearch()

        documents = self.hybrid_search.search(
            query=question,
            retrieval_k=20,
            rerank_top_k=5
        )

        if not documents:

            return {
                "answer": (
                    "I couldn't find any relevant information "
                    "in the uploaded document."
                ),
                "sources": []
            }

        context = self.build_context(
            documents
        )

        prompt = PromptTemplates.legal_rag_prompt()

        chain = prompt | self.llm

        response = chain.invoke(
            {
                "question": question,
                "context": context
            }
        )

        return {
            "answer": response.content,
            "sources": documents
        }