from pathlib import Path
import pymupdf


# Directorio raíz del proyecto
BASE_DIR = Path(__file__).resolve().parents[2]

# Directorio que contiene los documentos PDF
DOCUMENTS_DIR = BASE_DIR / "documents"


def load_documents():
    """
    Carga todos los archivos PDF de la carpeta documents
    y extrae su contenido página por página.

    Returns:
        list[dict]: Lista de páginas con su contenido y metadatos.
    """

    documents = []

    # Buscar todos los archivos PDF
    pdf_files = sorted(DOCUMENTS_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            f"No se encontraron archivos PDF en: {DOCUMENTS_DIR}"
        )

    print(f"\nDocumentos encontrados: {len(pdf_files)}")

    # Procesar cada archivo PDF
    for pdf_path in pdf_files:

        print(f"Procesando: {pdf_path.name}")

        with pymupdf.open(pdf_path) as pdf_document:

            for page_number, page in enumerate(pdf_document, start=1):

                # Extraer texto de la página
                text = page.get_text("text").strip()

                # Ignorar páginas sin contenido textual
                if not text:
                    continue

                # Guardar contenido y metadatos
                documents.append({
                    "content": text,
                    "metadata": {
                        "source": pdf_path.name,
                        "page": page_number
                    }
                })

    print("\nExtracción finalizada.")

    return documents
