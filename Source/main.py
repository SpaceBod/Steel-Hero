
import pygame as pg
import sys
from os import path
from settings import *
from tilemap import *
from sprites import *
import time
import os


class Game:

    def __init__(self):
        # setup the screen size and game time
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.DOUBLEBUF | pg.FULLSCREEN)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.currentWave = 0
        self.despawnWave = 0
        self.spawnTurret = False
        self.name = ""


    def load_data(self):
        # file directories for images and map
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'maps')
        font_folder = path.join(game_folder, 'font')

        self.map = TiledMap(path.join(map_folder, 'level1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen2 = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.dim_screen.fill((0, 0, 0, 230))

        # create image shortcuts
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.player_img2 = pg.image.load(path.join(img_folder, PLAYER_IMG2)).convert_alpha()
        self.healthPack_img = pg.image.load(path.join(img_folder, HEALTHPACK)).convert_alpha()
        self.shotgun_img = pg.image.load(path.join(img_folder, SHOTGUN)).convert_alpha()
        self.minigun_img = pg.image.load(path.join(img_folder, MINIGUN)).convert_alpha()
        self.player_turret_img = pg.image.load(path.join(img_folder, PLAYER_TURRET_IMG)).convert_alpha()
        self.player_turret_upgrade_img = pg.image.load(path.join(img_folder, TURRET_UPGRADE_IMG)).convert_alpha()
        self.player_turret_upgrade_2_img = pg.image.load(path.join(img_folder, TURRET_UPGRADE_2_IMG)).convert_alpha()
        self.enemy_img = pg.image.load(path.join(img_folder, ENEMY_IMG)).convert_alpha()
        self.enemy_img2 = pg.image.load(path.join(img_folder, ENEMY_IMG2)).convert_alpha()
        self.enemy_turret_img = pg.image.load(path.join(img_folder, ENEMY_TURRET_IMG)).convert_alpha()
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.hud_font = path.join(font_folder, 'HUDfont.ttf')
        self.gameover_font = path.join(font_folder, 'defused.ttf')
        self.pause_font = path.join(font_folder, 'THORN.ttf')
        self.HUD = pg.image.load(path.join(img_folder, HUD_IMG)).convert_alpha()
        self.gun_flashes = []

        self.boss_img = pg.image.load(path.join(img_folder, BOSS_IMG)).convert_alpha()
        self.boss_img2 = pg.image.load(path.join(img_folder, BOSS_IMG2)).convert_alpha()
        self.boss_turret_img = pg.image.load(path.join(img_folder, BOSS_TURRET_IMG)).convert_alpha()
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())

    def draw_text(self, text, font_name, size, color, x, y, align="topleft"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.screen.blit(text_surface, text_rect)

    def new(self):
        # initialise all variables and do all the setup for a new game

        self.players = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.turret = pg.sprite.Group()
        self.turret_upgrade = pg.sprite.Group()
        self.turret_upgrade_2 = pg.sprite.Group()
        self.enemy_turrets = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.enemy_bullets = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.healthpacks = pg.sprite.Group()
        self.shotguns = pg.sprite.Group()
        self.miniguns = pg.sprite.Group()

        self.paused = False
        self.gameover = False
        self.playGameOver = False

        # spawns the player at the centre with its turret
        self.player = Player(self, 40, 32)
        self.camera = Camera(self.map.width, self.map.height)
        # creates wall obstacles from xy positions from tmx file
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)

        # wave info
        self.wave = 0

        THEME_SNG
        pg.mixer.music.play(-1, 0.5)

    def run(self):
        # main game update loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            if not self.gameover:
                if not self.paused:
                    self.update()
            else:
                if self.playGameOver == False:
                    pg.mixer.Sound.play(GAMEOVER_SFX)
                    self.playGameOver = True
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):

        # update sprites and camera
        self.all_sprites.update()
        self.camera.update(self.player)

        # bullet hits enemy detection
        hits = pg.sprite.groupcollide(self.enemies, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0, 0)
            pg.mixer.Sound.set_volume(DMG_SFX, 0.2)
            pg.mixer.Sound.play(DMG_SFX)
            MuzzleFlash(self, hit.pos)

            # kill enemy if health 0
            if hit.health <= 0:
                hit.kill()
                hit.turret.kill()
                pg.mixer.Sound.play(EXPLODE_SFX)

        hits = pg.sprite.spritecollide(self.player, self.shotguns, False)
        for hit in hits:
            pg.mixer.Sound.play(HEALTH_SFX)
            hit.kill()
            self.turretUpgrade = TurretUpgrade(self, 40, 32)
            self.currentWave = self.wave
            self.despawnWave = self.wave + 1

        hits2 = pg.sprite.spritecollide(self.player, self.miniguns, False)
        for hit in hits2:
            pg.mixer.Sound.play(HEALTH_SFX)
            hit.kill()

            self.turretUpgrade2 = TurretUpgrade2(self, 40, 32, BULLET_RATE/2)
            self.currentWave = self.wave
            self.despawnWave = self.wave + 1

        # spawns enemy
        if len(self.enemies) == 0:
            self.wave += 1
            pg.mixer.Sound.play(NEW_WAVE_SFX)
            self.waveMod = self.wave % 5
            self.shotgun = Shotgun(self, randint(12, 77), randint(7, 42))
            self.minigun = Minigun(self, randint(12, 77), randint(7, 42))
            if self.wave > 1 and len(self.turret)!= 1:
                import sprites
                self.playerTurret = Turret(self, self.player.pos.x, self.player.pos.y, BULLET_RATE)
            self.waveShotgun = self.wave
            if self.waveMod == 0:
                self.numberBoss = int(self.wave/5)
                for n in range(0, self.numberBoss):
                    self.enemy = Boss(self, randint(12, 77), randint(7, 42))

            else:
                for n in range(0, self.wave):
                    self.enemy = Enemy(self, randint(12, 77), randint(7, 42))
            if len(self.healthpacks) == 0:
                self.healthpack = HealthPack(self, randint(12, 77), randint(7, 42))
                self.healthpack = HealthPack(self, randint(12, 77), randint(7, 42))
                self.healthpack = HealthPack(self, randint(12, 77), randint(7, 42))
            if len(self.healthpacks) == 1:
                self.healthpack = HealthPack(self, randint(12,77), randint(7,42))
                self.healthpack = HealthPack(self, randint(12, 77), randint(7, 42))
            if len(self.healthpacks) == 2:
                self.healthpack = HealthPack(self, randint(12,77), randint(7,42))

        if self.player.health <= 0:
            self.gameover = True


    def draw(self):
        # draws the map background and positions the camera to be the correct size and position
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        self.screen.blit(self.HUD, (0, 0))
        draw_player_health(self.screen, WIDTH / 2 - 710, HEIGHT - 50, self.player.health / PLAYER_HEALTH)
        self.draw_text('HEALTH', self.hud_font, 30, BLACK, 145, HEIGHT - 48, align="topleft")
        self.draw_text('                                                                                                                ENEMIES: {}       WAVE: {}'.format(len(self.enemies), self.wave), self.hud_font, 30, WHITE, 145, HEIGHT - 48, align="topleft")
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text('Paused', self.pause_font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")
            self.draw_text('Press ESC to return to menu', self.pause_font, 72, RED, WIDTH / 2, HEIGHT / 2 +100, align="center")

        if self.gameover:
            self.screen.blit(self.dim_screen2, (0, 0))
            self.draw_text('GAME OVER', self.gameover_font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")
            self.draw_text('WAVES SURVIVED: {}'.format(self.wave-1), self.pause_font, 36, RED, WIDTH / 2, HEIGHT / 1.6, align="center")
            self.draw_text('PRESS ENTER TO CONTINUE', self.pause_font, 56, RED, WIDTH / 2, HEIGHT / 1.2, align="center")
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        import highscore
                        highscore.run(self.wave-1)




        pg.display.flip()




    def events(self):
        # all input events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE and self.paused:
                    import menu
                    menu.menu()
                if event.key == pg.K_p:
                    self.paused = not self.paused

# HUD FUNCTIONS
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 400
    BAR_HEIGHT = 40
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, BLACK, outline_rect, 2)

