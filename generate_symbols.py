from config import *
from generator import (
    generate_vectors,
    generate_map,
    normalize_vectors,
    generate_shapes,
)
from tabulate import tabulate
from matplotlib import pyplot as plt
import argparse


def create_language(
    words_path: str,
    seed: int,
    width: int,
    height: int,
    scale: float,
    octaves: int,
    persistence: float,
    lacunarity: float,
    symbol_size: int,
    perplexity: float,
    image_directory: str,
    verbose: bool = False,
):
    words = tuple(open(words_path).read().split())

    vectors = generate_vectors(words)
    normalized_vectors = normalize_vectors(
        height=height,
        symbol_size=symbol_size,
        perplexity=perplexity,
        seed=seed,
        vectors=vectors,
        words=words,
    )
    map = generate_map(seed, width, height, scale, octaves, persistence, lacunarity)

    if verbose:
        table = []
        for i, vector in enumerate(normalized_vectors):
            table.append([words[i], vector[0], vector[1]])

        print(tabulate(table, headers=["Word", "X", "Y"]))

        plt.imshow(map, cmap="gray")
        for i, word in enumerate(words):
            normalized_vectors[i][0] = int(normalized_vectors[i][0])
            normalized_vectors[i][1] = int(normalized_vectors[i][1])

            plt.annotate(
                word,
                (normalized_vectors[i][0] + 10, normalized_vectors[i][1] + 10),
                color="r",
                size=10,
            )
            plt.scatter(
                normalized_vectors[i][0], normalized_vectors[i][1], color="r", s=2
            )

        plt.show()

    generate_shapes(symbol_size, image_directory, words, map, normalized_vectors)

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="galactica generator")

    parser.add_argument("verbose", type=bool)

    args = parser.parse_args()

    create_language(
        words_path,
        seed,
        width,
        height,
        scale,
        octaves,
        persistence,
        lacunarity,
        symbol_size,
        perplexity,
        image_directory,
        args.verbose,
    )
