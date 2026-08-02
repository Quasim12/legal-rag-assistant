import os
import uuid
from pathlib import Path


class Helpers:

    @staticmethod
    def generate_uuid():

        return str(uuid.uuid4())

    @staticmethod
    def get_file_extension(file_path: str):

        return Path(file_path).suffix.lower()

    @staticmethod
    def file_exists(file_path: str):

        return os.path.exists(file_path)

    @staticmethod
    def ensure_directory(directory: str):

        os.makedirs(
            directory,
            exist_ok=True
        )

    @staticmethod
    def format_context(documents):

        return "\n\n".join(
            document.page_content
            for document in documents
        )