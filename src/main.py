from retrieval.embedding_model import create_embedding_model
from retrieval.vector_store import load_vector_store
from generation.response_generator import generate_response


def main():

    # 1. Cargar el modelo de embeddings
    print("\n========== MODELO DE EMBEDDINGS ==========")

    embedding_model = create_embedding_model()

    print("Modelo de embeddings cargado correctamente.")

    # 2. Cargar la base vectorial
    print("\n========== BASE VECTORIAL ==========")

    vector_store = load_vector_store(
        embedding_model=embedding_model
    )

    print("Base vectorial cargada correctamente.")

    # 3. Recibir la pregunta
    print("\n========== TELECOCONSULTA ==========")

    question = input("\nEscribe tu pregunta: ").strip()

    if not question:
        print("Debes ingresar una pregunta.")
        return

    # 4. Generar respuesta
    print("\n========== GENERANDO RESPUESTA ==========")

    response = generate_response(
        vector_store=vector_store,
        question=question
    )

    # 5. Mostrar respuesta
    print("\nRespuesta de TelecoConsulta:\n")
    print(response)


if __name__ == "__main__":
    main()
