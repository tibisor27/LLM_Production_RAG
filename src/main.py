from config import config
from ingestion import load_pdf, chunks_and_metadata
import pandas as pd

if __name__ == "__main__":
    print(f"Reading PDF by pages...\n")
    pages_and_texts = load_pdf(config.PDF_PATH)

    print("Chunking (10 sentences per chunk, 2 overlap)...\n")
    chunks = chunks_and_metadata(pages_and_texts)
    print(chunks[0].keys())
    chunks_df = pd.DataFrame(chunks)
    print(chunks_df.describe(percentiles=[.05, .10, .25]))
