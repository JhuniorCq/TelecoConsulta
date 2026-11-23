from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Configuración inicial del chunking
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def split_documents(documents: list[dict]) -> list[Document]:
    """
    Divide los documentos limpios en fragmentos (chunks).

    Conserva los metadatos de cada página y agrega
    la posición inicial del fragmento dentro del texto.
    """

    # Configurar el fragmentador
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
        add_start_index=True
    )

    # Convertir los documentos al formato Document de LangChain
    langchain_documents = [
        Document(
            page_content=document["content"],
            metadata=document["metadata"].copy()
        )
        for document in documents
    ]

    # Fragmentar los documentos
    chunks = text_splitter.split_documents(langchain_documents)

    return chunks
