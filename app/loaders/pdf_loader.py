# app/loaders/pdf_loader.py

from langchain_community.document_loaders import PDFPlumberLoader


class PDFLoader:

    @staticmethod
    def load(file_path: str):

        loader = PDFPlumberLoader(file_path)

        return loader.load()