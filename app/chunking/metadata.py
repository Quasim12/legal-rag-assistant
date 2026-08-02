from pathlib import Path


class MetadataBuilder:

    @staticmethod
    def build(
        file_path: str,
        page_number: int = None
    ):

        metadata = {
            "source": file_path,
            "file_name": Path(file_path).name,
            "file_type": Path(file_path).suffix.lower()
        }

        if page_number is not None:
            metadata["page"] = page_number

        return metadata