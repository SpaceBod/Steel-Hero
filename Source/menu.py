import pygame as pg
from settings import *
import main
import sys
from sprites import *
from time import sleep




def menu():
    class Option:
        # main menu options
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


    class turretMenu(pg.sprite.Sprite):
        image = None

        def __init__(self, location):
            pg.sprite.Sprite.__init__(self)

            if turretMenu.image is None:
                game_folder = path.dirname(__file__)
                img_folder = path.join(game_folder, 'img')
                turretMenu.image = pg.image.load(path.join(img_folder, 'turret.png')).convert_alpha()
                turretMenu.image = pg.transform.scale(turretMenu.image, (462, 308))
                turretMenu.image = pg.transform.rotate(turretMenu.image, 170)
            self.image = turretMenu.image


            # Make our top-left corner the passed-in location.
            self.rect = self.image.get_rect()
            self.rect.topleft = location



    # main code for interface


    # locating the menu background image
    img_folder = path.join(game_folder, 'img')
    font_folder = path.join(game_folder, 'font')
    menu_img = pg.image.load(path.join(img_folder, MENU_IMG))


    # initialise screen and menu
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.DOUBLEBUF | pg.FULLSCREEN)
    menu_font = pg.font.Font(path.join(font_folder, 'BroshK.ttf'), 72)
    options = [Option("START", (150, 350)), Option("LEADERBOARD", (150, 450)), Option("HELP", (150, 550)), Option("QUIT", (150, 650))]

    pg.mouse.set_cursor(*pg.cursors.broken_x)



    while True:
        pg.event.pump()
        screen.blit(menu_img, (1, 1))
        b = turretMenu([866, 388])
        screen.blit(b.image, b.rect)

        for option in options:
            # mouse detection
            if option.rect.collidepoint(pg.mouse.get_pos()):
                option.hovered = True

                for event in pg.event.get():
                    if event.type == pg.MOUSEBUTTONDOWN:

                        # option 1: start
                        if option == options[0]:
                            g = main.Game()
                            while True:
                                g.new()
                                g.run()

                        # option 2: leaderboard
                        if option == options[1]:
                            import leaderboard
                            while True:
                                leaderboard.leaderboardMenu()

                        # option 2: help
                        if option == options[2]:
                            import help
                            while True:
                                help.helpMenu()

                        # option 3: quit
                        if option == options[3]:
                            pg.quit()
                            sys.exit()
            else:
                option.hovered = False

            option.draw()
        pg.display.update()


menu()