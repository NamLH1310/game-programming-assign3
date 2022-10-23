from constants import BLACK
from states.game_world import GameWorld
from states.state import State

import pygame_gui as pggui
import pygame as pg


class Menu(State):
    def __init__(self, game, ui_manager):
        """
        :param game: game instance
        :type game: main.Game
        :param ui_manager: pygame_gui manager
        :type ui_manager: pygame_gui.UIManager
        """
        State.__init__(self, game, None)
        self.ui_manager = ui_manager
        button_w, button_h = self.game.SCREEN_WIDTH >> 3, self.game.SCREEN_HEIGHT >> 3
        self.start_button = pggui.elements.UIButton(
            pg.Rect((self.game.SCREEN_WIDTH - button_w) >> 1, (self.game.SCREEN_HEIGHT >> 1) - button_h, button_w, button_h),
            'start',
            self.ui_manager,
            object_id='start')
        self.quit_button = pggui.elements.UIButton(
            pg.Rect((self.game.SCREEN_WIDTH - button_w) >> 1, self.game.SCREEN_HEIGHT >> 1, button_w, button_h),
            'quit',
            self.ui_manager,
            object_id='quit')

    def update(self, delta_time, actions):
        match actions['button_click']:
            case self.start_button:
                GameWorld(self.game).enter_state()
            case self.quit_button:
                self.game.running = False
                self.game.playing = False

        self.game.reset_keys()

    def render(self, surface):
        surface.fill(BLACK)
        self.ui_manager.draw_ui(surface)
