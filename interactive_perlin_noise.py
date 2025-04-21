from perlin_noise import (
    CHUNK_SIZE,
    LACUNARITY,
    OCTAVES,
    PERSISTENCE,
    PerlinNoise,
    get_height,
)


class InteractivePerlinNoise(PerlinNoise):
    def __init__(self, width: int, height: int) -> None:
        self.__pos = [0, 0]

        super().__init__(width, height)

    def _apply_noise_at(self, x: int, y: int) -> None:
        influence = 1
        size = CHUNK_SIZE

        for _ in range(OCTAVES):
            height = get_height(x - self.__pos[0], y - self.__pos[1], size) * influence
            self._heightmap[y][x] += height

            influence //= PERSISTENCE
            size //= LACUNARITY

    def w(self) -> None:
        self.__pos[1] += 1

        row = [-1 for _ in range(len(self._heightmap[0]))]
        self._heightmap.pop(-1)
        self._heightmap.insert(0, row)

        for x in range(len(self._heightmap[0])):
            self._apply_noise_at(x, 0)

    def s(self) -> None:
        self.__pos[1] -= 1

        row = [-1 for _ in range(len(self._heightmap[0]))]
        self._heightmap.pop(0)
        self._heightmap.append(row)

        for x in range(len(self._heightmap[0])):
            self._apply_noise_at(x, len(self._heightmap) - 1)

    def a(self) -> None:
        self.__pos[0] += 1

        for y, row in enumerate(self._heightmap):
            row.pop()
            row.insert(0, -1)
            self._apply_noise_at(0, y)

    def d(self) -> None:
        self.__pos[0] -= 1

        for y, row in enumerate(self._heightmap):
            row.pop(0)
            row.append(-1)
            self._apply_noise_at(len(self._heightmap) - 1, y)
