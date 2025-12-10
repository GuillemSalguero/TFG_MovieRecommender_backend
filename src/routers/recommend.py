from fastapi import APIRouter, HTTPException
from src.models.schemas import RecommendRequest, RecommendResponse, RAResult
from src.utils.text import normalize_query
from src.service.retrieval import retrieve
from src.service.augment import augment_results
from src.clients.supabase_client import MovieMeta
from src.config import settings

router = APIRouter(prefix="/recommend", tags=["recommend"])

meta_client = MovieMeta()

def meta_lookup(link: str):
    return meta_client.get_movie_meta(link)

@router.post("", response_model=RecommendResponse)
def recommend(payload: RecommendRequest):
    if not payload.query:
        raise HTTPException(400, "query is required")

    q = normalize_query(payload.query)
    raw = retrieve(q, min(payload.max_results*5, 25))

    augmented = augment_results(
        chroma_res=raw,
        meta_lookup=meta_lookup,
        max_results=payload.max_results,
        max_runtime=payload.max_runtime
    )

    api_results = [
        RAResult(
            title=i["title"],
            year=i["year"],
            genres=i["genres"],
            directors=i["directors"],
            runtime=i["runtime"],
            score=round(i["score"], 4),
            signals={
                "sim_avg": round(i["sim_avg"], 4),
                "tomatometer": i["tomatometer"],
                "count": i["tomatometer_count"]
            },
            snippets=i["snippets"],
            link=i["link"],
            poster=i.get("poster"),
        )
        for i in augmented
    ]

    return RecommendResponse(query=q, results=api_results)
