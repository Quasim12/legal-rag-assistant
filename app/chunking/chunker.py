import re

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class Chunker:

    def __init__(
        self,
        chunk_size: int = 1200,
        chunk_overlap: int = 150
    ):

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def create_chunks(self, documents):

        final_chunks = []

        for document in documents:

            page_text = document.page_content.strip()

            if not page_text:
                continue

            # Split whenever a new Article starts
            sections = re.split(
                r'(?=Article\s+\d+\b)',
                page_text,
                flags=re.IGNORECASE
            )

            for section_text in sections:

                section_text = section_text.strip()

                if not section_text:
                    continue

                metadata = document.metadata.copy()

                match = re.search(
                    r'Article\s+(\d+)',
                    section_text,
                    flags=re.IGNORECASE
                )

                if match:

                    metadata["article"] = int(match.group(1))

                else:
                    # Anything before Article 1 is treated as Preamble
                    metadata["section"] = "preamble"

                    # Make preamble easier to retrieve
                    if not section_text.lower().startswith("preamble"):
                        section_text = "Preamble\n\n" + section_text

                section_doc = Document(
                    page_content=section_text,
                    metadata=metadata
                )

                # Split only if section is too large
                if len(section_text) > self.text_splitter._chunk_size:

                    sub_chunks = self.text_splitter.split_documents(
                        [section_doc]
                    )

                    for index, chunk in enumerate(sub_chunks):

                        chunk.metadata["part"] = index + 1

                        final_chunks.append(chunk)

                else:

                    final_chunks.append(section_doc)

        return final_chunks