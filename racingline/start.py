import os
from functools import partial

import pygame
import pygame_menu

from .lib.constants import FPS, WINDOW_HEIGHT, WINDOW_WIDTH, Color
from .run_mode import create_track, edit_track, run_track

MODE = {"run_track": run_track, "edit_track": edit_track, "create_track": create_track}


class Menu(object):
    def __init__(self):
        self.selected_run_mode = None
        self.run_mode_args = {}

        ### Initialize Main Menu ###
        self.menu = pygame_menu.Menu(
            title="Welcome",
            height=WINDOW_HEIGHT * 0.9,
            width=WINDOW_WIDTH * 0.9,
            theme=pygame_menu.themes.THEME_BLUE,
        )

        ### Initialize Load Track Menu ###
        load_track_menu = pygame_menu.Menu(
            height=WINDOW_HEIGHT * 0.9,
            theme=pygame_menu.themes.THEME_BLUE,
            title="Load Track",
            width=WINDOW_WIDTH * 0.9,
        )
        for file in os.listdir("./conf/tracks"):
            if file.endswith(".json"):
                load_track_menu.add.button(
                    file,
                    partial(
                        self.set_run_mode,
                        "run_track",
                        {"file": os.path.join("./conf/tracks", file)},
                    ),
                )

        load_track_menu.add.button("Return to Menu", pygame_menu.events.BACK)

        def build_new_track():
            print("Building new track")

        self.menu.add.button("Select Track", load_track_menu)
        self.menu.add.button(
            "Create New Track",
            partial(
                self.set_run_mode,
                "create_track",
                {},
            ),
        )
        self.menu.add.button("Quit", pygame_menu.events.EXIT)

    def set_run_mode(self, run_mode, run_mode_args, close_menu=True):
        self.selected_run_mode = MODE[run_mode]
        self.run_mode_args = run_mode_args
        if close_menu:
            self.menu.disable()
        import json

        print(json.dumps(run_mode_args))


def start():
    ### Initialize pygame ###
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    game_menu = Menu()

    ### Start Game Loop ###
    run = True
    while run:
        clock.tick(FPS)
        screen.fill(Color.DARK_GREEN.value)

        if game_menu.menu.is_enabled():
            game_menu.menu.mainloop(screen)

        # Run the selected mode
        run = game_menu.selected_run_mode(screen, **game_menu.run_mode_args)
