from states.state import State
from pygame.sprite import Sprite
from constants import BLACK, BLUE, GREEEN_KEY, GREEN, RED, RESOURCES_DIR, MOVESET, WHITE, YELLOW, attr
import pygame as pg
import numpy.random


class Enemy(Sprite):
    def __init__(self, game, attr: MOVESET, pos):
        super().__init__()
        image = pg.image.load(f'{RESOURCES_DIR}/graphics/innman.png').convert()
        image.set_colorkey(WHITE)
        self.last_updated, self.current_frame = 0, 0
        self.game = game
        self.max_health = 200
        self.health = 200
        self.strength = 20
        self.move_set: list[MOVESET] = [
            MOVESET.ATT, MOVESET.DEF, MOVESET.DEBUFF
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
        self.image = pg.transform.scale(self.walking_frames['down'][0],(250,250)) 
        # Only the feet should be collided with objects, not whole body
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.feet = pg.Rect(0, 0, self.rect.width * 0.5, 8)

    def update(self, dt: float) -> None:
        # animation
        now = pg.time.get_ticks()
        if now - self.last_updated > 200:
            self.last_updated = now
            self.current_frame = (self.current_frame + 1) % len(self.walking_frames['down'])
            self.image = self.walking_frames['down'][self.current_frame]

    def fight(self, target)->None:
        if self.state == MOVESET.ATT:
            attack = self.strength*(self.buff-self.debuff)
            if attack<0:
                attack=0
            if self.attr == target.attr and target.state == MOVESET.DEF:
                attack = 0
            target.health-=attack
        elif self.state == MOVESET.DEBUFF:
            target.debuff-=0.1
        elif self.state == MOVESET.DEF:
            attack = self.strength * 2
            if target.state == MOVESET.DEF:
                target.health-=attack
            self.buff+=0.1
    def act(self, player):
        #TODO lam con ai hay cai action list cho may con quai di/ mob
        
        pass
    

class Boss(Enemy):
    def __init__(self, game, attr: MOVESET, pos):
        super().__init__(game, attr, pos)
        image = pg.image.load(f'{RESOURCES_DIR}/graphics/king.png').convert()
        image.set_colorkey(GREEEN_KEY)
        self.last_updated, self.current_frame = 0, 0
        self.game = game
        self.max_health = 1500
        self.health = 1500
        self.strength = 200
        self.move_set_index = 0
        self.move_set: list[MOVESET] = [
            MOVESET.ATT, MOVESET.DEF, MOVESET.DEBUFF, MOVESET.ULT
        ]
        self.ult_counter = 0
        self.buff = 1
        self.debuff = 0
        self.attr = attr
        self.attr_index = 0
        self.attr_list = [
            MOVESET.FIRE, MOVESET.WATER, MOVESET.EARTH
        ]
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
        self.image = pg.transform.scale(self.walking_frames['down'][0],(250,250)) 
        # Only the feet should be collided with objects, not whole body
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.feet = pg.Rect(0, 0, self.rect.width * 0.5, 8)
        
    def fight(self, target)->None:
        super().fight(target)
        if self.state== MOVESET.ULT:
            self.ult_counter+=1
            if self.ult_counter >= 4:
                target.health -= 10000
    def change_attr(self):
        self.attr_index = (self.attr_index+1)%len(self.attr_list)
        self.attr = self.attr_list[self.attr_index]
    
    def act(self, player):
        #TODO lam con ai hay cai action list cho may con quai di/ bodd
        self.change_attr()
        self.fight(player)
        if self.state != MOVESET.ULT:
            self.move_set_index +=1
        self.state = self.move_set[self.move_set_index]
        

class Battle(State):
    def __init__(self, game, player):
        super().__init__(game)
        self.font_title = pg.font.SysFont('comicsans',40)
        self.font_status = pg.font.SysFont('comicsans',20)
        self.change_wait_time = 0
        self.change_cool_down = 10
        self.player = player
        self.fool_pos = ((game.SCREEN_WIDTH - 250) /2,150)
        self.fool = Enemy(game, attr[numpy.random.randint(0,100)%3] , self.fool_pos)
        self.player_wait_time:float = 0
        self.player_action_cooldown:float = 60
        self.fool_wait_time:float = 90
        self.fool_action_cooldown:float = 90
        self.bg= pg.image.load(f'{RESOURCES_DIR}/graphics/selectionbox.png').convert()
        self.bg = pg.transform.scale(self.bg,(800, 600))
        self.orb = pg.image.load(f'{RESOURCES_DIR}/graphics/ORB.png')
        self.fighting = True
        

    def update(self, delta_time, actions):
        if (self.fool.alive ==False) or (self.player.live == False):
            self.fighting =False
        self.player_wait_time =self.player_wait_time- delta_time if (self.player_wait_time>0) else 0
        self.change_wait_time =self.change_wait_time- delta_time if (self.change_wait_time>0) else 0
        self.fool_wait_time-=delta_time
        if self.fighting == False:
            self.reward()
            self.exit_state()
        if actions['mouse_click'] is not None:
            if self.player_wait_time<=0 and self.fool.rect.collidepoint(actions['mouse_click']):
                print('hit')
                self.player.fight(self.fool)
                self.player_wait_time = self.player_action_cooldown           
        elif self.change_wait_time<=0:
            self.change_wait_time = self.change_cool_down
            if actions['change']:
                actions['change'] = False
                self.player.change_attr()
            elif actions['act']:
                print('act')
                actions['act'] = False
                self.player.state = MOVESET.ATT
            elif actions['debuff']:
                actions['debuff'] = False
                self.player.state = MOVESET.DEBUFF
            elif actions['def']:
                actions['def'] = False
                self.player.state = MOVESET.DEF 
            elif actions['ult'] and (MOVESET.ULT in self.player.move_set):
                actions['ult'] = False
                self.player.state = MOVESET.ULT
            else:
                self.change_wait_time = 0
        if self.fool_wait_time <= 0 :
            self.fool.act(self.player)
            self.fool_wait_time = self.fool_action_cooldown
            
        if self.fool.health<=0:
            self.fool.alive = False
        if self.player.health<=0:
            self.player.alive = False
        
            
    def get_str(self, str:MOVESET):
        
        match str:
            case MOVESET.ATT:
                return 'Attack'
            case MOVESET.DEF:
                return 'Defend'
            case MOVESET.DEBUFF:
                return 'Debuff'
            case MOVESET.BUFF:
                return 'Buffing'
            case MOVESET.FIRE:
                return 'Fire'
            case MOVESET.WATER:
                return 'Water'
            case MOVESET.EARTH:
                return 'Earth'
            case MOVESET.ULT:
                return 'Killer Move'
            case MOVESET.PURE:
                return 'Pure'
            
    def reward(self):
        if(self.player.live):
            self.player.buff=1
            self.player.debuff=0
            self.player.strength+=5
            self.player.max_health+=20
            self.player.health= self.player.health+40 if(self.player.max_health-self.player.health>=40) else self.player.max_health

    
    def display_enemy(self):
        
        attr_type=self.font_title.render( 'Attribute: ' +self.get_str(self.fool.attr),True, BLACK)
        
        state = self.font_title.render('Action State: '+self.get_str(self.fool.state), True, BLACK)
        
        health_bar = pg.Rect(self.game.SCREEN_WIDTH - 250 , 175 ,200 , 50)
        life_bar = pg.Rect(self.game.SCREEN_WIDTH - 250 , 175 ,round(200 - (self.fool.max_health-self.fool.health)/self.fool.max_health*200), 50)
        
        stamina_bar = pg.Rect(self.game.SCREEN_WIDTH - 250 , 250 ,200  , 50)
        regain_bar = pg.Rect(self.game.SCREEN_WIDTH - 250 , 250 ,round(200* (1-(self.fool_wait_time/self.fool_action_cooldown)) ) , 50)
        
        
        pg.draw.rect(self.game.screen, RED, health_bar)
        pg.draw.rect(self.game.screen, GREEN, life_bar)
        pg.draw.rect(self.game.screen, BLUE, stamina_bar)
        pg.draw.rect(self.game.screen, YELLOW, regain_bar)
        
        self.game.screen.blit(attr_type,(30,50))
        self.game.screen.blit(state,(self.game.SCREEN_WIDTH-state.get_width()-30,50))
        self.game.screen.blit(pg.transform.scale(self.fool.image,(250,250)) ,self.fool_pos)
        
    def display_player(self):
        
        attr_type=self.font_status.render( 'Attribute: ' +self.get_str(self.player.attr),True, BLACK)
        state = self.font_status.render('Action State: '+self.get_str(self.player.state), True, BLACK)

        health_bar = pg.Rect( 300, 450 ,200 , 30)
        life_bar = pg.Rect( 300 , 450 ,round((self.player.health/self.player.max_health)*200), 30)
        
        stamina_bar = pg.Rect(300 , 500 ,200  , 30)
        regain_bar = pg.Rect(300 , 500 ,round(200* (1-(self.player_wait_time/self.player_action_cooldown)) ) , 30)
        
        self.game.screen.blit(attr_type,(50,450))
        self.game.screen.blit(state,(50,500))
        
        ult_orb = self.orb.copy()
        
        if self.player.state != MOVESET.ULT:
            ult_orb.set_alpha(128)
        
        if (MOVESET.ULT in self.player.move_set):
            self.game.screen.blit(pg.transform.scale(ult_orb,(110,110)),(600,425))
        
        pg.draw.rect(self.game.screen, RED, health_bar)
        pg.draw.rect(self.game.screen, GREEN, life_bar)
        pg.draw.rect(self.game.screen, BLUE, stamina_bar)
        pg.draw.rect(self.game.screen, YELLOW, regain_bar)
        
        

    def render(self, surface):
        surface.fill(BLACK)
        self.game.screen.blit(self.bg, (0, 0))
        self.display_enemy()
        self.display_player()
        # self.game.screen.blit(pg.transform.scale(self.player.image,(60,60)) ,self.player_pos)
        

class BossBattle(Battle):
    def __init__(self, game, player):
        super().__init__(game, player)
        self.fool = Boss(game, MOVESET.FIRE , self.fool_pos)
        if MOVESET.ULT not in player.move_set:
            self.player_wait_time:float = 0
            self.player_action_cooldown:float = 80
            self.fool_wait_time:float = 0
            self.fool_action_cooldown:float = 90
    
    def reward(self):
        if(self.player.live):
            self.game.win = True
        else:
            self.game.lose = True
