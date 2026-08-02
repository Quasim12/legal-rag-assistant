import re

from app.services.document_metadata_service import (
    DocumentMetadataService
)


class MetadataQueryService:

    def __init__(self):

        self.metadata = (
            DocumentMetadataService.load()
        )

        self.patterns = [

            (
                [
                    r"how many articles?",
                    r"number of articles?",
                    r"total articles?",
                    r"article count"
                ],
                self.total_articles
            ),

            (
                [
                    r"how many pages?",
                    r"number of pages?",
                    r"total pages?",
                    r"page count"
                ],
                self.total_pages
            ),

            (
                [
                    r"list articles?",
                    r"list all articles?",
                    r"all articles?"
                ],
                self.list_articles
            ),

            (
                [
                    r".*preamble.*"
                ],
                self.preamble
            ),

            (
                [
                    r"document name",
                    r"file name",
                    r"filename"
                ],
                self.document_name
            )
        ]

    def answer(
        self,
        question: str
    ):

        if self.metadata is None:

            return None

        query = question.lower().strip()

        for patterns, handler in self.patterns:

            for pattern in patterns:

                if re.search(
                    pattern,
                    query
                ):

                    return handler()

        return None

    # ----------------------------------------------------
    # Handlers
    # ----------------------------------------------------

    def total_articles(self):

        return (
            f"This document contains "
            f"{self.metadata['total_articles']} articles."
        )

    def total_pages(self):

        return (
            f"This document contains "
            f"{self.metadata['total_pages']} pages."
        )

    def list_articles(self):

        articles = ", ".join(
            map(
                str,
                self.metadata["articles"]
            )
        )

        return (
            "The document contains the following articles: "
            f"{articles}."
        )

    def preamble(self):

        if self.metadata["has_preamble"]:

            return (
                "Yes, this document contains a preamble."
            )

        return (
            "No, this document does not contain a preamble."
        )

    def document_name(self):

        return self.metadata["filename"]