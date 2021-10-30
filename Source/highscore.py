import pygame as pg
import os
pg.init()
from settings import *
import csv
from csv import writer

class TextInput:

    def __init__(
            self,
            initial_string="",
            font_family="",
            font_size=150,
            antialias=True,
            text_color=(255, 255, 255),
            cursor_color=(0, 0, 0),
            repeat_keys_initial_ms=400,
            repeat_keys_interval_ms=35,
            max_string_length=8):

        # Text related vars:
        self.antialias = antialias
        self.text_color = text_color
        self.font_size = font_size
        self.max_string_length = max_string_length
        self.input_string = initial_string  # Inputted text

        font_folder = path.join(game_folder, 'font')

        self.font_object = pg.font.Font(path.join(font_folder, 'Imperfecta Regular.ttf'), font_size)

        # Text-surface will be created during the first update call:
        self.surface = pg.Surface((1, 1))
        self.surface.set_alpha(0)

        # Vars to make keydowns repeat after user pressed a key for some time:
        self.keyrepeat_counters = {}  # {event.key: (counter_int, event.unicode)} (look for "***")
        self.keyrepeat_intial_interval_ms = repeat_keys_initial_ms
        self.keyrepeat_interval_ms = repeat_keys_interval_ms

        # Things cursor:
        self.cursor_surface = pg.Surface((int(self.font_size / 20 + 1), self.font_size))
        self.cursor_surface.fill(cursor_color)
        self.cursor_position = len(initial_string)  # Inside text
        self.cursor_visible = True  # Switches every self.cursor_switch_ms ms
        self.cursor_switch_ms = 500  # /|\
        self.cursor_ms_counter = 0

        self.clock = pg.time.Clock()

    def update(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                self.cursor_visible = True  # So the user sees where he writes

                # If none exist, create counter for that key:
                if event.key not in self.keyrepeat_counters:
                    self.keyrepeat_counters[event.key] = [0, event.unicode]

                if event.key == pg.K_BACKSPACE:
                    self.input_string = (
                        self.input_string[:max(self.cursor_position - 1, 0)]
                        + self.input_string[self.cursor_position:]
                    )

                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)
                elif event.key == pg.K_DELETE:
                    self.input_string = (
                        self.input_string[:self.cursor_position]
                        + self.input_string[self.cursor_position + 1:]
                    )

                elif event.key == pg.K_RETURN and len(self.input_string) > 2:
                    return True

                elif event.key == pg.K_RIGHT:
                    # Add one to cursor_pos, but do not exceed len(input_string)
                    self.cursor_position = min(self.cursor_position + 1, len(self.input_string))

                elif event.key == pg.K_LEFT:
                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)

                elif event.key == pg.K_END:
                    self.cursor_position = len(self.input_string)

                elif event.key == pg.K_HOME:
                    self.cursor_position = 0

                elif len(self.input_string) < self.max_string_length or self.max_string_length == -1:
                    # If no special key is pressed, add unicode of key to input_string
                    self.input_string = (
                        self.input_string[:self.cursor_position]
                        + event.unicode
                        + self.input_string[self.cursor_position:]
                    )
                    self.cursor_position += len(event.unicode)  # Some are empty, e.g. K_UP

            elif event.type == pg.KEYUP:
                # *** Because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
                if event.key in self.keyrepeat_counters:
                    del self.keyrepeat_counters[event.key]

        # Update key counters:
        for key in self.keyrepeat_counters:
            self.keyrepeat_counters[key][0] += self.clock.get_time()  # Update clock

            # Generate new key events if enough time has passed:
            if self.keyrepeat_counters[key][0] >= self.keyrepeat_intial_interval_ms:
                self.keyrepeat_counters[key][0] = (
                    self.keyrepeat_intial_interval_ms
                    - self.keyrepeat_interval_ms
                )

                event_key, event_unicode = key, self.keyrepeat_counters[key][1]
                pg.event.post(pg.event.Event(pg.KEYDOWN, key=event_key, unicode=event_unicode))

        # Re-render text surface:
        self.surface = self.font_object.render(self.input_string, self.antialias, self.text_color)

        # Update self.cursor_visible
        self.cursor_ms_counter += self.clock.get_time()
        if self.cursor_ms_counter >= self.cursor_switch_ms:
            self.cursor_ms_counter %= self.cursor_switch_ms
            self.cursor_visible = not self.cursor_visible



        self.clock.tick()
        return False

    def get_surface(self):
        return self.surface

    def get_text(self):
        return self.input_string

    def get_cursor_position(self):
        return self.cursor_position

    def set_text_color(self, color):
        self.text_color = color

    def set_cursor_color(self, color):
        self.cursor_surface.fill(color)

    def clear_text(self):
        self.input_string = ""
        self.cursor_position = 0



def run(wave):
    # Create TextInput-object
    textinput = TextInput()

    # image, CSV and font directories
    img_folder = path.join(game_folder, 'img')
    font_folder = path.join(game_folder, 'font')
    csv_folder = path.join(game_folder, 'CSV')
    highscore_img = pg.image.load(path.join(img_folder, HIGHSCORE_IMG))

    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.DOUBLEBUF | pg.FULLSCREEN)
    clock = pg.time.Clock()
    while True:
        screen.blit(highscore_img, (1, 1))
        font_folder = path.join(game_folder, 'font')
        waveText = pg.font.Font(path.join(font_folder, 'THORN.ttf'), 72)
        waveSurface = waveText.render(str(wave), True, (255, 255, 255))
        screen.blit(waveSurface, (WIDTH/2 + 70, HEIGHT/2 + 130))

        import help
        # back button to return to menu
        options = [("BACK", (150, 675))]
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                exit()

        # feed it with events every frame
        if textinput.update(events):
            # inputs the name and capitalises it
            name = (textinput.get_text()).upper()
            # opens the CSV as append (Dictionary)
            with open((path.join(csv_folder, 'leaderboard.csv')), 'a') as file:
                field = [name, str(wave)]
                writer = csv.writer(file)
                writer.writerow(field)
                file.close()
            import menu
            menu.menu()

        # Blit its surface onto the screen
        screen.blit(textinput.get_surface(), (WIDTH/2 - 420, HEIGHT/2 - 60))
        pg.display.update()
        clock.tick(1000)