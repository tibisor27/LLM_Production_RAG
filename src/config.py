import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PDF_PATH = os.getenv("PDF_PATH")
    SENTS_PER_CHUNK = int(os.getenv("SENTS_PER_CHUNK"))
    SENT_OVERLAP = int(os.getenv("SENT_OVERLAP"))
    
    # User's preferred embedding model
    EMBED_MODEL = os.getenv("EMBED_MODEL")

    # AWS and Bedrock Settings
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION")
    # Switch the model to Mistral 7B Instruct
    BEDROCK_MODEL_ID = "mistral.mistral-7b-instruct-v0:2"
    MAX_TOKENS = int(os.getenv("MAX_TOKENS"))

    BATCH_SIZE = int(os.getenv("BATCH_SIZE"))
    DOC_ID = os.getenv("DOC_ID")
    BATCH_INSERT = int(os.getenv("BATCH_INSERT"))
    TOP_K = int(os.getenv("TOP_K"))
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

config = Config()