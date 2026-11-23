import re
import unicodedata


# Patrones de encabezados y elementos de paginación que se pueden eliminar.
NOISE_PATTERNS = [
    re.compile(
        r"^Sistema Peruano de Información Jurídica(?:\s+Ministerio de Justicia)?$",
        re.IGNORECASE
    ),
    re.compile(
        r"^Ministerio de Justicia$",
        re.IGNORECASE
    ),
    re.compile(
        r"^\d{2}/\d{2}/\d{4}\s+\d{1,2}:\d{2}:\d{2}\s+"
        r"(?:a\.?\s*m\.?|p\.?\s*m\.?)\s+Página\s+\d+$",
        re.IGNORECASE
    ),
    re.compile(r"^\d+\s*\|\s*\d+$")
]


def clean_text(text: str) -> str:
    """
    Normaliza el texto extraído de una página PDF.

    Conserva el contenido legal y los saltos de párrafo,
    eliminando espacios, caracteres y elementos de paginación.
    """

    # Normalizar caracteres Unicode
    text = unicodedata.normalize("NFC", text)

    # Reemplazar espacios especiales
    text = text.replace("\u00a0", " ")

    # Eliminar guiones invisibles
    text = text.replace("\u00ad", "")

    # Normalizar saltos de línea
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Eliminar espacios repetidos dentro de las líneas
    text = re.sub(r"[ \t]+", " ", text)

    # Limpiar líneas y eliminar encabezados o numeración de página
    cleaned_lines = []

    for line in text.split("\n"):
        line = line.strip()

        if not line:
            cleaned_lines.append(line)
            continue

        if any(pattern.fullmatch(line) for pattern in NOISE_PATTERNS):
            continue

        cleaned_lines.append(line)

    text = "\n".join(cleaned_lines)

    # Reducir saltos de línea excesivos
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()



def clean_documents(documents: list[dict]) -> list[dict]:
    """
    Limpia el contenido de los documentos y elimina números
    de página aislados cuando coinciden con sus metadatos.
    """

    cleaned_documents = []

    for document in documents:

        cleaned_content = clean_text(document["content"])

        page_number = str(document["metadata"]["page"])

        # Eliminar el número de página si aparece como primera línea.
        lines = cleaned_content.split("\n")

        if lines and lines[0].strip() == page_number:
            lines.pop(0)

        cleaned_content = "\n".join(lines).strip()

        if not cleaned_content:
            continue

        cleaned_documents.append({
            "content": cleaned_content,
            "metadata": document["metadata"].copy()
        })

    return cleaned_documents
