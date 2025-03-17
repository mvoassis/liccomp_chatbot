import streamlit as st
import parser_helper
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings, load_index_from_storage, VectorStoreIndex, StorageContext
import os

# Caminho onde o índice será salvo
INDEX_STORAGE_PATH = "./index_storage"

# Configuração da página do Streamlit
st.set_page_config(page_title="Liccomp Chatbot", page_icon="🦙", layout="centered",
                   initial_sidebar_state="auto", menu_items=None)

# Título do chatbot
st.title("Liccomp Chatbot 💬🦙")

# Inicializa o histórico de mensagens do chat
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá, tudo bem? Ficarei feliz em ajudar! :)"}
    ]

# Chave da API do Google para uso dos modelos da Gemini
GOOGLE_API_KEY = st.secrets["GOOGLE_API"]

# Chave API do Llama parse para converter documentos .pdf em markdown
LLAMAPARSE_API_KEY = st.secrets["LLAMAPARSE_API"]


@st.cache_resource(show_spinner=False)
def load_data():
    """
    Carrega o índice salvo do armazenamento ou cria um novo se ele não existir.
    """

    # Configuração do parser para dividir o texto em sentenças menores
    node_parser = SentenceSplitter(chunk_size=1024, chunk_overlap=20)

    # Configuração do modelo de embeddings e LLM da Gemini
    Settings.embed_model = GeminiEmbedding(
        model_name="models/gemini-embedding-exp-03-07", api_key=GOOGLE_API_KEY
    )
    llm = Gemini(api_key=GOOGLE_API_KEY, model_name="models/gemini-1.5-flash", temperature=0.2)

    # Configuração dos modelos globais no Settings
    Settings.llm = llm
    Settings.node_parser = node_parser

    if os.path.exists(INDEX_STORAGE_PATH):
        with st.spinner("Carregando índice salvo..."):
            storage_context = StorageContext.from_defaults(persist_dir=INDEX_STORAGE_PATH)
            return load_index_from_storage(storage_context)

    with st.spinner(text="Carregando e indexando os documentos. Isso pode levar 1-2 minutos..."):
        # Leitura do arquivo PDF com o parser helper
        docs = parser_helper.le_arquivo(LLAMAPARSE_API_KEY)

        # Criação do índice vetorial a partir dos documentos
        index = VectorStoreIndex.from_documents(docs, transformation=[node_parser, llm])

        # Salva o índice para futuras execuções
        index.storage_context.persist(persist_dir=INDEX_STORAGE_PATH)

        return index


# Carrega o índice dos documentos
index = load_data()

# Inicializa o mecanismo de chat e de consulta se ainda não estiver configurado
if "chat_engine" not in st.session_state.keys():
    st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)
    #st.session_state.query_engine = index.as_query_engine(similarity_top_k=5, response_mode="refine", verbose=True)

# Captura a entrada do usuário no chat
if prompt := st.chat_input("Digite sua pergunta"):
    st.session_state.messages.append({"role": "user", "content": prompt})

# Exibe as mensagens anteriores do chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Se a última mensagem não for do assistente, gera uma nova resposta
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            print(index)  # Exibe o índice no console para debug

            # Contextualização da pergunta para o assistente
            preparacao = ('Considerando que você é um assistente prestativo, que tem como objetivo responder '
                          'perguntas relacionadas ao curso de Licenciatura em Computação da Universidade Federal do Paraná '
                          '(UFPR), localizado no Setor Palotina, e que seu nome é Jonas, responda às perguntas em português (pt-br).\n\n'
                          '# Pergunta:\n\n')

            response = st.session_state.chat_engine.chat(preparacao + prompt)
            st.write(response.response)  # Exibe a resposta no chat

            # Adiciona a resposta ao histórico do chat
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)
