import time
from typing import Tuple

import pygame as pg
import pygame.event
import pygame_gui as pggui

from constants import TARGET_FPS, attr, MOVESET
from states.battle import Battle, Enemy
from states.game_world import Player, Treasure
from states.menu import Menu
from states.state import State


class Game:
    def __init__(self):
        pg.init()
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 800, 600
        self.screen = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pg.RESIZABLE)
        self.ui_manager = pggui.UIManager((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 'assets/themes/button_theme.json')
        self.dt, self.prev_time = 0.0, 0.0
        self.running, self.playing, self.win, self.lose = True, True, False, False
        self.actions: dict[str, bool | Tuple[int,int]| int | pggui.elements.UIButton | None] = {
            'left': 360,
            'right': 360,
            'up': 360,
            'down': 360,
            'start': False,
            'button_click': None,
            'pause': False,
            'resize': True,
            'mouse_click': None,
            'change': False,
            'act': False,
            'def': False,
            'debuff': False,
            'ult': False
        }
        self.state_stack: list[State] = []
        self.init_state()
        self.player = Player(self)
        self.treasures= list([Treasure(self, MOVESET.FIRE), Treasure(self, MOVESET.EARTH),
            Treasure(self, MOVESET.WATER), Treasure(self, MOVESET.ULT)])
        

    def init_screen(self, width, height):
        self.screen = pg.display.set_mode((width, height), pg.RESIZABLE)

    def run(self):
        while self.running:
            self.game_loop()
            if self.win:
                print('win')
            if self.lose:
                print('lose')

    def game_loop(self):
        while self.playing:
            self.handle_dt()
            self.handle_events()
            self.update()
            self.render()

    def handle_dt(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def handle_events(self):
        
        self.actions['change'] = self.actions['act'] = self.actions['def'] =self.actions['debuff']= self.actions['ult']=False
        self.actions['down'] = self.actions['up'] = 0
        self.actions['left'] = self.actions['right'] = 0

        # handle events and single key pressed
        self.actions['mouse_click'] = None
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    self.playing = False
                    self.running = False
                case pg.KEYDOWN:
                    self.actions['pause'] = event.key == pg.K_ESCAPE and not self.actions['pause']
                case pg.VIDEORESIZE:
                    self.init_screen(event.w, event.h)
                case pggui.UI_BUTTON_PRESSED:
                    self.actions['button_click'] = event.ui_element
                case pg.MOUSEBUTTONDOWN:
                    if isinstance(self.state_stack[-1],Battle):
                        self.actions['mouse_click'] = pg.mouse.get_pos()
            self.ui_manager.process_events(event)

        # handle consecutive key pressed
        pressed = pygame.key.get_pressed()
        if isinstance(self.state_stack[-1],Battle)==False:
            if pressed[pg.K_a]:
                self.actions['left'] = 1
            elif pressed[pg.K_d]:
                self.actions['right'] = 1

            if pressed[pg.K_s]:
                self.actions['down'] = 1
            elif pressed[pg.K_w]:
                self.actions['up'] = 1
        else:
            if pressed[pg.K_x]:
                self.actions['change'] = True
            elif pressed[pg.K_z]:
                self.actions['act'] = True
            elif pressed[pg.K_c]:
                self.actions['debuff'] = True
            elif pressed[pg.K_d]:
                self.actions['def'] = True
            elif pressed[pg.K_v]:
                self.actions['ult'] = True

    def update(self):
        dt = self.dt * TARGET_FPS
        self.ui_manager.update(dt)
        self.state_stack[-1].update(dt, self.actions)

    def render(self):
        self.state_stack[-1].render(self.screen)
        self.screen.blit(pg.transform.scale(self.screen, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0, 0))
        pg.display.update()

    def reset_keys(self):
        for action, action_value in self.actions.items():
            if not action_value:
                continue
            self.actions[action] = False if type(action_value) is bool else None

    def init_state(self):
        self.state_stack.append(Menu(self, self.ui_manager))


if __name__ == '__main__':
    Game().run()
