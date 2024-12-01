from datetime import datetime

import pygame

from ..lib.constants import GRID_SQUARE_SIZE, Color


class Cursor:
    def __init__(self):
        self.last_click = datetime(1, 1, 1)
        self.buffer = []

    def clear_points(self):
        self.buffer = []

    def remove_last_point(self):
        if len(self.buffer) > 0:
            self.buffer.pop()

    def update(self, clicked):
        """
        Updates the cursor with the latest mouse interaction. If the last interaction completes a
        line it will be returned, otherwise None is returned.
        """
        x, y = pygame.mouse.get_pos()
        column_num = x // GRID_SQUARE_SIZE
        row_num = y // GRID_SQUARE_SIZE
        self.cx, self.cy = column_num * GRID_SQUARE_SIZE, row_num * GRID_SQUARE_SIZE
        center_x = column_num * GRID_SQUARE_SIZE + int(GRID_SQUARE_SIZE / 2)
        center_y = row_num * GRID_SQUARE_SIZE + int(GRID_SQUARE_SIZE / 2)

        self.center = (center_x, center_y)
        self.clicked = clicked

        # enforce a minimum time between clicks to avoid double-click after finishing a line
        if self.clicked and (datetime.now() - self.last_click).total_seconds() > 0.2:
            self.last_click = datetime.now()

            if len(self.buffer) == 0:
                self.buffer.append(self.center)
            elif self.buffer[-1] != self.center:
                self.buffer.append(self.center)

            if len(self.buffer) >= 2:
                if self.buffer[0] == self.buffer[-1]:
                    completed_line = [p for p in self.buffer]
                    self.buffer = []
                    return completed_line

        return None

    def draw(self, surface):
        # # enforce a minimum time between clicks to avoid double-click after finishing a line
        # if self.clicked and (datetime.now() - self.last_click).total_seconds() > 0.2:
        #     self.last_click = datetime.now()

        #     if len(self.buffer) == 0:
        #         self.buffer.append(self.center)
        #     elif self.buffer[-1] != self.center:
        #         self.buffer.append(self.center)

        #     if len(self.buffer) >= 2:
        #         if self.buffer[0] == self.buffer[-1]:
        #             line_to_draw = [p for p in self.buffer]
        #             self.buffer = []

        if len(self.buffer) == 1:
            # Add the first point
            pygame.draw.circle(surface, Color.DARK_GRAY.value, self.buffer[0], 1)
        if len(self.buffer) > 1:
            # Draw line segment
            pygame.draw.lines(
                surface, Color.DARK_GRAY.value, False, self.buffer, width=20
            )
            pygame.draw.lines(
                surface, Color.LIGHT_BLUE.value, False, self.buffer, width=2
            )

        # Draw the guide-line segment
        if len(self.buffer) >= 1:
            pygame.draw.lines(
                surface,
                Color.DARK_GRAY.value,
                False,
                [self.buffer[-1], (self.center[0], self.center[1])],
                width=20,
            )
            pygame.draw.lines(
                surface,
                Color.LIGHT_BLUE.value,
                False,
                [self.buffer[-1], (self.center[0], self.center[1])],
                width=2,
            )

        pygame.draw.circle(
            surface, Color.WHITE.value, (self.center[0], self.center[1]), 4
        )
