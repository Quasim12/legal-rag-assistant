import re

from enum import Enum


class Intent(Enum):

    GREETING = "greeting"

    METADATA = "metadata"

    RAG = "rag"


class IntentDetector:

    GREETING_PATTERNS = [

        r"^(hi|hello|hey)$",

        r"^good morning$",

        r"^good afternoon$",

        r"^good evening$"
    ]

    METADATA_PATTERNS = [

        # -------------------------
        # Total Articles
        # -------------------------

        r".*how many.*articles?.*",
        r".*number of.*articles?.*",
        r".*total.*articles?.*",
        r".*article count.*",

        # -------------------------
        # Total Pages
        # -------------------------

        r".*how many.*pages?.*",
        r".*number of.*pages?.*",
        r".*total.*pages?.*",
        r".*page count.*",

        # -------------------------
        # List Articles
        # -------------------------

        r".*list.*articles?.*",
        r".*all.*articles?.*",

        # -------------------------
        # Preamble
        # -------------------------

        r".*preamble.*",

        # -------------------------
        # Document Name
        # -------------------------

        r".*document.*name.*",
        r".*file.*name.*",
        r".*filename.*"
    ]

    def detect(
        self,
        query: str
    ):

        query = query.lower().strip()

        # -------------------------
        # Greeting
        # -------------------------

        for pattern in self.GREETING_PATTERNS:

            if re.search(
                pattern,
                query
            ):

                return Intent.GREETING

        # -------------------------
        # Metadata
        # -------------------------

        for pattern in self.METADATA_PATTERNS:

            if re.search(
                pattern,
                query
            ):

                return Intent.METADATA

        # -------------------------
        # Default
        # -------------------------

        return Intent.RAG