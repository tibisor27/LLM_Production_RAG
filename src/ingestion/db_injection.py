from ..config import config
from supabase import create_client, Client
from tqdm.auto import tqdm 

def create_metadata(chunk_list: list[dict]) -> tuple[list, list]:
    metas = []
    content_list = []

    for page in chunk_list:
        metas.append({
            "page_number" : page["page_number"],
            "chunk_sentence_count" : page["chunk_sentence_count"],
            "source" : config.PDF_PATH
        })
        content_list.append(page["sentence_chunk"])
    return metas, content_list

def inject_data_to_db(content_list: list, embeddings_list: list, metadata_list: list):
    sb: Client = create_client(config.SUPABASE_URL, config.SUPABASE_SERVICE_ROLE_KEY)

    #Optional: keep the table clean for this document
    sb.table("chunks").delete().eq("doc_id", config.DOC_ID).execute()
    rows = []
    for idx, (content, embedding, metadata) in enumerate(zip(content_list, embeddings_list, metadata_list)):
        rows.append({
            "doc_id" : config.DOC_ID,
            "chunk_index" : idx,
            "content" : content,
            "metadata" : metadata,
            "embedding" : embedding.tolist()
        })

    print(f"Uploading to Supabase...")
    for j in tqdm(range(0, len(rows), config.BATCH_INSERT), desc="Uploading"):
        sb.table("chunks").insert(rows[j:j+config.BATCH_INSERT]).execute()

    print(f"Done! Inserted {len(rows)} chunks for doc_id={config.DOC_ID}")
