import pygame as pg
from settings import *
import sys


def ShowSplash():

    # locating the menu background image
    img_folder = path.join(game_folder, 'img')
    splash_img = pg.image.load(path.join(img_folder, SPLASH_IMG))

    # initialise screen and menu
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.DOUBLEBUF | pg.FULLSCREEN)


    pg.mouse.set_visible(0)

    # option selection while loop to keep checking
    time = pg.time.get_ticks() + 3000
    pg.mixer.Sound.play(SPLASH_SFX)
    while pg.time.get_ticks()< time:
        pg.event.pump()
        screen.blit(splash_img, (1, 1))
        pg.display.update()


ShowSplash()
pg.mouse.set_visible(1)
import menu
