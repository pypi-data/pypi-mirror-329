from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button, Label

from mastermind.game import Game
from mastermind.widgets.code_peg import CodePeg


class Row(Horizontal):
    def __init__(self, game: Game, row_number: int) -> None:
        super().__init__(classes="row")

        self.game = game

        self.row_number = row_number

        self.code_pegs: list[CodePeg] = [
            CodePeg(self.game) for _ in range(self.game.num_pegs)
        ]

        check_button_label: str = ("❔ " * self.game.num_pegs)[:-1]
        self.check_button: Button = Button(
            check_button_label, classes="check", id="check", action="app.check_code"
        )

    def compose(self) -> ComposeResult:
        yield Label(f"{self.row_number:02}", classes="num")
        for code_peg in self.code_pegs:
            yield code_peg
        yield self.check_button
