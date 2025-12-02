import chromadb
from sentence_transformers import SentenceTransformer
from src.config import settings

class ChromaRetriever:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_PATH)
        self.collection = self.client.get_or_create_collection("reviews")
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")

    def search(self, query: str, k: int):
        q_emb = self.encoder.encode(query).tolist()
        return self.collection.query(
            query_embeddings=[q_emb],
            n_results=k,
            include=["documents", "metadatas", "distances"]
        )
