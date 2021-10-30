import pygame as pg
import math
from random import uniform, choice, randint, random
from settings import *
from tilemap import *
from random import randint


# shorten the vector sentence
vec = pg.math.Vector2


# collision detection with obstacles / walls
# the parameters are the sprite, which group it will collide with, and its velocity direction
def collide_with_walls(sprite, group, dir):
    # x movement of sprite to collide
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # checks hit boxes of both sprite and obstacle
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            # stops the sprite's movement in x-axis
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    # y movement of sprite to collide
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # checks hit boxes of both sprite and obstacle
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            # stops the sprite's movement in y-axis
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

def enemy_collide_with_walls(sprite, group, dir):
    # x movement of sprite to collide
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            # stops the sprite's movement
            sprite.vel.x = 0
            sprite.vel.y = 10
            sprite.hit_rect.centerx = sprite.pos.x
    # y movement of sprite to collide
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            # stops the sprite's movement
            sprite.vel.y = 0
            sprite.vel.x = 10
            sprite.hit_rect.centery = sprite.pos.y

# collision detection with other sprites
def collide_with_sprite(sprite1, sprite2, dir):
    # x movement of sprite to collide
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite1, sprite2, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite1.hit_rect.centerx:
                sprite1.pos.x = hits[0].rect.left - sprite1.hit_rect.width / 2
            if hits[0].rect.centerx < sprite1.hit_rect.centerx:
                sprite1.pos.x = hits[0].rect.right + sprite1.hit_rect.width / 2
            # stops the sprite's movement
            sprite1.vel.x = 0
            sprite1.hit_rect.centerx = sprite1.pos.x
    # y movement of sprite to collide
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite1, sprite2, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite1.hit_rect.centery:
                sprite1.pos.y = hits[0].rect.top - sprite1.hit_rect.height / 2
            if hits[0].rect.centery < sprite1.hit_rect.centery:
                sprite1.pos.y = hits[0].rect.bottom + sprite1.hit_rect.height / 2
            # stops the sprite's movement
            sprite1.vel.y = 0
            sprite1.hit_rect.centery = sprite1.pos.y


# the tank player class
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # setup all variables and attributes
        self.images = []
        self.images.append(game.player_img)
        self.images.append(game.player_img2)
        self.imageIndex = 0
        self.groups = game.all_sprites, game.players
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.images[self.imageIndex]
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        self.animationDelay = PLAYER_ANIMATION
        self.animationPrevious = 0
        self.moving = False
        self.acceleration = 0
        self.currentSpeed = 0
        self.maxSpeed = PLAYER_SPEED
        self.noKey = True
        self.playerTurret = Turret(game, self.pos.x, self.pos.y, BULLET_RATE)

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        now = pg.time.get_ticks()
        moving = False

        # player movement
        if keys[pg.K_a]:    # right
            self.rot_speed = PLAYER_ROT_SPEED

        if keys[pg.K_d]:    # left
            self.rot_speed = -PLAYER_ROT_SPEED

        if keys[pg.K_w]:    # forwards
            self.acceleration = 4
            self.noKey = False

        if keys[pg.K_s]:    # backwards
            self.acceleration = -2
            self.noKey = False

        if not (keys[pg.K_w] or keys[pg.K_s]):
            self.noKey = True

        self.currentSpeed += self.acceleration

        if self.noKey == True:
            self.acceleration = 0
            self.currentSpeed *= 0.9
        if self.currentSpeed >= self.maxSpeed:
            self.currentSpeed = self.maxSpeed
        if self.currentSpeed <= (-self.maxSpeed)/2:
            self.currentSpeed = (-self.maxSpeed)/2

        if self.currentSpeed > 2 or self.currentSpeed < 2:
            self.moving = True

        if self.noKey == True:
            if self.currentSpeed <= 2 and self.currentSpeed >= -2:
                self.currentSpeed = 0
                self.moving = False

        self.vel = vec(self.currentSpeed, 0).rotate(-self.rot)

    def update(self):

        if self.moving == True:
            timeNow = pg.time.get_ticks()
            if timeNow - self.animationPrevious > self.animationDelay:
                self.animationPrevious = timeNow
                self.image = self.images[self.imageIndex]

                self.imageIndex += 1
                if self.imageIndex >= len(self.images):
                    self.imageIndex = 0
        # gets input
        self.get_keys()
        # works out new rotation from input and rotates the image
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.images[self.imageIndex], self.rot)
        # re-aligns the collision rectangle
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        # updates position by adding the speed multiplied by time
        self.pos += self.vel * self.game.dt

        # positions the tank turret sprite on top of the tank
        self.game.turret.pos = self.pos

        # checks for collisions with walls
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

        # checks for collisions with enemies
        self.hit_rect.centerx = self.pos.x
        collide_with_sprite(self, self.game.enemies, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_sprite(self, self.game.enemies, 'y')
        self.rect.center = self.hit_rect.center

        self.playerTurret.pos = self.pos

        if self.game.player.health == 0:
            self.kill()

# the turret that always follows the player
class Turret(pg.sprite.Sprite):
    def __init__(self, game, x, y, bullet_rate):
        # setup all variables and attributes
        self.groups = game.all_sprites, game.turret
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_turret_img
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.offset = vec(0, 0)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.last_shot = 0
        self.rate = bullet_rate
        self.increment = 0
        self.angle = 0

        now = pg.time.get_ticks()

    def update(self):
        # setup shortcut code
        click = pg.mouse.get_pressed()
        mx, my = pg.mouse.get_pos()
        now = pg.time.get_ticks()
        # calculates rotation angle to mouse position on screen and rotates sprite image
        self.rot = ((mx, my) - (vec(WIDTH/2, HEIGHT/2))).angle_to(vec(0, 0))

        offset_rotated = self.offset.rotate(self.rot)
        self.image = pg.transform.rotate(self.game.player_turret_img, self.rot)
        # re-aligns the sprite image
        self.rect = self.image.get_rect(center=self.pos + offset_rotated)
        self.acc = vec(1, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        # updates the position to the same as the player tank body
        self.pos = self.game.player.pos

        if click[0] == 1:
            # checks if bullet can be shot
            if now - self.last_shot > self.rate:
                self.last_shot = now
                # takes the direction of the turret
                dir = vec(1, 0).rotate(-self.rot)
                # adjusts the position of the projectile to the end of the barrel
                pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                # instantiates the bullet
                Bullet(self.game, pos, dir)
                MuzzleFlash(self.game, pos)
                # plays sound effect for shooting
                pg.mixer.Sound.set_volume(SHOOT_SFX, 0.5)
                pg.mixer.Sound.play(SHOOT_SFX)

        hits = pg.sprite.spritecollide(self.game.player, self.game.shotguns, False)
        for hit in hits:
            self.kill()
        hits2 = pg.sprite.spritecollide(self.game.player, self.game.miniguns, False)
        for hit in hits2:
            self.kill()

        if self.game.player.health == 0:
            self.kill()

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

    def update(self):
        # centers rectangle
        self.rect.center = self.pos
        # updates movement
        self.pos += self.vel * self.game.dt

        if pg.sprite.spritecollideany(self, self.game.walls):
            MuzzleFlash(self.game, self.pos)
            self.kill()

        # kills bullet after certain time
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


class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(20, 50)
        self.image = pg.transform.scale(choice(game.gun_flashes), (size, size))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()

class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # setup all variables and attributes
        self.groups = game.all_sprites, game.enemies
        self.images = []
        self.images.append(game.enemy_img)
        self.images.append(game.enemy_img2)
        self.imageIndex = 0
        self.image = self.images[self.imageIndex]
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = self.image.get_rect()
        self.hit_rect = ENEMY_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.rot = 0
        self.acc = vec(0, 0)
        self.health = ENEMY_HEALTH
        self.currentlyLoading = False
        self.bulletCount = 5
        self.reloadStop = 0
        self.animationDelay = ENEMY_ANIMATION
        self.animationPrevious = 0
        self.moving = False
        self.acceleration = 0
        self.currentSpeed = 0
        self.maxSpeed = ENEMY_SPEED
        self.noKey = True
        self.rot_speed = ENEMY_ROT_SPEED
        self.offset = vec(0, 0)
        self.angleIncrement = 1
        self.turret = Enemy_Turret(game, self.pos.x, self.pos.y)


    def is_close(object1, object2, distance):
        return math.hypot(object2.x - object1.x, object2.y - object1.y) < float(distance)

    def update(self):
        x, y = self.pos
        now = pg.time.get_ticks()
        # calculates rotation angle to mouse position on screen and rotates sprite image
        if not Enemy.is_close(self.game.player.pos, self.pos, TURRET_PROXIMITY):
            angle = ((self.game.player.pos) - (vec(self.pos))).angle_to(self.vel)
            angle = int(angle)

            if angle < 180 and angle > 0:
                right = 2
                self.rot += right
                self.moving = True

            if angle < -180 and angle > -360:
                right = 2
                self.rot += right
                self.moving = True

            if angle < 0 and angle > -180:
                left = -2
                self.rot += left
                self.moving = True

            if angle < 360 and angle > 180:
                left = -2
                self.rot += left
                self.moving = True

            self.currentSpeed = -120
        else:
            self.currentSpeed = 0
            self.moving = False

        if self.moving == True:
            timeNow = pg.time.get_ticks()
            if timeNow - self.animationPrevious > self.animationDelay:
                self.animationPrevious = timeNow
                self.image = self.images[self.imageIndex]
                self.imageIndex += 1
                if self.imageIndex >= len(self.images):
                    self.imageIndex = 0

        offset_rotated = self.offset.rotate(self.rot)
        self.image = pg.transform.rotate(self.images[self.imageIndex], self.rot)
        self.rect = self.image.get_rect(center=self.pos + offset_rotated)
        self.acc = vec(1, 0).rotate(-self.rot)
        self.acc += self.vel * -1

        self.vel = vec(self.currentSpeed, 0).rotate(-self.rot)
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2

        self.hit_rect.centerx = self.pos.x
        enemy_collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        enemy_collide_with_walls(self, self.game.walls, 'y')

        for self.game.enemy in self.game.enemies:
            self.draw_health()

        self.rect.center = self.hit_rect.center
        self.turret.pos = self.pos



    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / ENEMY_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < ENEMY_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)



class Enemy_Turret(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # setup all variables and attributes
        self.groups = game.all_sprites, game.enemy_turrets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.enemy_turret_img
        self.rect = self.image.get_rect()
        self.pos = vec(x,y)
        self.offset = vec(0, 0)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.last_shot = 0
        self.moving = False
        self.acceleration = 0
        self.currentSpeed = 0
        self.maxSpeed = ENEMY_SPEED
        self.noKey = True
        self.rot_speed = ENEMY_ROT_SPEED
        self.angleIncrement = 1

        now = pg.time.get_ticks()

    def update(self):
        # setup shortcut code
        #self.pos = self.game.enemy.pos
        x, y = self.pos
        now = pg.time.get_ticks()

        # calculates rotation angle to mouse position on screen and rotates sprite image
        self.rot = ((x, y) - (vec(self.game.player.pos.x, self.game.player.pos.y))).angle_to(vec(1, 0))
        offset_rotated = self.offset.rotate(self.rot)
        self.image = pg.transform.rotate(self.game.enemy_turret_img, self.rot)
        self.rect = self.image.get_rect(center=self.pos + offset_rotated)
        self.acc = vec(1, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt

        if Enemy.is_close(self.game.player.pos, self.pos, SHOOT_PROXIMITY):
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot+180)
                pos = self.pos + BARREL_OFFSET.rotate(-self.rot+180)
                BulletEnemy(self.game, pos, dir)
                MuzzleFlash(self.game, pos)
                pg.mixer.Sound.set_volume(SHOOT_SFX, 0.5)
                pg.mixer.Sound.play(SHOOT_SFX)


class BulletEnemy(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.enemy_bullets
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

    def update(self):

        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        # wall collision
        if pg.sprite.spritecollideany(self, self.game.walls):
            MuzzleFlash(self.game, self.pos)
            self.kill()
        # bullet collides with player
        hits = pg.sprite.spritecollide(self.game.player, self.game.enemy_bullets, False, collide_hit_rect)

        for hit in hits:
            self.game.player.health -= BULLET_DAMAGE
            pg.mixer.Sound.set_volume(DMG_SFX, 0.1)
            pg.mixer.Sound.play(DMG_SFX)
            MuzzleFlash(self.game, self.pos)
            self.kill()
            # kill player if health 0

        # kills bullet in time
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()

class HealthPack(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.healthpacks
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.healthPack_img
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.pos = vec(self.pos)
        self.hit_rect = HEALTHPACK_RECT
        self.hit_rect.center = self.rect.center
        self.rect.center = self.pos

    def update(self):

        self.rect.center = self.pos
        # bullet hits enemy detection
        hits = pg.sprite.spritecollide(self.game.player, self.game.healthpacks, False)
        for hit in hits:
            if self.game.player.health + 250 >= PLAYER_HEALTH:
                self.game.player.health = PLAYER_HEALTH
            else:
                self.game.player.health += 250
            pg.mixer.Sound.play(HEALTH_SFX)
            hit.kill()

class Boss(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # setup all variables and attributes
        self.groups = game.all_sprites, game.enemies
        self.images = []
        self.images.append(game.boss_img)
        self.images.append(game.boss_img2)
        self.imageIndex = 0
        self.image = self.images[self.imageIndex]
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = self.image.get_rect()
        self.hit_rect = ENEMY_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.rot = 0
        self.acc = vec(0, 0)
        self.health = BOSS_HEALTH
        self.currentlyLoading = False
        self.bulletCount = 5
        self.reloadStop = 0
        self.animationDelay = ENEMY_ANIMATION
        self.animationPrevious = 0
        self.moving = False
        self.acceleration = 0
        self.currentSpeed = 0
        self.maxSpeed = BOSS_SPEED
        self.noKey = True
        self.rot_speed = ENEMY_ROT_SPEED
        self.offset = vec(0, 0)
        self.angleIncrement = 1
        self.turret = Boss_Turret(game, self.pos.x, self.pos.y)


    def is_close(object1, object2, distance):
        return math.hypot(object2.x - object1.x, object2.y - object1.y) < float(distance)

    def update(self):
        x, y = self.pos
        now = pg.time.get_ticks()
        # calculates rotation angle to mouse position on screen and rotates sprite image
        if not Enemy.is_close(self.game.player.pos, self.pos, TURRET_PROXIMITY):
            angle = ((self.game.player.pos) - (vec(self.pos))).angle_to(self.vel)
            angle = int(angle)

            if angle < 180 and angle > 0:
                right = 2
                self.rot += right
                self.moving = True

            if angle < -180 and angle > -360:
                right = 2
                self.rot += right
                self.moving = True

            if angle < 0 and angle > -180:
                left = -2
                self.rot += left
                self.moving = True

            if angle < 360 and angle > 180:
                left = -2
                self.rot += left
                self.moving = True

            self.currentSpeed = -120
        else:
            self.currentSpeed = 0
            self.moving = False

        if self.moving == True:
            timeNow = pg.time.get_ticks()
            if timeNow - self.animationPrevious > self.animationDelay:
                self.animationPrevious = timeNow
                self.image = self.images[self.imageIndex]
                self.imageIndex += 1
                if self.imageIndex >= len(self.images):
                    self.imageIndex = 0

        offset_rotated = self.offset.rotate(self.rot)
        self.image = pg.transform.rotate(self.images[self.imageIndex], self.rot)
        self.rect = self.image.get_rect(center=self.pos + offset_rotated)
        self.acc = vec(1, 0).rotate(-self.rot)
        self.acc += self.vel * -1

        self.vel = vec(self.currentSpeed, 0).rotate(-self.rot)
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2

        self.hit_rect.centerx = self.pos.x
        enemy_collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        enemy_collide_with_walls(self, self.game.walls, 'y')

        self.draw_health()

        self.rect.center = self.hit_rect.center
        self.turret.pos = self.pos



    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / BOSS_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < BOSS_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)



class Boss_Turret(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # setup all variables and attributes
        self.groups = game.all_sprites, game.enemy_turrets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.boss_turret_img
        self.rect = self.image.get_rect()
        self.pos = vec(x,y)
        self.offset = vec(0, 0)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.last_shot = 0
        self.moving = False
        self.acceleration = 0
        self.currentSpeed = 0
        self.maxSpeed = ENEMY_SPEED
        self.noKey = True
        self.rot_speed = ENEMY_ROT_SPEED
        self.angleIncrement = 1

        now = pg.time.get_ticks()

    def update(self):
        # setup shortcut code
        #self.pos = self.game.enemy.pos
        x, y = self.pos
        now = pg.time.get_ticks()

        # calculates rotation angle to mouse position on screen and rotates sprite image
        self.rot = ((x, y) - (vec(self.game.player.pos.x, self.game.player.pos.y))).angle_to(vec(1, 0))
        offset_rotated = self.offset.rotate(self.rot)
        self.image = pg.transform.rotate(self.game.boss_turret_img, self.rot)
        self.rect = self.image.get_rect(center=self.pos + offset_rotated)
        self.acc = vec(1, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt

        if Enemy.is_close(self.game.player.pos, self.pos, SHOOT_PROXIMITY):
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot+180)
                pos = self.pos + BARREL_OFFSET.rotate(-self.rot+180)
                BulletEnemy(self.game, pos, dir)
                BulletEnemy(self.game, pos, dir)
                BulletEnemy(self.game, pos, dir)
                MuzzleFlash(self.game, pos)
                pg.mixer.Sound.set_volume(SHOOT_SFX, 0.5)
                pg.mixer.Sound.play(SHOOT_SFX)

# the turret upgrade that always follows the player
class TurretUpgrade(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # setup all variables and attributes
        self.groups = game.all_sprites, game.turret_upgrade
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_turret_upgrade_img
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.offset = vec(0, 0)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.last_shot = 0

        now = pg.time.get_ticks()

    def update(self):
        # setup shortcut code
        self.pos = self.game.player.pos
        click = pg.mouse.get_pressed()
        mx, my = pg.mouse.get_pos()
        now = pg.time.get_ticks()
        # calculates rotation angle to mouse position on screen and rotates sprite image
        self.rot = ((mx, my) - (vec(WIDTH/2, HEIGHT/2))).angle_to(vec(1, 0))
        offset_rotated = self.offset.rotate(self.rot)
        self.image = pg.transform.rotate(self.game.player_turret_upgrade_img, self.rot)
        # re-aligns the sprite image
        self.rect = self.image.get_rect(center=self.pos + offset_rotated)
        self.acc = vec(1, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        if self.game.wave == self.game.despawnWave:
            self.kill()
            self.game.spawnTurret = True



        if click[0] == 1:
            if now - self.last_shot > BULLET_RATE * 1.5:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                Bullet(self.game, pos, dir)
                Bullet(self.game, pos, dir)
                Bullet(self.game, pos, dir)
                Bullet(self.game, pos, dir)
                Bullet(self.game, pos, dir)
                MuzzleFlash(self.game, pos)
                pg.mixer.Sound.set_volume(SHOOT_SFX, 0.5)
                pg.mixer.Sound.play(SHOOT_SFX)

        hits = pg.sprite.spritecollide(self.game.player, self.game.shotguns, False)
        for hit in hits:
            self.kill()
        hits2 = pg.sprite.spritecollide(self.game.player, self.game.miniguns, False)
        for hit in hits2:
            self.kill()
        if self.game.player.health == 0:
            self.kill()



class Shotgun(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.shotguns
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.shotgun_img
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.pos = vec(self.pos)
        self.hit_rect = SHOTGUN_RECT
        self.hit_rect.center = self.rect.center
        self.rect.center = self.pos

    def update(self):

        self.rect.center = self.pos


class Minigun(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.miniguns
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.minigun_img
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.pos = vec(self.pos)
        self.hit_rect = SHOTGUN_RECT
        self.hit_rect.center = self.rect.center
        self.rect.center = self.pos

    def update(self):

        self.rect.center = self.pos

# the turret upgrade that always follows the player
class TurretUpgrade2(pg.sprite.Sprite):
    def __init__(self, game, x, y, bullet_rate):
        # setup all variables and attributes
        self.groups = game.all_sprites, game.turret_upgrade_2
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_turret_upgrade_2_img
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.offset = vec(0, 0)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.last_shot = 0
        self.rate = bullet_rate
        now = pg.time.get_ticks()

    def update(self):
        # setup shortcut code
        self.pos = self.game.player.pos
        click = pg.mouse.get_pressed()
        mx, my = pg.mouse.get_pos()
        now = pg.time.get_ticks()
        # calculates rotation angle to mouse position on screen and rotates sprite image
        self.rot = ((mx, my) - (vec(WIDTH/2, HEIGHT/2))).angle_to(vec(0, 0))
        offset_rotated = self.offset.rotate(self.rot)
        self.image = pg.transform.rotate(self.game.player_turret_upgrade_2_img, self.rot)
        # re-aligns the sprite image
        self.rect = self.image.get_rect(center=self.pos + offset_rotated)
        self.acc = vec(1, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        if self.game.wave == self.game.despawnWave:
            self.kill()
            self.game.spawnTurret = True



        if click[0] == 1:
            if now - self.last_shot > self.rate:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + BARREL_OFFSET.rotate(-self.rot)

                import settings
                settings.BULLET_RATE = settings.BULLET_RATE/2
                Bullet(self.game, pos, dir)
                MuzzleFlash(self.game, pos)
                pg.mixer.Sound.set_volume(SHOOT_SFX, 0.5)
                pg.mixer.Sound.play(SHOOT_SFX)

        hits = pg.sprite.spritecollide(self.game.player, self.game.shotguns, False)
        for hit in hits:
            self.kill()
        hits2 = pg.sprite.spritecollide(self.game.player, self.game.miniguns, False)
        for hit in hits2:
            self.kill()
        if self.game.player.health == 0:
            self.kill()
