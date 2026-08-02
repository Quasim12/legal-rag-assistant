import json
import re

from app.core.config import settings


class DocumentMetadataService:

    @staticmethod
    def save(documents, filename):

        full_text = "\n".join(
            document.page_content
            for document in documents
        )

        # Detect Articles (Numeric + Roman)
        matches = re.finditer(
            r"\bArticle\s+([IVXLCDM]+|\d+)\b",
            full_text,
            flags=re.IGNORECASE
        )

        article_numbers = []

        first_article_position = None

        for match in matches:

            if first_article_position is None:

                first_article_position = match.start()

            value = match.group(1)

            if value.isdigit():

                article_numbers.append(
                    int(value)
                )

        article_numbers = sorted(
            set(article_numbers)
        )

        # Detect Preamble
        has_preamble = False

        if first_article_position is not None:

            before_first_article = full_text[
                :first_article_position
            ].strip()

            has_preamble = len(
                before_first_article
            ) > 50

        metadata = {

            "filename": filename,

            "total_pages": max(
                document.metadata.get("page", 0)
                for document in documents
            ) + 1,

            "total_articles": len(
                article_numbers
            ),

            "articles": article_numbers,

            "has_preamble": has_preamble,

            "document_type": "legal"
        }

        with open(
            settings.DOCUMENT_METADATA_PATH,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                metadata,
                file,
                indent=4
            )

    @staticmethod
    def load():

        if not settings.DOCUMENT_METADATA_PATH.exists():

            return None

        with open(
            settings.DOCUMENT_METADATA_PATH,
            encoding="utf-8"
        ) as file:

            return json.load(file)