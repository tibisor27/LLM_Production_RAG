import torch
from ..config import config
from sentence_transformers import SentenceTransformer
from time import perf_counter as timer

def _load_model():
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"Using device: {device}")

    #load the model
    print(f"[EMBEDDING] Loading model {config.EMBED_MODEL}...")
    start_time = timer()
    model = SentenceTransformer(
        model_name_or_path=config.EMBED_MODEL,
        device=device
    )
    end_time = timer()
    print(f"[EMBEDDING] Time to load model: {end_time - start_time} seconds")
    print(f"[EMBEDDING] Model loaded successfully")

    return model


def create_embeddings(list_chunks:list[dict]):
    embedding_model = _load_model()
    chunks = [item["sentence_chunk"] for item in list_chunks]
    embeddings_qwen = embedding_model.encode(chunks,
    batch_size = config.BATCH_SIZE,
    show_progress_bar = True
    )
    return embeddings_qwen

def embed_query(query:str):
    embedding_model = _load_model()
    return embedding_model.encode(query)