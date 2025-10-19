from ingestion import embed_query
from config import config
from supabase import create_client, Client
import textwrap

def retrieve_relevant_sources(query:str)->list[dict]:
    sb: Client = create_client(config.SUPABASE_URL, config.SUPABASE_SERVICE_ROLE_KEY)
    query_embedding = embed_query(query)
    resp = sb.rpc("match_documents", {
        "query_embedding": query_embedding.tolist(),
        "match_count": config.TOP_K,
        "filter": {"source": config.PDF_PATH}}).execute()

    rows = resp.data or []
    print(rows)
    print(f"\nLength of rows: {len(rows)}")
    print(f"Type of rows: {type(rows[0])}")
    print("\n" + "="*90)
    print(f"QUERY: {query}")
    if not rows:
        print("  (no matches)")
        return []
        
    for rank, r in enumerate(rows, start=1):
        page = (r.get("metadata") or {}).get("page_number", "?")
        sim  = r.get("similarity", None)
        sim_str = f"{sim:.3f}" if isinstance(sim, (int, float)) else "?"
        preview = textwrap.shorten(r.get("content","").replace("\n"," "), width=160)
        print(f"  [{rank}] page {page}  sim={sim_str}  chunk_index={r.get('chunk_index')}")
        print(f"      {preview}")
    
    return rows
