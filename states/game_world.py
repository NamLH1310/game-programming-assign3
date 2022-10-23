from enum import Enum
from pickle import TRUE
import numpy.random
import pygame.image
import pyscroll
import pytmx
from pygame.sprite import Sprite

from constants import BLACK, RESOURCES_DIR, MOVESET
from states.battle import Battle
from states.pause_menu import PauseMenu
from states.state import State



class Player(Sprite):
    def __init__(self, game):
        super().__init__()
        image = pygame.image.load(f'{RESOURCES_DIR}/graphics/player.png').convert()
        image.set_colorkey(BLACK)
        self.last_updated, self.current_frame = 0, 0
        self.game = game
        self.health = 200
        self.max_health = 250
        self.strength = 10
        self.potion = 0
        self.live = TRUE
        self.move_set: list[MOVESET] = [
            MOVESET.ATT, MOVESET.DEF, MOVESET.ULT
        ]
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
        self.image = self.walking_frames['down'][0]
        self.rect = self.image.get_rect()
        self.direction = [0, 0]
        self.velocity = 2
        self.position = [0.0, 0.0]
        self.old_position = self.position
        self.direction = [0, 0]
        # Only the feet should be collided with objects, not whole body
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 8)

    def update(self, dt: float) -> None:
        actions = self.game.actions

        state: str | None = None
        direction_x = actions["right"] - actions["left"]
        direction_y = actions["down"] - actions["up"]

        if direction_y == 1:
            state = 'down'
        elif direction_y == -1:
            state = 'up'

        if direction_x == 1:
            state = 'right'
        elif direction_x == -1:
            state = 'left'

        # animation
        now = pygame.time.get_ticks()
        if state and now - self.last_updated > 200:
            self.last_updated = now
            self.current_frame = (self.current_frame + 1) % len(self.walking_frames[state])
            self.image = self.walking_frames[state][self.current_frame]

        self.old_position = self.position[:]
        self.position[0] += direction_x * self.velocity * dt
        self.position[1] += direction_y * self.velocity * dt
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self) -> None:
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom


class GameWorld(State):
    def __init__(self, game):
        """
        param game: game instance
        :type game: main.Game
        """
        super().__init__(game)
        tiled_map = pytmx.util_pygame.load_pygame(f'{RESOURCES_DIR}/data/grasslands.tmx')
        screen = game.screen
        self.cave: pygame.Rect | None = None
        self.walls: list[pygame.Rect] = []
        for obj in tiled_map.objects:
            if hasattr(obj, 'name') and obj.name == 'cave':
                self.cave = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                continue
            self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.map_layer = pyscroll.BufferedRenderer(
            data=pyscroll.data.TiledMapData(tiled_map),
            size=screen.get_size(),
            clamp_camera=False,
        )
        self.levels = [i + 1 for i in range(5)]
        self.map_layer.zoom = 2
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=2)

        # put the hero in the center of the map
        self.hero = game.player
        self.hero.position = list(self.map_layer.map_rect.center)

        # add our hero to the group
        self.group.add(self.hero)

    def update(self, delta_time, actions):
        if actions['pause']:
            PauseMenu(self.game).enter_state()
        elif actions['resize']:
            self.map_layer.set_size(self.game.screen.get_size())

        self.group.update(delta_time)
        distance = (self.hero.rect.x - self.map_layer.map_rect.center[0])**2 + (self.hero.rect.y - self.map_layer.map_rect.center[1])**2

        # 1 / 1000  chance of encounter enemy
        # if distance > 1000000 and int(numpy.random.uniform(0, 1000)) == 500:
            # TODO: spawn enemy
            # print('spawned')
            # self.game.fools.append(Enemy(self.game,attr[numpy.random.uniform(0, 11)%3] ))
            # self.game.fools[-1].position[0] = self.hero.position[0]+100+numpy.random.uniform(0, 11)
            # self.game.fools[-1].position[1] = self.hero.position[1]+100+numpy.random.uniform(0, 11)
        Battle(self.game,self.hero).enter_state()
        # pass
            

        for sprite in self.group.sprites():
            if isinstance(sprite, Player):
                if sprite.feet.collidelist(self.walls) > -1:
                    sprite.move_back()
                elif sprite.feet.colliderect(self.cave):
                    # TODO: BOSS fight
                    pass

    def render(self, surface):
        map_rect = self.map_layer.map_rect

        offset_x = surface.get_width() >> 2
        offset_y = surface.get_height() >> 2

        camera_pos = list(self.hero.rect.center)
        if offset_x >= self.hero.rect.centerx:
            camera_pos[0] = offset_x
        if self.hero.rect.centerx >= map_rect.width - offset_x:
            camera_pos[0] = map_rect.width - offset_x

        if offset_y >= self.hero.rect.centery:
            camera_pos[1] = offset_y
        elif self.hero.rect.centery >= map_rect.height - offset_y:
            camera_pos[1] = map_rect.height - offset_y

        self.group.center(tuple(camera_pos))

        # draw the map and all sprites
        self.group.draw(surface)
