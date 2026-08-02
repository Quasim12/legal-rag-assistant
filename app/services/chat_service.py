from app.services.rag_service import RAGService
from app.services.metadata_query_service import (
    MetadataQueryService
)

from app.retrieval.intent_detector import (
    IntentDetector,
    Intent
)


class ChatService:

    def __init__(self):

        self.intent_detector = IntentDetector()

        self.metadata_service = (
            MetadataQueryService()
        )

        # Lazy initialization
        self.rag_service = None

    def chat(
        self,
        question: str
    ):

        intent = self.intent_detector.detect(
            question
        )

        # -------------------------
        # Greeting
        # -------------------------

        if intent == Intent.GREETING:

            return "Hello! How can I help you today?"

        # -------------------------
        # Metadata Queries
        # -------------------------

        if intent == Intent.METADATA:

            metadata_answer = (
                self.metadata_service.answer(
                    question
                )
            )

            if metadata_answer is not None:

                return metadata_answer

        # -------------------------
        # RAG
        # -------------------------

        if self.rag_service is None:

            self.rag_service = RAGService()

        response = self.rag_service.answer(
            question
        )

        return response["answer"]