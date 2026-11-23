
from ingestion.document_loader import load_documents
from ingestion.text_cleaner import clean_documents
from ingestion.text_splitter import split_documents

from retrieval.embedding_model import create_embedding_model
from retrieval.vector_store import create_vector_store


def main():

    # 1. Cargar documentos PDF
    print("\n========== CARGA DE DOCUMENTOS ==========")

    documents = load_documents()

    print(f"Documentos cargados: {len(documents)}")

    # 2. Limpiar documentos
    print("\n========== LIMPIEZA DE DOCUMENTOS ==========")

    cleaned_documents = clean_documents(documents)

    print(f"Documentos limpios: {len(cleaned_documents)}")

    # 3. Dividir documentos en chunks
    print("\n========== DIVISIÓN EN CHUNKS ==========")

    chunks = split_documents(cleaned_documents)

    print(f"Chunks generados: {len(chunks)}")

    # 4. Crear modelo de embeddings
    print("\n========== MODELO DE EMBEDDINGS ==========")

    embedding_model = create_embedding_model()

    print("Modelo de embeddings cargado correctamente.")

    # 5. Crear base vectorial
    print("\n========== CONSTRUCCIÓN DE CHROMADB ==========")

    vector_store = create_vector_store(
        chunks=chunks,
        embedding_model=embedding_model
    )

    print("\nBase vectorial construida correctamente.")


if __name__ == "__main__":
    main()
