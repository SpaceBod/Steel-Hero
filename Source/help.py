import pygame as pg
from settings import *
import sys


def helpMenu():
    class Option:

        # help menu options
        hovered = False
        def __init__(self, text, pos):
            # a function to insert text
            self.text = text
            self.pos = pos
            self.set_rect()
            self.draw()

        def draw(self):
            # draws the options on the screen
            self.set_rend()
            screen.blit(self.rend, self.rect)

        def set_rend(self):
            # render the text with font
            self.rend = menu_font.render(self.text, True, self.get_color())

        def get_color(self):
            # colour change on hover
            if self.hovered:
                # highlight colour
                return (255, 255, 255)
            else:
                # normal colour
                return (0, 0, 0)

        def set_rect(self):
            # sets the rectangle detection based off the size of the option
            self.set_rend()
            self.rect = self.rend.get_rect()
            self.rect.topleft = self.pos

    # locating the menu background image
    img_folder = path.join(game_folder, 'img')
    font_folder = path.join(game_folder, 'font')
    menu_img = pg.image.load(path.join(img_folder, HELP_IMG))

    # initialise screen and menu
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.DOUBLEBUF | pg.FULLSCREEN)
    menu_font = pg.font.Font(path.join(font_folder, 'BroshK.ttf'), 72)
    options = [Option("BACK", (150, 675))]
    pg.mouse.set_cursor(*pg.cursors.broken_x)

    # option selection while loop to keep checking
    while True:
        pg.event.pump()
        screen.blit(menu_img, (1, 1))
        for option in options:

            # mouse detection
            if option.rect.collidepoint(pg.mouse.get_pos()):
                option.hovered = True
                for event in pg.event.get():
                    if event.type == pg.MOUSEBUTTONDOWN:

                        # option 1: back
                        if option == options[0]:
                            import menu
                            while True:
                                menu.menu()
            else:
                option.hovered = False
            option.draw()
        pg.display.update()
