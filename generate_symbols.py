from config import *
from generator import (
    generate_vectors,
    generate_map,
    normalize_vectors,
    generate_shapes,
    colorize_map,
)
from tabulate import tabulate
from matplotlib import pyplot as plt
import argparse
import random
import math


def explorer(
    normalized_vectors: list,
    words: list,
    nearby_words: int = 5,
):
    print("Entering explorer... Type 'c' to exit.")

    max_distance = math.sqrt((width - symbol_size) ** 2 + (height - symbol_size) ** 2)

    while True:
        print(f"Random words: {[random.choice(words) for _ in range(5)]}")

        word = input("Enter a word (or exit): ")
        if word == "c":
            break
        try:
            index = words.index(word)
        except ValueError:
            print("Word not found.")
            continue

        x, y = normalized_vectors[index]

        distances = []
        for i, vector in enumerate(normalized_vectors):
            distance = ((x - vector[0]) ** 2 + (y - vector[1]) ** 2) ** 0.5
            distances.append(
                (
                    words[i],
                    distance,
                    str(round((distance / max_distance) * 100, 3)) + "%",
                )
            )

        distances.sort(key=lambda x: x[1])

        print(
            tabulate(
                distances[: nearby_words + 1],
                headers=["Word", "Distance", "Percentage of max distance"],
            )
        )


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
    colorized: bool,
    colorized_scale: float = 0,
    colorized_octaves: int = 0,
    colorized_persistence: float = 0,
    colorized_lacunarity: float = 0,
    color_complexity: int = 0,
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

    if colorized:
        map = colorize_map(
            map,
            colorized_scale,
            colorized_octaves,
            colorized_persistence,
            colorized_lacunarity,
            seed,
            number_colors=color_complexity,
        )

    if verbose:
        table = []
        for i, vector in enumerate(normalized_vectors):
            table.append([words[i], vector[0], vector[1]])

        print(tabulate(table, headers=["Word", "X", "Y"]))

        if colorized:
            plt.imshow(map)
        else:
            plt.imshow(map, cmap="gray")

        for i, word in enumerate(words):
            normalized_vectors[i][0] = int(normalized_vectors[i][0])
            normalized_vectors[i][1] = int(normalized_vectors[i][1])

            plt.annotate(
                word,
                (normalized_vectors[i][0] + 10, normalized_vectors[i][1] + 10),
                color="k",
                size=10,
            )
            plt.scatter(
                normalized_vectors[i][0], normalized_vectors[i][1], color="k", s=2
            )

        plt.show()

        x = input("Enter coordinate explorer? (y/n): ")
        if x == "y":
            explorer(normalized_vectors, words)
        else:
            pass

    generate_shapes(symbol_size, image_directory, words, map, normalized_vectors)

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="galactica",
        description="galactica generator",
        epilog="made by: dorian spiegel",
    )

    parser.add_argument("-v", "--verbose", action="store_true")

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
        colorized,
        colorized_scale,
        colorized_octaves,
        colorized_persistence,
        colorized_lacunarity,
        color_complexity,
        args.verbose,
    )
