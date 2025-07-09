import random
import math
from pygame import Rect
from pgzero.actor import Actor
import pgzrun

TITLE = "Roguelike"
WIDTH = 640
HEIGHT = 480
CELL_SIZE = 64

# === ESTADO DO JOGO ===
game_started = False
sound_on = True

# === HERÓI ===
class Hero:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.x = x * CELL_SIZE
        self.y = y * CELL_SIZE
        self.image_idle = ["player"]
        self.image_walk = ["player", "player"]
        self.frame = 0
        self.sprite = Actor(self.image_idle[0], (self.x, self.y))
        self.speed = 4
        self.moving = False
        self.move_target = (self.x, self.y)

    def draw(self):
        self.sprite.draw()

    def update(self):
        if self.moving:
            dx = self.move_target[0] - self.x
            dy = self.move_target[1] - self.y
            dist = math.hypot(dx, dy)
            if dist < self.speed:
                self.x, self.y = self.move_target
                self.moving = False
            else:
                self.x += self.speed * dx / dist
                self.y += self.speed * dy / dist
        self.sprite.pos = (self.x, self.y)
        self.frame = (self.frame + 1) % len(self.image_walk)
        self.sprite.image = self.image_walk[self.frame] if self.moving else self.image_idle[0]

    def move(self, dx, dy):
        if self.moving:
            return
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy
        if 0 <= new_x < 10 and 0 <= new_y < 8:
            self.grid_x = new_x
            self.grid_y = new_y
            self.move_target = (new_x * CELL_SIZE, new_y * CELL_SIZE)
            self.moving = True
        
# === Enemy ===
class Enemy:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.x = x * CELL_SIZE
        self.y = y * CELL_SIZE
        self.image_idle = ["enemy"]
        self.image_walk = ["enemy", "enemy"]
        self.sprite = Actor(self.image_idle[0], (self.x, self.y))
        self.frame = 0
        self.move_target = (self.x, self.y)
        self.speed = 2
        self.moving = False
        self.timer = 0

    def draw(self):
        self.sprite.draw()

    def update(self):
        if not self.moving and self.timer <= 0:
            dx = hero.grid_x - self.grid_x
            dy = hero.grid_y - self.grid_y
            distance = abs(dx) + abs(dy)

            if distance <= 4:
                step_x = 0
                step_y = 0
                if abs(dx) > abs(dy):
                    step_x = 1 if dx > 0 else -1
                elif dy != 0:
                    step_y = 1 if dy > 0 else -1
                self.try_move(step_x, step_y)
            else:
                dir_x, dir_y = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
                self.try_move(dir_x, dir_y)

            self.timer = 30
        else:
            self.timer -= 1

        if self.moving:
            dx = self.move_target[0] - self.x
            dy = self.move_target[1] - self.y
            dist = math.hypot(dx, dy)
            if dist < self.speed:
                self.x, self.y = self.move_target
                self.moving = False
            else:
                self.x += self.speed * dx / dist
                self.y += self.speed * dy / dist

        self.sprite.pos = (self.x, self.y)
        self.frame = (self.frame + 1) % len(self.image_walk)
        self.sprite.image = self.image_walk[self.frame] if self.moving else self.image_idle[0]

    def try_move(self, dx, dy):
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy

        if not (0 <= new_x < 10 and 0 <= new_y < 8):
            return

        for other in enemies:
            if other is not self and other.grid_x == new_x and other.grid_y == new_y:
                return 

        self.grid_x = new_x
        self.grid_y = new_y
        self.move_target = (new_x * CELL_SIZE, new_y * CELL_SIZE)
        self.moving = True

# === MENU ===
buttons = [
    {"label": "Start Game", "x": 250, "y": 150, "w": 140, "h": 40, "action": "start"},
    {"label": "Toggle Sound", "x": 250, "y": 200, "w": 140, "h": 40, "action": "sound"},
    {"label": "Quit", "x": 250, "y": 250, "w": 140, "h": 40, "action": "quit"},
]

hero = Hero(2, 2)
enemies = [Enemy(5, 3), Enemy(7, 5)]

def draw():
    screen.clear() # type: ignore
    if not game_started:
        draw_menu()
    else:
        screen.fill((180, 160, 255)) # type: ignore
        hero.draw()
        for e in enemies:
            e.draw()

def draw_menu():
    screen.fill((20, 20, 60)) # type: ignore
    for b in buttons:
        screen.draw.filled_rect(Rect((b["x"], b["y"]), (b["w"], b["h"])), (200, 200, 255)) # type: ignore
        screen.draw.text(b["label"], center=(b["x"]+b["w"]/2, b["y"]+20), color="black") # type: ignore

def on_mouse_down(pos):
    global game_started, sound_on
    if not game_started:
        for b in buttons:
            rect = Rect((b["x"], b["y"]), (b["w"], b["h"]))
            if rect.collidepoint(pos):
                if b["action"] == "start":
                    game_started = True
                    if sound_on:
                        music.play("music") # type: ignore
                elif b["action"] == "sound":
                    sound_on = not sound_on
                    if not sound_on:
                        music.stop() # type: ignore
                elif b["action"] == "quit":
                    exit()

def update():
    if game_started:
        hero.update()
        for e in enemies:
            e.update()

def on_key_down(key):
    if not game_started:
        return
    if key.name == "UP" or key.name == "W":
        hero.move(0, -1)
    elif key.name == "DOWN" or key.name == "S":
        hero.move(0, 1)
    elif key.name == "LEFT" or key.name == "A":
        hero.move(-1, 0)
    elif key.name == "RIGHT" or key.name == "D":
        hero.move(1, 0)

pgzrun.go()
