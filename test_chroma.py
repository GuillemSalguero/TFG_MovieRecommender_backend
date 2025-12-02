from sentence_transformers import SentenceTransformer
import chromadb

from src.config import settings 


CHROMA_PATH = settings.CHROMA_PATH

print("🔎 Connecting to Chroma at:", CHROMA_PATH)
client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection("reviews")
print("📊 Number of vectors in 'reviews':", collection.count())

model = SentenceTransformer("all-MiniLM-L6-v2")

query = "a sci-fi movie about artificial intelligence"
emb = model.encode(query).tolist()

res = collection.query(
    query_embeddings=[emb],
    n_results=5,
    include=["documents", "metadatas", "distances"]
)

print("\nRaw Chroma result:")
print(res)
