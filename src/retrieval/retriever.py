
from langchain_chroma import Chroma
from langchain_core.documents import Document


# Cantidad de fragmentos que se recuperarán
TOP_K = 3


def retrieve_documents(
    vector_store: Chroma,
    query: str,
    k: int = TOP_K
) -> list[Document]:
    """
    Recupera los fragmentos más relevantes para una consulta.

    Args:
        vector_store: Base de datos vectorial ChromaDB.
        query: Pregunta realizada por el usuario.
        k: Cantidad máxima de fragmentos a recuperar.

    Returns:
        list[Document]: Fragmentos recuperados.
    """

    if not query.strip():
        raise ValueError("La consulta no puede estar vacía.")

    retriever_results = vector_store.similarity_search(
        query=query,
        k=k
    )

    return retriever_results
