from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader


def le_arquivo(KEY):
    parser = LlamaParse(
        api_key=KEY,
        # can also be set in your env as LLAMA_CLOUD_API_KEY
        result_type="markdown",  # "markdown" and "text" are available
        num_workers=4,  # if multiple files passed, split in `num_workers` API calls
        verbose=True,
        language='pt'
    )

    file_extractor = {".pdf": parser}
    documents = SimpleDirectoryReader(
        "./arquivos", file_extractor=file_extractor
    ).load_data()


    # documents = parser.load_data(arquivo)
    # print(document[0].text[:300])
    # with open("./arquivos/ppc-liccomp-parsed.md", "w", encoding="utf-8") as arquivo:
    #     # Escrevendo o conteúdo da variável documento no arquivo
    #     arquivo.write(document[0].text)
    return documents
