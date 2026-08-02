import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


class GroqLLM:

    _model = None

    @classmethod
    def get_model(cls):

        if cls._model is None:

            cls._model = ChatGroq(
                api_key=os.getenv("GROQ_API_KEY"),
                model="llama-3.1-8b-instant",
                temperature=0
            )

        return cls._model