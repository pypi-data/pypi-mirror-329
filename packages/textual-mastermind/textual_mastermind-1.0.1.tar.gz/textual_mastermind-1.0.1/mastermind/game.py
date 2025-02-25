import random

from mastermind.settings import app_settings


class Game:
    def __init__(self) -> None:
        self.num_rows = app_settings.variation.num_rows
        self.num_pegs = app_settings.variation.num_pegs
        self.num_colors = app_settings.variation.num_colors

        colors: list[int] = list(range(1, self.num_colors + 1))
        if app_settings.blank_color:
            colors.append(0)

        self.mastercode: list[int]
        if not app_settings.duplicate_colors:
            self.mastercode = random.sample(colors, k=self.num_pegs)
        else:
            self.mastercode = random.choices(colors, k=self.num_pegs)

    def check_breaker_code(self, breaker_code: list[int]) -> tuple[int, int]:
        num_red_pegs: int = 0
        num_white_pegs: int = 0

        red_idxs: list[int] = []
        for i, breaker_code_color in enumerate(breaker_code):
            if self.mastercode[i] == breaker_code_color:
                num_red_pegs += 1
                red_idxs.append(i)

        breaker_code_no_reds = [
            color for i, color in enumerate(breaker_code) if i not in red_idxs
        ]
        mastercode_no_reds = [
            color for i, color in enumerate(self.mastercode) if i not in red_idxs
        ]

        for color in breaker_code_no_reds:
            if color in mastercode_no_reds:
                num_white_pegs += 1

        return num_red_pegs, num_white_pegs

    def get_mastercode(self) -> list[int]:
        return self.mastercode
