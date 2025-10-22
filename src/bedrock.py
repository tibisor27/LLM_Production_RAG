import boto3
from .config import config

_bedrock_client = None

def get_bedrock_client() -> boto3.client:
    global _bedrock_client
    if _bedrock_client is None:
        _bedrock_client = boto3.client(
            service_name="bedrock-runtime",
            region_name=config.AWS_REGION,
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
        )
    return _bedrock_client

def invoke_bedrock_model(prompt: str, max_tokens: int = 512, temperature: float = 0.5) -> dict:
    """
    A wrapper function to invoke a Bedrock model using the Converse API.
    Handles client retrieval, request formatting, and response parsing.
    Returns a dictionary with the answer and token usage.
    """
    try:
        bedrock_client = get_bedrock_client()

        messages = [{"role": "user", "content": [{"text": prompt}]}]
        inference_config = {"maxTokens": max_tokens, "temperature": temperature}

        response = bedrock_client.converse(
            modelId=config.BEDROCK_MODEL_ID,
            messages=messages,
            inferenceConfig=inference_config,
        )

        answer = response["output"]["message"]["content"][0]["text"]
        
        # Extract token usage from the response metadata
        print(f"RAW RESPONSE: {response}")
        usage = response.get("usage", {})
        input_tokens = usage.get("inputTokens", 0)
        output_tokens = usage.get("outputTokens", 0)

        return {
            "answer": answer.strip(),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens
        }
    
    except Exception as e:
        print(f"ERROR during Bedrock Converse API call: {e}")
        return {
            "answer": "",
            "input_tokens": 0,
            "output_tokens": 0
        } # Return a default dictionary on error