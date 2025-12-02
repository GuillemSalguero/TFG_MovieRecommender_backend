from collections import defaultdict
from typing import Dict

def augment_results(chroma_res: Dict, meta_lookup, max_results=5, max_runtime=None):
    docs = chroma_res["documents"][0]
    metas = chroma_res["metadatas"][0]
    dists = chroma_res["distances"][0]

    items = []
    for doc, meta, dist in zip(docs, metas, dists):
        sim = 1 - dist
        items.append({
            "link": meta.get("link", ""),
            "sim": float(sim),
            "snippet": doc[:300]
        })

    grouped = defaultdict(list)
    for it in items:
        grouped[it["link"]].append(it)

    enriched = []
    for link, lst in grouped.items():
        sim_avg = sum(x["sim"] for x in lst)/len(lst)
        m = meta_lookup(link)
        penalty = 0.0
        if max_runtime and m.get("runtime") and m["runtime"] > max_runtime:
            penalty += 0.2

        tom = (m.get("tomatometer_rating") or 0)/100.0
        score = 0.7*sim_avg + 0.3*tom - 0.1*penalty

        enriched.append({
            "link": link,
            "score": score,
            "sim_avg": sim_avg,
            "title": m.get("movie_title"),
            "year": (m.get("original_release_date") or "")[:4],
            "genres": m.get("genres"),
            "directors": m.get("directors"),
            "runtime": m.get("runtime"),
            "tomatometer": m.get("tomatometer_rating"),
            "tomatometer_count": m.get("tomatometer_count"),
            "snippets": [x["snippet"] for x in sorted(lst, key=lambda z:z["sim"], reverse=True)[:2]]
        })

    enriched.sort(key=lambda x: x["score"], reverse=True)
    return enriched[:max_results]
