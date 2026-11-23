
from langchain_huggingface import HuggingFaceEmbeddings


# Modelo multilingüe para generar embeddings
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def create_embedding_model() -> HuggingFaceEmbeddings:
    """
    Crea y configura el modelo de embeddings de Hugging Face.

    Returns:
        HuggingFaceEmbeddings: Modelo preparado para generar embeddings.
    """

    embedding_model = HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs={
            "device": "cpu"
        },
        encode_kwargs={
            "normalize_embeddings": True
        }
    )

    return embedding_model
