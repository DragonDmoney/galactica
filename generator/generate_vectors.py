from typing import Tuple
from .cache import get_cache, save_cache
import gensim.downloader as api
from tqdm import tqdm


def generate_vectors(words: Tuple[str]):
    # check cache for vectors
    e, vectors = get_cache(str(words))
    if e:
        return vectors

    print(f"Loaded {len(words)} words.")

    # load model
    print("Loading pre-trained Word2Vec model...")
    model = api.load("word2vec-google-news-300")
    print("Done.")

    vectors = []

    for word in tqdm(words):
        try:
            embedding = model[word]
            vectors.append(embedding)
        except KeyError as e:
            print(f"Word '{word}' not found in model.")

    print(f"Generated {len(vectors)} vectors.")

    save_cache(str(words), vectors)

    return vectors
