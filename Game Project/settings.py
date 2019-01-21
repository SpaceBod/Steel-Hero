import pygame as pg
from os import path
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)

# game settings
WIDTH = 1280
HEIGHT = 720
FPS = 64
TITLE = "Tank Royale"

pg.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
game_folder = path.dirname(__file__)
sound_folder = path.join(game_folder, 'sounds')
THEME_SNG = pg.mixer.music.load(path.join(sound_folder, 'theme.mp3'))
SHOOT_SFX = pg.mixer.Sound(path.join(sound_folder, 'explodeSFX.wav'))
CONTACT_SFX = pg.mixer.Sound(path.join(sound_folder, 'blipSFX.wav'))
EXPLODE_SFX = pg.mixer.Sound(path.join(sound_folder, 'collisionSFX.wav'))
EMPTY_SFX = pg.mixer.Sound(path.join(sound_folder, 'emptySFX.wav'))
RELOAD_SFX = pg.mixer.Sound(path.join(sound_folder, 'reloadSFX.wav'))
KILL_SFX = pg.mixer.Sound(path.join(sound_folder, 'killSFX.wav'))
DMG_SFX = pg.mixer.Sound(path.join(sound_folder, 'dmgSFX.wav'))
GAMEOVER_SFX = pg.mixer.Sound(path.join(sound_folder, 'gameOverSFX.wav'))




TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE


# Player settings
PLAYER_HEALTH = 1000
PLAYER_SPEED = 150
PLAYER_ROT_SPEED = 200
PLAYER_IMG = 'tank.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 64, 64)
BARREL_OFFSET = vec(30, 0)

# Gun settings
BULLET_IMG = 'bullet.png'
BULLET_SPEED = 128
BULLET_LIFETIME = 15000
BULLET_RATE = 512
GUN_SPREAD = 0
BULLET_DAMAGE = 20
RELOAD_COOLDOWN = 1000
SHOT_BURST = 5
BULLET_HIT_RECT = pg.Rect(0, 0, 12, 12)


# Mob settings
MOB_IMG = 'enemytank.png'
BULLETENEMY_IMG = 'bulletEnemy.png'
MOB_SPEED = 100
MOB_HIT_RECT = pg.Rect(0, 0, 12, 12)
MOB_HEALTH = 50
MOB_DAMAGE = 30
MOB_KNOCKBACK = 20
BARREL_OFFSET_MOB = vec(30, 0)
AVOID_RADIUS = 64

