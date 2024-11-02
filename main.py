import argparse
import json
import logging
import sys

import pygame

from racingline.editor import GRAY, RED, WHITE, start_editor

# from racingline.editor import calc_normal_line, upsample_line

LOGGER = logging.getLogger(__name__)

LOGGER.warning("Started")
### Load Track ###
TRACK_FILE = "conf/tracks/basic_square.json"


def run_track():
    print("Running track")

    LOGGER.warning("Import finished")
    track_definition = {}
    with open(TRACK_FILE, "r") as f:
        track_definition = json.load(f)

    track_size = tuple(track_definition["track_dimensions"])
    background_color = tuple(track_definition["track_background_color"])
    finish_line = track_definition["finish_line"]
    outer_track_limits = track_definition["outer_track_limits"]
    inner_track_limits = track_definition["inner_track_limits"]
    TRACK_COLOR = GRAY
    # exit()
    # inner_track_limits = upsample_line(inner_track_limits)

    ### Initialized Pygame ###
    pygame.init()
    # Create the window, saving it to a variable.
    screen = pygame.display.set_mode(track_size, pygame.RESIZABLE)
    pygame.display.set_caption("Max Verstappen - WDC")

    ### Main Loop ###
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(background_color)

        pygame.draw.polygon(screen, TRACK_COLOR, outer_track_limits)
        pygame.draw.polygon(screen, background_color, inner_track_limits)
        pygame.draw.line(screen, WHITE, finish_line[0], finish_line[1], 3)

        for point in outer_track_limits + inner_track_limits:
            pygame.draw.circle(screen, WHITE, point, 2)

        for index in range(0, len(inner_track_limits) - 1):
            second_index = (index + 1) % (len(inner_track_limits) - 1)
            normal_line = calc_normal_line(
                inner_track_limits[index], inner_track_limits[second_index]
            )
            pygame.draw.line(screen, RED, normal_line[0], normal_line[1], 1)

        pygame.display.flip()


def build_track():
    print("Building track")
    start_editor()
    pass


def main():
    # Instantiate the parser
    parser = argparse.ArgumentParser(description="Racing Line Calculation")
    sub = parser.add_subparsers(dest="command", help="sub-command help")

    # Build a track
    parser_auth = sub.add_parser("build-track")
    parser_auth.set_defaults(func=build_track)

    # Evaluate a track
    parser_auth = sub.add_parser("run-track")
    parser_auth.set_defaults(func=run_track)

    args = parser.parse_args()
    print(f"Args: {args}")
    args.func()


if __name__ == "__main__":
    print("running")
    main()
