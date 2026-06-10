# caption_engine.py

def split_words(script):
    return script.split()

def chunk_words(words, size=3):
    chunks = []
    for i in range(0, len(words), size):
        chunks.append(" ".join(words[i:i+size]))
    return chunks