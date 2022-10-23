from typing import Tuple
from states.state import State
from pygame.sprite import Sprite
from constants import BLACK, RESOURCES_DIR, MOVESET
import pygame as pg

class Enemy(Sprite):
    def __init__(self, game, attr: MOVESET, pos):
        super().__init__()
        image = pg.image.load(f'{RESOURCES_DIR}/graphics/innman.png').convert()
        image.set_colorkey(BLACK)
        self.last_updated, self.current_frame = 0, 0
        self.game = game
        self.health = 200
        self.strength = 20
        self.move_set: list[MOVESET] = [
            MOVESET.ATT, MOVESET.DEF, attr
        ]
        self.buff = 1
        self.debuff = 0
        self.attr = attr
        self.state = MOVESET.ATT
        # Hard code frames
        self.walking_frames = {
            'left': [
                image.subsurface(0, 32, 32, 32),
                image.subsurface(32, 32, 32, 32),
            ],
            'right': [
                image.subsurface(64, 32, 32, 32),
                image.subsurface(96, 32, 32, 32),
            ],
            'up': [
                image.subsurface(0, 0, 32, 32),
                image.subsurface(32, 0, 32, 32),
            ],
            'down': [
                image.subsurface(64, 0, 32, 32),
                image.subsurface(96, 0, 32, 32),
            ],
        }
        self.image = self.walking_frames['right'][0]
        # Only the feet should be collided with objects, not whole body
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.feet = pg.Rect(0, 0, self.rect.width * 0.5, 8)

    def update(self, dt: float) -> None:
        # animation
        now = pg.time.get_ticks()
        if now - self.last_updated > 200:
            self.last_updated = now
            self.current_frame = (self.current_frame + 1) % len(self.walking_frames['right'])
            self.image = self.walking_frames['right'][self.current_frame]

    def fight(self, target)->None:
        if self.state == MOVESET.ATT:
            attack = self.strength*(self.buff-self.debuff)
            if attack<0:
                attack=0
            if self.attr == target.attr and target.state == MOVESET.DEF:
                attack = 0
            target.health-=attack
        if self.state == MOVESET.DEBUFF:
            if target == self:
                target.buff += 0.1
            else:
                target.debuff-=0.1

class Player(Sprite):
    def __init__(self, game, avatar, pos):
        super().__init__()
        self.last_updated, self.current_frame = 0, 0
        self.game = game
        self.health = 200
        self.strength = 20
        self.move_set: list[MOVESET] = avatar.move_set
        self.buff = avatar.buff
        self.debuff = avatar.debuff
        self.attr = avatar.attr
        self.state = MOVESET.ATT
        # Hard code frames
        
        self.image = avatar.walking_frames['right'][0]
        # Only the feet should be collided with objects, not whole body
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.feet = pg.Rect(0, 0, self.rect.width * 0.5, 8)

    def update(self, dt: float) -> None:
        # animation
        now = pg.time.get_ticks()
        if now - self.last_updated > 200:
            self.last_updated = now
            self.current_frame = (self.current_frame + 1) % len(self.walking_frames['right'])
            self.image = self.walking_frames['right'][self.current_frame]

    def fight(self, target)->None:
        if self.state == MOVESET.ATT:
            attack = self.strength*(self.buff-self.debuff)
            if attack<0:
                attack=0
            if self.attr == target.attr and target.state == MOVESET.DEF:
                attack = 0
            target.health-=attack
        if self.state == MOVESET.DEBUFF:
            if target == self:
                target.buff += 0.1
            else:
                target.debuff-=0.1

class Battle(State):
    def __init__(self, game, player):
        super().__init__(game)
        self.player = player
        self.player_pos = (700,50)
        self.fool_pos = (50,50)
        self.fool = Enemy(game, MOVESET.WATER)
        self.player_wait_time = 0
        self.player_action_cooldown = 60
        self.bg= pg.image.load(f'{RESOURCES_DIR}/graphics/selectionbox.png').convert()
        self.bg = pg.transform.scale(self.bg,(800, 600))
        self.fighting = True
        

    def update(self, delta_time, actions):
        if actions is Tuple:
            self.player_wait_time+=delta_time
            if self.player_wait_time>=self.player_action_cooldown:
                self.player_wait_time = 0
                pass
        else:
            if actions['change']:
                self.player.change_attr()
            if actions['act']:
                self.player.state = MOVESET.ATT
            if actions['debuff']:
                self.player.state = MOVESET.DEBUFF
            if actions['def']:
                self.player.state = MOVESET.DEF 

    def render(self, surface):
        surface.fill(BLACK)
        self.game.screen.blit(self.bg, (0, 0))
        self.game.screen.blit(self.player.image,self.player_pos)
        self.game.screen.blit(self.fool.image,self.fool_pos)
        
