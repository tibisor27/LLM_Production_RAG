import nltk
from config import config
from spacy.lang.en import English
import re

nlp = English()
nlp.add_pipe("sentencizer")

SENTS_PER_CHUNK = config.SENTS_PER_CHUNK
SENT_OVERLAP = config.SENT_OVERLAP
MAX_TOKENS = config.MAX_TOKENS
MIN_TOKENS = config.MIN_TOKENS

def split_sentences(text:str) -> list:
    return [str(sent) for sent in nlp(text).sents]

def chunk_page_by_sentences(sentences:list, sents_per_chunk: int = SENTS_PER_CHUNK, overlap: int = SENT_OVERLAP, max_tokens: int = MAX_TOKENS, min_tokens: int = MIN_TOKENS):
    if not sentences:
        return []
    chunks,current_chunk,current_tokens = [],[],0

    for i, sentence in enumerate(sentences):
        sentence_tokens_count = len(sentence) // 4
        if (current_tokens + sentence_tokens_count > max_tokens and current_chunk) or (len(current_chunk) >= sents_per_chunk):
            if current_chunk:
                chunks.append(" ".join(current_chunk))

            if overlap > 0:
                overlap_start_index = max(0,len(current_chunk) - overlap)
                new_chunk_sents = current_chunk[overlap_start_index:]
            else:
                new_chunk_sents = []
            
            new_chunk_sents.append(sentence)

            current_chunk = new_chunk_sents
            current_tokens = sum(len(s) //4 for s in current_chunk)
        else:
            current_chunk.append(sentence)
            current_tokens += sentence_tokens_count
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

# def sentence_list(list):
#     for item in list:
#         item["sentences"] = list(nlp(item["text"]).sents)
#         item["sentences"] = [str(sent) for sent in item["sentences"]]
#     return list

def chunks_and_metadata(pages_list:list[dict])->list[dict]:
    chunk_and_metadata = []
    for page in pages_list:
        sents = split_sentences(page["text"])
        if len(sents) <= 3:
            continue  #skip pages with less than 3 sentences - ex pages with titles and subtitles
        chunks = chunk_page_by_sentences(sents)
        
        for chunk in chunks:
            chunk_dict = {}
            chunk_dict["page_number"] = page["page_number"]

            #Join the sentence together into a paragraph-like structure, aka a chunk(so they are a single strin)
            joined_sentence_chunk = "".join(chunk).replace("  "," ").strip() #every sentence in one string(no spaces)
            # ".A" -> ". A" for any full-stop/capital letter combo
            joined_sentence_chunk = re.sub(r'\.([A-Z])', r'. \1', joined_sentence_chunk)

            chunk_dict["sentence_chunk"] = joined_sentence_chunk
            chunk_dict["chunk_char_count"] = len(joined_sentence_chunk)
            chunk_dict["chunk_word_count"] = len([word for word in joined_sentence_chunk.split(" ")])
            chunk_dict["chunk_token_count"] = len(joined_sentence_chunk) // 4
            chunk_dict["chunk_sentence_count"] = len(list(nlp(joined_sentence_chunk).sents))
            chunk_and_metadata.append(chunk_dict)

            chunk_and_metadata.append(chunk_dict)

    return chunk_and_metadata
