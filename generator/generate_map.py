from tqdm import tqdm
from .cache import get_cache, save_cache
import numpy as np
import noise


def generate_noise_map(width, height, scale, octaves, persistence, lacunarity, seed):
    noise_map = np.zeros((width, height))
    for x in tqdm(range(width)):
        for y in range(height):
            noise_map[x][y] = noise.pnoise2(
                x * scale,
                y * scale,
                octaves=octaves,
                persistence=persistence,
                lacunarity=lacunarity,
                repeatx=1024,
                repeaty=1024,
                base=seed,
            )
    return noise_map


# get a square submap of size size
def square(map, x, y, size):
    return map[
        x - int(size / 2) : x + int(size / 2), y - int(size / 2) : y + int(size / 2)
    ]


# threshold the noise map
def threshold_noise(map, threshold):
    return np.where(map < threshold, 0, 1)


# add empty zeros to the edges of the array
def pad_array(array, padding, constant=1):
    return np.pad(array, padding, "constant", constant_values=constant)


def generate_map(
    seed: int,
    width: int,
    height: int,
    scale: float,
    octaves: int,
    persistence: float,
    lacunarity: float,
):
    # check cache
    key = f"{seed}-{width}-{height}-{scale}-{octaves}-{persistence}-{lacunarity}"
    e, map = get_cache(key)
    if e:
        return map

    np.random.seed(seed)

    map = generate_noise_map(
        width, height, scale, octaves, persistence, lacunarity, seed
    )
    map = threshold_noise(map, 0)

    save_cache(key, map)

    return map
