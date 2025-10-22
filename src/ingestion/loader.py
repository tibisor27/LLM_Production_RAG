import re
import fitz
from tqdm.auto import tqdm
from ..config import config


def text_formatter(text: str) -> str:
    text = text.replace("\r", " ")
    text = re.sub(r"-\s*\n\s*", "", text)     # join "nutri-\n tion" => "nutrition"
    text = re.sub(r"\s+\n", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = text.replace("\n", " ").strip()
    return text

def load_pdf(pdf_path: str) -> list[dict]:
    pages_and_texts = []
    doc = fitz.open(pdf_path)
    for page_number, page in tqdm(enumerate(doc)):
        text = page.get_text()
        text = text_formatter(text)
        pages_and_texts.append({
            "page_number": page_number - 41, #actual text starts at page 42
            "page_char_count": len(text),
            "page_word_count": len(text.split(" ")),
            "page_token_count": len(text)/4,
            "text": text
        })

    return pages_and_texts