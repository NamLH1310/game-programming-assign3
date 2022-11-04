import numpy
import pygame as pg

from constants import WHITE, BLACK
from states.state import State


class PauseMenu(State):
    def __init__(self, game):
        super().__init__(game)
        font = pg.font.SysFont('comicsans', 40)

        self.text: dict[str, pg.Surface] = {
            'quit': font.render('quit', True, WHITE),
            'continue': font.render('continue', True, WHITE),
        }

        self.canvas = self.game.screen.copy()
        self.indicator_coord = []
        self.index = 0

    def update(self, delta_time, actions):
        if actions['arrow_up']:
            self.index = (self.index - 1) % len(self.text)
        elif actions['arrow_down']:
            self.index = (self.index + 1) % len(self.text)
        elif actions['enter']:
            match self.index:
                case 1:
                    self.exit_state()
                case 0:
                    while len(self.game.state_stack) > 1:
                        self.game.state_stack.pop()

        self.game.reset_keys()

    def draw_indicator(self):
        h = self.text['quit'].get_height()
        x, y = self.indicator_coord[self.index]
        x -= numpy.int(numpy.sqrt(3) / 2 * h) + 20
        pg.draw.polygon(self.canvas, WHITE, ((x, y), (x, y + h), (x + numpy.int(numpy.sqrt(3) / 2 * h), y + h // 2)))

    def render(self, surface):
        self.canvas.fill(BLACK)

        sum_height = 0
        for v in self.text.values():
            sum_height += v.get_height()

        for k in self.text:
            w = self.text[k].get_width()
            x, y = (self.game.SCREEN_WIDTH - w) >> 1, (self.game.SCREEN_HEIGHT - sum_height) >> 1
            self.indicator_coord.append((x, y))
            self.canvas.blit(self.text[k], (x, y))

            sum_height -= self.text[k].get_height() << 1

        self.draw_indicator()
        surface.blit(self.canvas, (0, 0))