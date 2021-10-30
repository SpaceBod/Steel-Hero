import pygame as pg
from settings import *
import csv
import os
import sys


def leaderboardMenu():

    class Table:
        # help menu options
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
            self.rend = table_font.render(self.text, True, self.get_color())

        def get_color(self):
                return (255, 255, 255)

        def set_rect(self):
            # sets the rectangle detection based off the size of the option
            self.set_rend()
            self.rect = self.rend.get_rect()
            self.rect.topleft = self.pos

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
    game_folder = path.dirname(__file__)
    csv_folder = path.join(game_folder, 'CSV')
    img_folder = path.join(game_folder, 'img')
    font_folder = path.join(game_folder, 'font')
    menu_img = pg.image.load(path.join(img_folder, LEADERBOARD_IMG))
    scores = []
    players = []
    total = 0

    # reads the CSV file
    with open((path.join(csv_folder, 'leaderboard.csv')), 'r') as file:  # MAKES CSV A DICTIONARY
        reader = csv.DictReader(file)
        for row in reader:
            players.append(row['player'])
            scores.append(row['score'])
            total += 1
    # converts string to integer
    scores = [int(x) for x in scores]
    # sorts the players base on scores
    sortedPlayer = [x for _, x in sorted(zip(scores, players), reverse=True)]
    # re-orders the scores in descending order
    sortedScores = sorted(scores, reverse=True)

    # initialise screen and menu
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.DOUBLEBUF | pg.FULLSCREEN)
    menu_font = pg.font.Font(path.join(font_folder, 'BroshK.ttf'), 72)
    table_font = pg.font.Font(path.join(font_folder, 'Imperfecta Regular.ttf'), 52)
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

            # limits the players to 10
            if total < 10:
                n = total
            else:
                n = 10
            for i in range(0, n):
                Table(sortedPlayer[i], (355, 190+(i*40))).draw()
                Table(str(sortedScores[i]), (960, 190 + (i * 40))).draw()

        pg.display.update()


        