from src.clients.chroma_client import ChromaRetriever

retriever = ChromaRetriever()

def retrieve(query: str, top_k: int):
    return retriever.search(query, top_k)
