from config import config
from llama_cpp import Llama
from time import perf_counter as timer
from huggingface_hub import hf_hub_download
from transformers import AutoTokenizer

def _load_gen_model() -> tuple:
    # Download the GGUF model file from Hugging Face
    model_path = hf_hub_download(
        repo_id=config.GEN_MODEL_REPO_ID,
        filename=config.GEN_MODEL_FILE,
    )
    
    # The tokenizer is still best loaded from the original, non-quantized model repository
    tokenizer = AutoTokenizer.from_pretrained(config.TOKENIZER_ID)

    print(f"[GENERATION] Loading model {config.GEN_MODEL_FILE}...")
    start_time = timer()

    # Instantiate the model from the local GGUF file
    llm = Llama(
        model_path=model_path,
        n_gpu_layers=-1,  # Offload all layers to GPU (Metal)
        use_mmap=True,    # Use memory mapping for faster loading
        n_ctx=2048,       # Context window size
        verbose=False,    # Suppress verbose output
    )
    
    end_time = timer()
    print(f"[GENERATION] Time to load model: {end_time - start_time:.2f} seconds")

    return llm, tokenizer


def build_prompt(query:str, context:list[dict], tokenizer:AutoTokenizer) -> str:
    context_str = "\n\n---\n\n".join([item["content"] for item in context])

    base_prompt = f"""Use the following context to answer the user's question.
If the answer is not found in the context, say "I could not find the answer in the provided documents."

Context:
{context_str}

User's Question:
{query}
"""

    dialogue_template = [
        {"role": "user", "content": base_prompt}
    ]

    prompt = tokenizer.apply_chat_template(
        conversation=dialogue_template,
        tokenize=False,
        add_generation_prompt=True
    )
    
    return prompt


def augment_answer_with_context(query:str, context:list[dict]) -> str:
    llm, tokenizer = _load_gen_model()

    prompt = build_prompt(query, context, tokenizer)
    
    print("\n--- Generating Answer ---")
    
    # Use the Llama object to generate the response
    response = llm(
        prompt,
        max_tokens=256,
        echo=False,  # Do not repeat the prompt in the output
        stop=["<|eot_id|>", "<|end_of_text|>"], # Tokens to stop generation at
    )

    answer = response["choices"][0]["text"].strip()

    print(answer)

    return answer