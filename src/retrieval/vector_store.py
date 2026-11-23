
import shutil
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings


# Directorio raíz del proyecto
BASE_DIR = Path(__file__).resolve().parents[2]

# Directorio donde se almacenará ChromaDB
CHROMA_DB_DIR = BASE_DIR / "chroma_db"

# Nombre de la colección
COLLECTION_NAME = "teleco_consulta"


def create_vector_store(
    chunks: list[Document],
    embedding_model: HuggingFaceEmbeddings
) -> Chroma:
    """
    Genera los embeddings de los chunks y los almacena en ChromaDB.

    Args:
        chunks: Fragmentos de los documentos.
        embedding_model: Modelo utilizado para generar embeddings.

    Returns:
        Chroma: Instancia de la base de datos vectorial.
    """

    if not chunks:
        raise ValueError("No hay chunks para almacenar.")

    # Eliminar la base anterior para evitar duplicar información
    if CHROMA_DB_DIR.exists():
        shutil.rmtree(CHROMA_DB_DIR)

    print("\nGenerando embeddings y almacenando en ChromaDB...")

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        collection_name=COLLECTION_NAME,
        persist_directory=str(CHROMA_DB_DIR)
    )

    print("Base vectorial creada correctamente.")

    return vector_store


def load_vector_store(
    embedding_model: HuggingFaceEmbeddings
) -> Chroma:
    """
    Carga una base vectorial ChromaDB existente.

    Args:
        embedding_model: Modelo utilizado para las consultas.

    Returns:
        Chroma: Instancia de la base de datos vectorial.
    """

    if not CHROMA_DB_DIR.exists():
        raise FileNotFoundError(
            f"No se encontró la base vectorial en: {CHROMA_DB_DIR}"
        )

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_model,
        persist_directory=str(CHROMA_DB_DIR)
    )

    return vector_store
