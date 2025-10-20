import boto3
import json
from config import config
from bedrock import invoke_bedrock_model 

def build_rag_prompt(query: str, context: list[dict]) -> str:
    context_str = "\n\n---\n\n".join([item["content"] for item in context])

    # Mistral models expect a specific instruction format with [INST] tags.
    prompt = f"""<s>[INST] Use the following context to answer the user's question.
If the answer is not found in the context, say "I could not find the answer in the provided documents."

Context:
{context_str}

User's Question:
{query} [/INST]"""
    return prompt

def rewrite_query(query:str) -> str:
    rewrite_template = f""" 
    You are a query rewriting expert.

    All user queries are related to human nutrition and health.
    Your task is to rewrite the user query to be more specific and detailed.

    Analyze the user's query and rewrite it to improve RAG document retrieval chances:
        - Make it more specific or more general as appropriate
        - Add synonyms or related terms
        - Rephrase to target likely document content
        - Do not include in the rewritten query the fact that the campaign is called Curse of Strahd or is related to the campaign, just use this information as context to improve the query

    User query: {query}

    Rewritten user query:
    """
    
    print("\n--- Rewriting query via Bedrock ---")
    response_data = invoke_bedrock_model(prompt=rewrite_template, temperature=0.5)
    
    rewritten_query = response_data["answer"]
    
    print(f"Original query: {query}")
    print(f"Rewritten query: {rewritten_query}")
    print(f"(Token Usage: Input={response_data['input_tokens']}, Output={response_data['output_tokens']})")
    
    return rewritten_query




def augment_answer_with_context(query: str, context: list[dict]) -> str:
    # Build the complete RAG prompt
    rewritten_query = rewrite_query(query)
 
    prompt = build_rag_prompt(rewritten_query, context)

    print("\n--- Generating Answer via Amazon Bedrock (Converse API) ---")
    
    # Use the wrapper function for a clean API call
    response_data = invoke_bedrock_model(prompt=prompt, temperature=0.1)
    
    answer = response_data["answer"]
    
    print(f"\nFinal Answer (Token Usage: Input={response_data['input_tokens']}, Output={response_data['output_tokens']}):")
    print(answer)
    return answer