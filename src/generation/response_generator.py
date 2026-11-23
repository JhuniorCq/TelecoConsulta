import logging

from google.genai.errors import APIError
from langchain_chroma import Chroma

from config.settings import GEMINI_MODEL
from generation.gemini_client import create_gemini_client
from generation.prompt_template import create_prompt
from retrieval.retriever import retrieve_documents

logger = logging.getLogger(__name__)

def generate_response(
    vector_store: Chroma,
    question: str
) -> str:

    # 1. Recuperar los fragmentos relevantes
    documents = retrieve_documents(
        vector_store=vector_store,
        query=question
    )

    if not documents:
        return (
            "No encontré información suficiente en los documentos "
            "disponibles para responder tu pregunta."
        )

    # 2. Construir el contexto con los fragmentos recuperados
    context_parts = []

    for document in documents:

        source = document.metadata.get("source", "Documento desconocido")
        page = document.metadata.get("page", "Página desconocida")

        context_parts.append(
            f"Documento: {source}\n"
            f"Página: {page}\n"
            f"Contenido:\n{document.page_content}"
        )

    context = "\n\n".join(context_parts)

    # 3. Construir el prompt
    prompt = create_prompt(
        question=question,
        context=context
    )

    # 4. Generar la respuesta con Gemini
    client = create_gemini_client()

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        if not response.text:
            raise RuntimeError("Gemini no devolvió una respuesta.")

        return response.text.strip()

    except APIError:
        logger.exception("Error al comunicarse con Gemini.")
        return (
            "Lo siento, ocurrió un problema al generar la respuesta. "
            "Por favor, inténtalo nuevamente más tarde."
        )

    except Exception:
        logger.exception("Error inesperado al generar la respuesta.")
        return (
            "Lo siento, ocurrió un error inesperado al procesar tu consulta."
        )

    finally:
        client.close()
