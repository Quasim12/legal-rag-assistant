from pathlib import Path


class Validators:

    SUPPORTED_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".txt"
    }

    @classmethod
    def validate_file(cls, file_path: str):

        extension = Path(file_path).suffix.lower()

        if extension not in cls.SUPPORTED_EXTENSIONS:

            raise ValueError(
                f"Unsupported file type: {extension}"
            )

    @staticmethod
    def validate_question(question: str):

        if not question.strip():

            raise ValueError(
                "Question cannot be empty."
            )