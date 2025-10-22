from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import your RAG functions from the src package's unified API
from src import (
    retrieve_relevant_sources,
    augment_answer_with_context,
    rewrite_query,
    config
)

# Initialize the FastAPI app
app = FastAPI(
    title="RAG API",
    description="An API for the Retrieval-Augmented Generation application.",
    version="1.0.0",
)

# Configure CORS (Cross-Origin Resource Sharing)
# This allows your TypeScript frontend to communicate with this backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define the request body model for the /chat endpoint
class ChatQuery(BaseModel):
    query: str

@app.post("/api/chat")
def chat_endpoint(chat_query: ChatQuery):
    """
    Receives a user query, performs the RAG process, and returns the generated answer.
    """
    print(f"Received query: {chat_query.query}")
    
    # Step 1: Rewrite the query
    rewritten_query = rewrite_query(chat_query.query)
    
    # Step 2: Retrieve context using the rewritten query
    context_chunks = retrieve_relevant_sources(rewritten_query)
    
    # Step 3: Generate answer if context is found
    if context_chunks:
        response_data = augment_answer_with_context(rewritten_query, context_chunks)
        
        answer = response_data.get("answer", "No answer could be generated.")
        input_tokens = response_data.get("input_tokens", 0)
        output_tokens = response_data.get("output_tokens", 0)
        
        return {
            "answer": answer,
            "token_usage": {
                "input": input_tokens,
                "output": output_tokens
            },
            "retrieved_context": context_chunks # Optionally return the context for debugging
        }
    else:
        return {
            "answer": "I could not find relevant information to answer your question.",
            "token_usage": None,
            "retrieved_context": []
        }

if __name__ == "__main__":
    # This allows you to run the API server directly by running `python main.py`
    print("Starting RAG API server at http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
