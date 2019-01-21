import pygame as pg
import math
from random import uniform
from settings import *
from tilemap import collide_hit_rect
from random import randint

vec = pg.math.Vector2

xList = []  #wall X pos array
yList =[]   #wall Y pos array



#sounds

pg.mixer.Sound.set_volume(CONTACT_SFX, 0.2)
pg.mixer.Sound.set_volume(EMPTY_SFX, 0.5)
pg.mixer.Sound.set_volume(RELOAD_SFX, 0.5)
pg.mixer.Sound.set_volume(KILL_SFX, 0.3)



def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

def collide_with_sprite(sprite1, sprite2, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite1, sprite2, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite1.hit_rect.centerx:
                sprite1.pos.x = hits[0].rect.left - sprite1.hit_rect.width / 2
            if hits[0].rect.centerx < sprite1.hit_rect.centerx:
                sprite1.pos.x = hits[0].rect.right + sprite1.hit_rect.width / 2
            sprite1.vel.x = 0
            sprite1.hit_rect.centerx = sprite1.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite1, sprite2, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite1.hit_rect.centery:
                sprite1.pos.y = hits[0].rect.top - sprite1.hit_rect.height / 2
            if hits[0].rect.centery < sprite1.hit_rect.centery:
                sprite1.pos.y = hits[0].rect.bottom + sprite1.hit_rect.height / 2
            sprite1.vel.y = 0
            sprite1.hit_rect.centery = sprite1.pos.y





class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        self.currentlyLoading = False
        self.bulletCount = 5

        self.reloadStop = 0


    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        now = pg.time.get_ticks()


        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)
        if keys[pg.K_SPACE]:
            if self.bulletCount > 0:
                if now - self.last_shot > BULLET_RATE:
                    self.bulletCount -= 1
                    self.last_shot = now
                    dir = vec(1, 0).rotate(-self.rot)
                    pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                    Bullet(self.game, pos, dir)
                    pg.mixer.Sound.play(SHOOT_SFX)


        if self.bulletCount == 0:
            if now - self.last_shot > BULLET_RATE:
                while self.currentlyLoading == False:
                    self.currentlyLoading = True
                    self.reloadStop = now + RELOAD_COOLDOWN
                    pg.mixer.Sound.play(EMPTY_SFX)
                    break
                if not pg.mixer.get_busy():
                    pg.mixer.Sound.play(RELOAD_SFX)
                if now >= self.reloadStop and self.currentlyLoading == True:
                    self.bulletCount = SHOT_BURST
                    self.currentlyLoading = False


    def returnBullet(self):
        return self.bulletCount












    def update(self):
        self.get_keys()
        self.returnBullet()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

        collide_with_sprite(self, self.game.mobs, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_sprite(self, self.game.mobs, 'y')
        self.rect.center = self.hit_rect.center


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH
        now = pg.time.get_ticks()
        self.last_shot = 0


    def is_close(object1, object2, distance):
        return math.hypot(object2.x - object1.x, object2.y - object1.y) < float(distance)

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        now = pg.time.get_ticks()
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        # self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(MOB_SPEED, 0).rotate(-self.rot)
        self.avoid_mobs()
        self.acc += self.vel * -1

        if not Mob.is_close(self.pos, self.game.player.pos, 300):
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center


        if self.health <= 0:
            self.kill()
            pg.mixer.Sound.play(KILL_SFX)
        if Mob.is_close(self.pos, self.game.player.pos, 400):
            dir = vec(1, 0).rotate(-self.rot)
            pos = self.pos + BARREL_OFFSET_MOB.rotate(-self.rot)

            if now - self.last_shot > 2000:
                self.last_shot = now
                BulletEnemy(self.game, pos, dir)
                pg.mixer.Sound.set_volume(SHOOT_SFX, 0.2)
                pg.mixer.Sound.play(SHOOT_SFX)






    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.hit_rect = BULLET_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.rect.center = pos
        spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir.rotate(spread) * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()
        self.collisionX = False
        self.collisionY = False





    def update(self):
        self.rect.center = self.pos


        if not pg.sprite.spritecollideany(self, self.game.walls):
            self.collisionX = False
            self.collisionY = False

        self.pos.x += self.vel.x * self.game.dt

        if pg.sprite.spritecollideany(self, self.game.walls) and self.collisionX == False:
            if (round(self.pos.x, 0)) in xList: #checks if X pos collision is an X pos wall
                self.vel.x *= -1
                self.collisionX = True
                self.pos += self.vel * self.game.dt
        self.pos.y += self.vel.y * self.game.dt
        if pg.sprite.spritecollideany(self, self.game.walls) and self.collisionY == False and self.collisionX == False:
            if (round(self.pos.y, 0)) in yList: #checks if Y pos collision is an Y pos wall
                self.vel.y *= -1
                self.collisionY = True
                self.pos += self.vel * self.game.dt








        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()



class BulletEnemy(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bulletsEnemy
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bulletEnemy_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos)

        self.rect.center = pos
        spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir.rotate(spread) * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()
        self.collision = False


    def update(self):
        self.rect.center = self.pos

        if not pg.sprite.spritecollideany(self, self.game.walls):
            self.collision = False

        self.pos.x += self.vel.x * self.game.dt

        if pg.sprite.spritecollideany(self, self.game.walls) and self.collision == False:

            if (round(self.pos.x, 0)) in xList:  # checks if X pos collision is an X pos wall
                self.vel.x *= -1
                self.collision = True
                self.pos += self.vel * self.game.dt
        self.pos.y += self.vel.y * self.game.dt
        if pg.sprite.spritecollideany(self, self.game.walls) and self.collision == False:
            if (round(self.pos.y, 0)) in yList:  # checks if Y pos collision is an Y pos wall
                self.vel.y *= -1
                self.collision = True
                self.pos += self.vel * self.game.dt


        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()




class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        for n in range(-1,1):
            xList.append(int(round(x + n, 0)))  #append leftwall + adjust
            xList.append(int(round(x + w + n , 0)))  #append rightwall + adjust
            yList.append(int(round(y + n, 0)))  #append topwall
            yList.append(int(round(y + h + n, 0)))  #append bottomWall + adjust








