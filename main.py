import tkinter as tk
from typing import Callable

from interactive_perlin_noise import InteractivePerlinNoise


class GUI(tk.Tk):
    def __init__(self, pixel_size: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.__pixel_size = pixel_size

        self.__noise = InteractivePerlinNoise(width=200, height=200)
        self.__heightmap = self.__noise.get_heightmap()

        self.geometry("1000x1000")
        self.resizable(False, False)
        self.focus_set()
        self.bind("<w>", lambda _: self.__key_press(self.__noise.w))
        self.bind("<s>", lambda _: self.__key_press(self.__noise.s))
        self.bind("<d>", lambda _: self.__key_press(self.__noise.d))
        self.bind("<a>", lambda _: self.__key_press(self.__noise.a))

        self.__canvas = tk.Canvas(self)
        self.__canvas.pack(fill=tk.BOTH, expand=tk.YES)

    def __key_press(self, func: Callable) -> None:
        func()
        self.__heightmap = self.__noise.get_heightmap()

    def __draw_pixel(self, x: int, y: int, color: str) -> None:
        x1 = x * self.__pixel_size
        y1 = y * self.__pixel_size

        x2 = x1 + self.__pixel_size
        y2 = y1 + self.__pixel_size

        self.__canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    def __draw_heightmap(self) -> None:
        for y, row in enumerate(self.__heightmap):
            for x, val in enumerate(row):
                rgb = int(val * 255)
                rgb = max(min(rgb, 255), 0)

                if rgb >= 100:
                    color = "#2222{:02x}".format(255 - rgb)
                elif rgb >= 90:
                    norm = (rgb - 90) / (100 - 90)

                    if norm < 0.7:
                        norm += (0.7 - norm) / 2

                    r = int(210 * norm)
                    g = int(180 * norm)
                    b = int(140 * norm)
                    color = "#{:02x}{:02x}{:02x}".format(r, g, b)
                elif rgb >= 60:
                    color = "#11{:02x}05".format(rgb)
                elif rgb >= 40:
                    color = "#00{:02x}00".format(rgb)
                else:
                    color = "#" + "{:02x}".format(rgb) * 3

                self.__draw_pixel(x, y, color)

    def main(self) -> None:
        while True:
            self.__canvas.delete("all")
            self.__draw_heightmap()
            self.update()
            self.update_idletasks()


def main() -> None:
    gui = GUI(pixel_size=5)
    gui.main()


if __name__ == "__main__":
    main()
