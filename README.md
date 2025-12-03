# TFG_MovieRecommender

🎬 Movie-RAG: Natural Language Movie Recommendation System
This project implements a Retrieval-Augmented Generation (RAG) architecture for movie recommendation using natural language queries.
It combines semantic retrieval over movie reviews with generative AI to provide personalized, explainable recommendations.

🚀 Key Components
Embedding Model: all-MiniLM-L6-v2 (SentenceTransformers)
Vector Database: ChromaDB
Backend API: FastAPI
Data Source: Rotten Tomatoes Movies & Reviews (Kaggle)



.venv\Scripts\activate


python -m uvicorn src.app:app --reload --port 8001