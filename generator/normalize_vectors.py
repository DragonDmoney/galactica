import numpy as np
from sklearn.manifold import TSNE
from .cache import get_cache, save_cache
from typing import List


def normalize_vectors(
    height: int, symbol_size: int, perplexity: float, seed: int, vectors, words
) -> List:
    key = f"{height}-{symbol_size}-{perplexity}-{seed}-{words}"

    e, v = get_cache(key)
    if e:
        return v

    tsne = TSNE(n_components=2, random_state=seed, perplexity=perplexity)
    word_embeddings = tsne.fit_transform(vectors)

    # normalize word_embeddings to be between symbol_size and height-symbol_size
    word_embeddings = word_embeddings - np.min(word_embeddings, axis=0)
    word_embeddings = word_embeddings / np.max(word_embeddings, axis=0)
    word_embeddings = word_embeddings * (height - symbol_size * 2) + symbol_size

    save_cache(key, word_embeddings)

    return word_embeddings
