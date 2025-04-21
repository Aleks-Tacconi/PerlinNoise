import math
import random
from dataclasses import dataclass, field
from typing import List
from enum import Enum

OCTAVES = 5     # layers of noise applied
LACUNARITY = 2  # how much smaller each chunk gets per octave
                # increasing this increases the finer details
PERSISTENCE = 1 # controls the impact reduction of each octave
CHUNK_SIZE = 80

# used for normalization
MAX_HEIGHT = 60
MIN_HEIGHT = -60

SEED = 123


class Side(Enum):
    TOP = 0
    BOTTOM = 1
    LEFT = 0
    RIGHT = 1


class Corner(Enum):
    TOP_LEFT = [Side.TOP, Side.LEFT]
    TOP_RIGHT = [Side.TOP, Side.RIGHT]
    BOTTOM_LEFT = [Side.BOTTOM, Side.LEFT]
    BOTTOM_RIGHT = [Side.BOTTOM, Side.RIGHT]


@dataclass
class Vector:
    i: int | float = field()
    j: int | float = field()


def dot_product(v1: Vector, v2: Vector) -> int | float:
    i = v1.i * v2.i
    j = v1.j * v2.j

    return i + j


def lerp(a: int | float, b: int | float, t: int | float) -> int | float:
    return a + (t * (b - a))


def fade(t: int | float) -> int | float:
    return (6 * t * t * t * t * t) - (15 * t * t * t * t) + (10 * t * t * t)


def get_influence_vector(x: int, y: int, corner: Corner, chunk_size: float | int) -> Vector:
    seed_x = (x // chunk_size) + corner.value[1].value
    seed_y = (y // chunk_size) + corner.value[0].value
    random.seed(f"{seed_x}|{seed_y}|{SEED}")

    angle = random.randint(0, 360)
    i = math.cos(math.radians(angle))
    j = math.sin(math.radians(angle))

    return Vector(i, j)

def get_offset_vector(x: int, y: int, corner: Corner, chunk_size: float | int) -> Vector:
    i = x % chunk_size
    j = y % chunk_size

    if corner.value[1].value == 1:
        i -= chunk_size
    if corner.value[0].value == 1:
        j -= chunk_size

    return Vector(i, j)

def get_scalar(x: int, y: int, corner: Corner, chunk_size: float | int) -> int | float:
    influence_vector = get_influence_vector(x, y, corner, chunk_size)
    offset_vector = get_offset_vector(x, y, corner, chunk_size)

    return dot_product(influence_vector, offset_vector)

def get_height(x: int, y: int, chunk_size: float | int) -> int | float:
    x_ratio = (x % chunk_size) / chunk_size
    y_ratio = (y % chunk_size) / chunk_size

    x_ratio = fade(x_ratio)
    y_ratio = fade(y_ratio)

    top = lerp(
        get_scalar(x, y, Corner.TOP_LEFT, chunk_size),
        get_scalar(x, y, Corner.TOP_RIGHT, chunk_size),
        x_ratio,
    )
    bottom = lerp(
        get_scalar(x, y, Corner.BOTTOM_LEFT, chunk_size),
        get_scalar(x, y, Corner.BOTTOM_RIGHT, chunk_size),
        x_ratio,
    )

    return lerp(top, bottom, y_ratio)

class PerlinNoise:
    def __init__(self, width: int, height: int) -> None:
        self.__width = width
        self.__height = height

        self._heightmap = [[-1 for _ in range(width)] for _ in range(height)]

        self.__generate_heightmap()

    def _apply_noise_at(self, x: int, y: int) -> None:
        influence = 1
        size = CHUNK_SIZE

        for _ in range(OCTAVES):
            height = get_height(x, y, size) * influence
            self._heightmap[y][x] += height

            influence //= PERSISTENCE
            size //= LACUNARITY

    def __generate_heightmap(self) -> None:
        for y in range(self.__height):
            for x in range(self.__width):
                self._apply_noise_at(x, y)

    def get_heightmap(self) -> List[List[int | float]]:
        heightmap = [
            [-1 for _ in range(len(self._heightmap[0]))]
            for _ in range(len(self._heightmap))
        ]

        # when using this method the landscape changes when using the InteractiblePerlinNoise class
        # heights = [height for row in self._heightmap for height in row]
        # max_height = max(heights)
        # min_height = min(heights)

        for y, row in enumerate(self._heightmap):
            for x, height in enumerate(row):
                heightmap[y][x] = (height - MIN_HEIGHT) / (MAX_HEIGHT - MIN_HEIGHT) 

        return heightmap
