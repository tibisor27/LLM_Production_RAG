import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PDF_PATH = os.getenv("PDF_PATH")
    EMBEDDING_MODEL = os.getenv("EMBED_MODEL")
    RAG_MODEL = os.getenv("RAG_MODEL")
    RAG_MODEL_ID = os.getenv("RAG_MODEL_ID")
    SENTS_PER_CHUNK = int(os.getenv("SENTS_PER_CHUNK"))
    SENT_OVERLAP = int(os.getenv("SENT_OVERLAP"))   
    MAX_TOKENS = int(os.getenv("MAX_TOKENS"))
    MIN_TOKENS = int(os.getenv("MIN_TOKENS"))

config = Config()