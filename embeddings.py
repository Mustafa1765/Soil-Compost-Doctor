"""
embeddings.py - Offline Deterministic Embedding Function for ChromaDB
======================================================================
Project: Soil & Compost Doctor (Hacktoberfest "Touch Grass" Challenge)
Description:
  Provides a 100% offline, zero-dependency embedding function for ChromaDB.
  Eliminates network timeouts and external model downloads so the entire
  vector database works without internet access anywhere outdoors.
"""

import math
import hashlib
import re
from typing import List, Dict
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings

# Domain vocabulary for plant health, soil conditions, and compost stages
DOMAIN_TERMS = [
    # Leaf & Plant terms
    "leaf", "leaves", "blight", "early", "late", "alternaria", "spot", "spots",
    "ring", "rings", "concentric", "target", "yellow", "yellowing", "chlorosis",
    "interveinal", "green", "veins", "vein", "powder", "powdery", "mildew",
    "white", "fungus", "fungal", "dust", "talcum", "spores", "rust", "orange",
    "pustules", "aphid", "aphids", "pest", "pests", "insect", "insects",
    "sticky", "honeydew", "sooty", "mold", "rot", "blossom", "end", "calcium",
    "sunken", "black", "tomato", "potato", "squash", "zucchini", "cucumber",
    "rose", "beans", "chewing", "holes", "foliage", "stem", "stems", "prune",
    "cut", "shears", "spray", "baking", "soda", "neem", "oil", "soap",
    # Soil terms
    "soil", "clay", "compacted", "hard", "dense", "cracked", "crust", "puddle",
    "puddling", "sand", "sandy", "gritty", "depleted", "loose", "drainage",
    "drains", "waterlogged", "water", "wet", "muddy", "anaerobic", "swamp",
    "swampy", "sour", "acid", "acidic", "alkaline", "chalky", "limestone",
    "ph", "lime", "ash", "wood", "sulfur", "rock", "broadfork", "fork", "dig",
    "aeration", "aerate", "trench", "raised", "bed", "beds", "mulch", "straw",
    # Compost terms
    "compost", "pile", "bin", "heap", "smell", "smelly", "stink", "stalled",
    "foul", "rotten", "egg", "eggs", "ammonia", "sulfur", "slimy", "brown",
    "browns", "carbon", "green", "greens", "nitrogen", "pitchfork", "turn",
    "turning", "hot", "thermophilic", "heat", "steam", "temperature", "temp",
    "finished", "cured", "gold", "humus", "crumbly", "earthy", "forest",
    "dark", "decompose", "breakdown", "flies", "maggot", "maggots", "rats",
    "rodents", "food", "scraps", "grass", "clippings", "leaves", "cardboard"
]

VOCAB: Dict[str, int] = {term: idx for idx, term in enumerate(sorted(set(DOMAIN_TERMS)))}
BASE_DIM = len(VOCAB)
HASH_SLOTS = 64
TOTAL_DIM = BASE_DIM + HASH_SLOTS

STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "in", "on", "of", "for", "to",
    "and", "or", "with", "by", "at", "it", "this", "that", "be", "as", "from",
    "into", "your", "my", "our", "all", "so", "up", "out", "if", "not", "have"
}

class OfflineGardenEmbedding(EmbeddingFunction):
    """
    100% offline, domain-aligned embedding function for agricultural RAG.
    Combines vocabulary projection and hashing trick for OOV terms.
    Provides fast, deterministic cosine similarity without downloads.
    """
    def __init__(self, dim: int = TOTAL_DIM):
        self.dim = dim

    def _tokenize(self, text: str) -> List[str]:
        return [w for w in re.findall(r"\b[a-zA-Z0-9_\-]+\b", text.lower()) if w not in STOPWORDS]

    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for doc in input:
            vector = [0.0] * self.dim
            words = self._tokenize(doc)
            
            for w in words:
                if w in VOCAB:
                    # Give high weight to matched agricultural domain terms
                    vector[VOCAB[w]] += 2.0
                else:
                    # Hash into auxiliary slots
                    h = int(hashlib.md5(w.encode("utf-8")).hexdigest(), 16) % HASH_SLOTS
                    vector[BASE_DIM + h] += 0.5

            # Bigram matching for common phrases
            for i in range(len(words) - 1):
                bigram = f"{words[i]}_{words[i+1]}"
                if words[i] in VOCAB and words[i+1] in VOCAB:
                    vector[VOCAB[words[i]]] += 1.5
                    vector[VOCAB[words[i+1]]] += 1.5

            # L2 normalize
            norm = math.sqrt(sum(v * v for v in vector))
            if norm > 0:
                vector = [v / norm for v in vector]

            embeddings.append(vector)
        return embeddings

def get_embedding_function():
    """Returns the offline embedding function for ChromaDB collections."""
    return OfflineGardenEmbedding()
