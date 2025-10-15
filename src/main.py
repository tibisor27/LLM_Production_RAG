from config import config
from ingestion import load_pdf, chunks_and_metadata, create_embeddings, create_metadata, inject_data_to_db
import pandas as pd

def main():
    print(f"Reading PDF by pages...\n")
    pages_and_texts = load_pdf(config.PDF_PATH)

    print("Chunking (10 sentences per chunk, 2 overlap)...\n")
    chunks = chunks_and_metadata(pages_and_texts)
    print(chunks[0].keys())
    print(f"Length of chunks: {len(chunks)}")
    chunks_df = pd.DataFrame(chunks)
    print(chunks_df.describe(percentiles=[.05, .10, .25]))
    print(chunks[0]["sentence_chunk"])

    print(f'Type of chunks: {type(chunks[0]["sentence_chunk"])}')


    print("Creating embeddings...\n")
    embeddings_qwen = create_embeddings(chunks)
    print("EMBEDDINGS CREATED")
    print(embeddings_qwen)
    print(f"Type of embeddings: {type(embeddings_qwen)}")
    print(f"Shape of embeddings: {embeddings_qwen.shape}")
    print(f"First embedding: {embeddings_qwen[0]}")
    print(f"First embedding shape: {embeddings_qwen[0].shape}")
    print(f"First embedding type: {embeddings_qwen[0].dtype}")

    print(f"\nCreating metadata...\n")
    metadata,content_list = create_metadata(chunks)
    print(f"Metadata: {len(metadata)}")
    print(f"Content list: {len(content_list)}")

    print(f"\nInjecting data to Supabase...\n")
    inject_data_to_db(content_list, embeddings_qwen, metadata)



if __name__ == "__main__":
   main()