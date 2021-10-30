import pygame as pg
from pygame.math import Vector2


class Player(pg.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()

        self.image = pg.image.load('turret.png')
        self.orig_image = self.image  # Store a reference to the original.
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)

    def update(self):
        self.rotate()

    def rotate(self):
        # The vector to the target (the mouse position).
        direction = pg.mouse.get_pos() - self.pos
        # .as_polar gives you the polar coordinates of the vector,
        # i.e. the radius (distance to the target) and the angle.
        radius, angle = direction.as_polar()
        # Rotate the image by the negative angle (y-axis in pygame is flipped).
        self.image = pg.transform.rotate(self.orig_image, -angle)
        # Create a new rect with the center of the old rect.
        self.rect = self.image.get_rect(center=self.rect.center)


pg.init()
screen = pg.display.set_mode((640, 480))
clock = pg.time.Clock()
all_sprites = pg.sprite.Group(Player((500, 220)))
done = False

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

    all_sprites.update()
    screen.fill((30, 30, 30))
    all_sprites.draw(screen)

    pg.display.flip()
    clock.tick(30)