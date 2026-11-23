from google import genai

from config.settings import GEMINI_API_KEY


def create_gemini_client() -> genai.Client:
    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    return client
