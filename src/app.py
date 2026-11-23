import streamlit as st

from retrieval.embedding_model import create_embedding_model
from retrieval.vector_store import load_vector_store
from generation.response_generator import generate_response


# Configuración de la página
st.set_page_config(
    page_title="TelecoConsulta",
    page_icon="📡",
    layout="centered"
)


# Estilos CSS

st.markdown("""
<style>

    /* Espaciado del contenido */
    .block-container {
        max-width: 850px;
        padding-top: 3.5rem;
        padding-bottom: 3rem;
    }

    /* Título */
    .main-title {
        color: #1E40AF;
        font-size: 2.3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    /* Descripción */
    .main-description {
        color: #475569;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    /* Mensaje de bienvenida */
    .welcome-box {
        background-color: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-radius: 12px;
        padding: 18px;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .welcome-title {
        color: #1E40AF;
        font-size: 1.1rem;
        font-weight: 600;
    }

    .welcome-text {
        color: #334155;
        font-size: 0.95rem;
    }

    /* Botón principal */
    .stButton button {
        background-color: #2563EB;
        color: #FFFFFF;
        border-radius: 8px;
        border: none;
    }

    .stButton button:hover {
        background-color: #1D4ED8;
        color: #FFFFFF;
    }

    /* Entrada del chat */
    .stChatInput textarea {
        border-radius: 10px;
    }

    /* MODO OSCURO */
    @media (prefers-color-scheme: dark) {

        .main-title {
            color: #93C5FD;
        }

        .main-description {
            color: #CBD5E1;
        }

        .welcome-box {
            background-color: #1E293B;
            border-color: #334155;
        }

        .welcome-title {
            color: #93C5FD;
        }

        .welcome-text {
            color: #E2E8F0;
        }
    }

</style>
""", unsafe_allow_html=True)

# Encabezado
st.markdown(
    '<div class="main-title">📡 TelecoConsulta</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-description">'
    'Asistente virtual sobre los derechos de los usuarios de '
    'los servicios públicos de telecomunicaciones en Perú.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# Carga de componentes RAG
@st.cache_resource
def load_rag_components():

    embedding_model = create_embedding_model()

    vector_store = load_vector_store(
        embedding_model=embedding_model
    )

    return vector_store


try:
    vector_store = load_rag_components()

except Exception:
    st.error(
        "No se pudo iniciar TelecoConsulta. "
        "Por favor, inténtalo nuevamente más tarde."
    )
    st.stop()


# Historial de conversación
if "messages" not in st.session_state:
    st.session_state.messages = []


# Botón para nueva conversación
if st.button("＋ Nueva conversación"):

    st.session_state.messages = []
    st.rerun()


# Mensaje de bienvenida
if not st.session_state.messages:

    st.markdown("""
    <div class="welcome-box">
        <div class="welcome-title">
            ¡Bienvenido a TelecoConsulta!
        </div>
        <div class="welcome-text">
            Puedes realizar consultas sobre tus derechos como usuario
            de los servicios de telecomunicaciones.
            Mis respuestas se basan en documentos oficiales de OSIPTEL.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Algunas preguntas que puedes realizar:**")

    example_questions = [
        "¿Qué es la portabilidad numérica?",
        "¿Cómo puedo presentar un reclamo?",
        "¿Qué obligaciones tienen las operadoras respecto al servicio de Internet?"
    ]

    for example in example_questions:
        st.markdown(f"- {example}")


# Mostrar historial
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Entrada de preguntas
question = st.chat_input("Escribe tu pregunta aquí...")


if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Consultando los documentos de OSIPTEL..."):

            response = generate_response(
                vector_store=vector_store,
                question=question
            )

        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
