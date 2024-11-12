import json
import logging
import random
import sys
from datetime import datetime

import pygame
import pygame_menu

from racingline.lib.line_generator import (
    calc_normal_line,
    distance_between,
    get_midpoint,
    upsample_line,
)

from .graphics.button import Button
from .graphics.cursor import Cursor
from .lib.constants import GRID_SQUARE_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH, Color
from .lib.geometery import find_intersection

LOGGER = logging.getLogger(__name__)

LOGGER.warning("Started")
### Load Track ###
TRACK_FILE = "conf/tracks/basic_square.json"


def run_track(screen, file):
    print(file)
    track_definition = {}
    with open(file, "r") as f:
        track_definition = json.load(f)

    track_size = tuple(track_definition["track_dimensions"])
    background_color = tuple(track_definition["track_background_color"])
    finish_line = track_definition["finish_line"]
    outer_track_limits = track_definition["outer_track_limits"]
    inner_track_limits = track_definition["inner_track_limits"]
    TRACK_COLOR = Color.DARK_GRAY.value

    ### Add Centerline ###
    inner_track_limits = upsample_line(inner_track_limits)
    outer_track_limits = upsample_line(outer_track_limits)
    centerline = []
    last_outer_point_index = 0

    for index in range(0, len(inner_track_limits) - 1):
        second_index = (index + 1) % (len(inner_track_limits) - 1)
        # Create a normal line from the inner track
        normal_line = calc_normal_line(
            inner_track_limits[index], inner_track_limits[second_index]
        )

        # Find its minimum intersection with the outer track and trim
        min_point = None
        min_distance = float("inf")
        for index in range(0, len(outer_track_limits) - 1):
            # Remember where we last found an intersection and start there for the next segment of inner track
            index = (index + last_outer_point_index) % (len(outer_track_limits) - 1)

            if intersect := find_intersection(
                normal_line, [outer_track_limits[index], outer_track_limits[index + 1]]
            ):
                # if intersect := line_intersection(
                #     normal_line, [outer_track_limits[index], outer_track_limits[index + 1]]
                # ):
                dist = distance_between(normal_line[0], intersect)
                if dist < min_distance:
                    min_distance = dist
                    min_point = intersect

        # Create a centerline point from this normal line
        if min_point:
            centerline.append(get_midpoint(normal_line[0], min_point))

    ### Initialize Surface ###
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
        pygame.draw.polygon(screen, Color.BLACK.value, centerline, 1)
        pygame.draw.line(screen, Color.WHITE.value, finish_line[0], finish_line[1], 3)

        for point in outer_track_limits + inner_track_limits:
            pygame.draw.circle(screen, Color.WHITE.value, point, 2)

        for index in range(0, len(inner_track_limits) - 1):
            second_index = (index + 1) % (len(inner_track_limits) - 1)
            normal_line = calc_normal_line(
                inner_track_limits[index], inner_track_limits[second_index]
            )
            pygame.draw.line(screen, Color.RED.value, normal_line[0], normal_line[1], 1)

        pygame.display.flip()


def edit_track():
    pass


##### EDITOR ####
buffer = []


def draw_grid(width, surface):
    space_between_lines = GRID_SQUARE_SIZE
    for i in range(int(0 + (GRID_SQUARE_SIZE / 2)), width, space_between_lines):
        x, y = i, i
        pygame.draw.line(surface, Color.LIGHT_GREEN.value, (x, 0), (x, width))
        pygame.draw.line(surface, Color.LIGHT_GREEN.value, (0, y), (width, y))


def save_track(screen, lines):
    if len(lines) < 2:
        print("Error saving track. 2 lines are required (outer and inner boundaries)")
        return
    x, y = screen.get_size()
    track_definition = {
        "track_dimensions": [x, y],
        "track_background_color": list(Color.LIGHT_GREEN.value),
        "inner_track_limits": lines[0],
        "outer_track_limits": lines[1],
        "finish_line": [lines[0][0], lines[1][0]],
    }
    output_file_name = "track_" + str(random.randrange(0, 10000)).zfill(5) + ".json"
    out_file = open(output_file_name, "a")
    out_file.write(json.dumps(track_definition))
    out_file.close()
    print(f"Track saved to {output_file_name}")


def create_track(screen):
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    cursor = Cursor()
    completed_lines = []
    exit_to_menu_button = Button(
        (120, 10), 120, 24, "exit to menu", on_click=pygame_menu.events.RESET
    )
    save_button = Button(
        (40, 10), 70, 24, "save", on_click=lambda: save_track(screen, completed_lines)
    )
    TRACK_COLOR = Color.DARK_GRAY.value

    run = True
    while run:
        clock.tick(60)
        screen.fill(Color.DARK_GREEN.value)
        mouse_pressed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # checks if mouse position is over the button
                captured_click = save_button.check_for_click(event.pos)

                # if we didn't handle the click, pass it on
                mouse_pressed = not captured_click

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    cursor.clear_points()
                if event.key == pygame.K_BACKSPACE:
                    cursor.remove_last_point()

        mouse_pos = pygame.mouse.get_pos()

        if new_line := cursor.update(mouse_pressed):
            print(new_line)
            completed_lines.append(new_line)
        save_button.update(mouse_pos)
        exit_to_menu_button.update(mouse_pos)

        draw_grid(screen.get_width(), screen)
        # Draw current line
        if len(buffer) == 1:
            # Add the first point
            pygame.draw.circle(screen, TRACK_COLOR, buffer[0], 1)
        if len(buffer) > 1:
            # Draw line segment
            pygame.draw.lines(screen, TRACK_COLOR, False, buffer, width=20)
            pygame.draw.lines(screen, Color.LIGHT_BLUE.value, False, buffer, width=2)

        # Draw the guide-line segment
        if len(buffer) >= 1:
            pygame.draw.lines(
                screen,
                TRACK_COLOR,
                False,
                [buffer[-1], (cursor.center[0], cursor.center[1])],
                width=20,
            )
            pygame.draw.lines(
                screen,
                Color.LIGHT_BLUE.value,
                False,
                [buffer[-1], (cursor.center[0], cursor.center[1])],
                width=2,
            )

        # Draw previously saved lines
        for line in completed_lines:
            pygame.draw.lines(screen, Color.LIGHT_GRAY.value, False, line, width=2)

        cursor.draw(screen)
        save_button.draw(screen)
        exit_to_menu_button.draw(screen)
        pygame.display.flip()
