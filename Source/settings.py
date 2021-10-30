import pygame as pg
from os import path

vec = pg.math.Vector2

#colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)

SPLASH_IMG = 'splash.png'
MENU_IMG = 'menu.png'
HELP_IMG = 'help.png'
LEADERBOARD_IMG = 'leaderboard.png'
HIGHSCORE_IMG = 'highscore.png'
HUD_IMG = 'HUD.png'
# Player settings
PLAYER_HEALTH = 750
PLAYER_SPEED = 256
PLAYER_ROT_SPEED = 100
PLAYER_IMG = 'tank.png'
PLAYER_IMG2 = 'tank1.png'
PLAYER_TURRET_IMG = 'turret.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 64, 64)
BARREL_OFFSET = vec(45, 0)
PLAYER_ANIMATION = 128
HEALTHPACK = 'healthPack.png'
SHOTGUN = 'shotgun.png'
MINIGUN = 'minigun.png'
HEALTHPACK_RECT = pg.Rect(0, 0, 16, 16)
TURRET_UPGRADE_IMG = 'player_turret_upgrade.png'
TURRET_UPGRADE_2_IMG = 'player_turret_upgrade_2.png'
SHOTGUN_RECT = pg.Rect(0, 0, 16, 16)
MINIGUN_RECT = pg.Rect(0, 0, 16, 16)

CROSSHAIR_IMG = 'crosshair.png'
CROSSHAIR_HIT_RECT = pg.Rect(0, 0, 32, 32)

# Enemy settings
ENEMY_HEALTH = 100
ENEMY_SPEED = 128
ENEMY_ROT_SPEED = 100
ENEMY_IMG = 'enemy.png'
ENEMY_IMG2 = 'enemy1.png'
ENEMY_TURRET_IMG = 'enemy_turret.png'
ENEMY_HIT_RECT = pg.Rect(0, 0, 64, 64)
ENEMY_ANIMATION = 128
ENEMY_KNOCKBACK = 20
AVOID_RADIUS = 64
TURRET_PROXIMITY = 384
SHOOT_PROXIMITY = 400

BOSS_HEALTH = 1000
BOSS_SPEED = 156
BOSS_IMG = 'boss.png'
BOSS_IMG2 = 'boss1.png'
BOSS_TURRET_IMG = 'boss_turret.png'







# Gun settings
BULLET_IMG = 'bullet.png'
BULLET_SPEED = 1028
BULLET_LIFETIME = 15000
BULLET_RATE = 512
GUN_SPREAD = 5
BULLET_DAMAGE = 20
RELOAD_COOLDOWN = 1000
SHOT_BURST = 2
BULLET_HIT_RECT = pg.Rect(0, 0, 12, 12)

pg.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
game_folder = path.dirname(__file__)
sound_folder = path.join(game_folder, 'sounds')
THEME_SNG = pg.mixer.music.load(path.join(sound_folder, 'theme.mp3'))
SHOOT_SFX = pg.mixer.Sound(path.join(sound_folder, 'Fire.wav'))
NEW_WAVE_SFX = pg.mixer.Sound(path.join(sound_folder, 'waveSFX.wav'))
CONTACT_SFX = pg.mixer.Sound(path.join(sound_folder, 'blipSFX.wav'))
EXPLODE_SFX = pg.mixer.Sound(path.join(sound_folder, 'explodeSFX.wav'))
EMPTY_SFX = pg.mixer.Sound(path.join(sound_folder, 'emptySFX.wav'))
RELOAD_SFX = pg.mixer.Sound(path.join(sound_folder, 'reloadSFX.wav'))
KILL_SFX = pg.mixer.Sound(path.join(sound_folder, 'killSFX.wav'))
DMG_SFX = pg.mixer.Sound(path.join(sound_folder, 'collisionSFX.wav'))
GAMEOVER_SFX = pg.mixer.Sound(path.join(sound_folder, 'gameOverSFX.wav'))
HEALTH_SFX = pg.mixer.Sound(path.join(sound_folder, 'healthSFX.wav'))
SPLASH_SFX = pg.mixer.Sound(path.join(sound_folder, 'sound.wav'))
CLICK_SFX = pg.mixer.Sound(path.join(sound_folder, 'click.wav'))


# game settings
WIDTH = 1440
HEIGHT = 810
FPS = 60
TITLE = "Tank Royale"


TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE


MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png', 'whitePuff17.png',
                  'whitePuff18.png']
FLASH_DURATION = 50
# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1
