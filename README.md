# Liccomp Chatbot [(clique aqui)](https://liccompchatbot.streamlit.app/)

Liccomp Chatbot é um aplicativo de chatbot desenvolvido com [Streamlit](https://streamlit.io/) e [Llama Index](https://github.com/jerryjliu/llama_index), que utiliza os modelos Gemini da Google para responder perguntas relacionadas ao curso de Licenciatura em Computação da Universidade Federal do Paraná (UFPR), localizado no Setor Palotina. O chatbot, chamado Jonas, foi criado para fornecer respostas em português de forma interativa.

## Funcionalidades

- **Chat Interativo:** Permite que os usuários façam perguntas e recebam respostas em tempo real.
- **Indexação de Documentos:** Carrega e indexa um arquivo PDF contendo o conteúdo do curso, otimizando a busca por informações.
- **Persistência do Índice:** Salva o índice gerado em disco para evitar o recálculo a cada execução.
- **Modelos Gemini:** Utiliza o modelo de linguagem e embeddings do Google Gemini, garantindo respostas precisas sem depender do OpenAI.

## Requisitos

- Python 3.8 ou superior
- [Streamlit](https://streamlit.io/)
- [Llama Index](https://github.com/jerryjliu/llama_index) (verifique a compatibilidade da versão)
- Acesso à API do Google Gemini (obtenha sua chave em [Google Cloud](https://cloud.google.com/))

## Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/liccomp-chatbot.git
   cd liccomp-chatbot

2. **Crie e ative um ambiente virtual (opcional, mas recomendado):**

    ```bash
    python -m venv venv
    # No Linux/Mac:
    source venv/bin/activate
    # No Windows:
    venv\Scripts\activate

3. **Instale as dependências:**

Certifique-se de que o arquivo `requirements.txt` contenha todas as bibliotecas necessárias, por exemplo:

    ```bash
    streamlit
    llama-index
    parser_helper  # ou a biblioteca equivalente para manipulação de PDFs

4. **Configuração da chave da API:**

* Chave API do Google Gemini está salva como secret no streamlit. 

## Uso

Para executar o aplicativo, utilize o comando:

    ```bash
    streamlit run main.py

## Estrutura do Projeto
* nome_do_arquivo.py: Código principal do aplicativo, que inicializa o Streamlit, carrega ou cria o índice e gerencia o chat.
* parser_helper.py: Módulo auxiliar para leitura e processamento do arquivo PDF.
* ./arquivos/: Arquivos PDF contendo o conteúdo do curso.
* ./index_storage: Diretório onde o índice persistido é salvo para evitar recalcular a indexação a cada execução.














