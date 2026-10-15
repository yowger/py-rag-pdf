
from langchain_openai import OpenAIEmbeddings


def create_embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        model="text-embedding-3-small",
    )
