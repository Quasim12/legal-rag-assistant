import os

from dotenv import load_dotenv

from app.llms.groq import GroqLLM
from app.llms.openai import OpenAILLM


load_dotenv()


class LLMFactory:

    _llm = None

    @classmethod
    def get_llm(cls):

        if cls._llm is not None:
            return cls._llm

        provider = os.getenv(
            "LLM_PROVIDER",
            "groq"
        ).strip().lower()

        providers = {
            "groq": GroqLLM.get_model,
            "openai": OpenAILLM.get_model
        }

        if provider not in providers:

            raise ValueError(
                f"Unsupported LLM Provider: {provider}"
            )

        cls._llm = providers[provider]()

        return cls._llm

    @classmethod
    def clear_cache(cls):

        cls._llm = None