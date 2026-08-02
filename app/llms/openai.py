import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


class OpenAILLM:

    _model = None

    @classmethod
    def get_model(cls):

        if cls._model is None:

            cls._model = ChatOpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                model="gpt-4.1-mini",
                temperature=0
            )

        return cls._model