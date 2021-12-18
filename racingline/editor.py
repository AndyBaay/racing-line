import pygame, copy
from datetime import datetime
import random,json

# Settings
GRID_SQUARE_SIZE=16
WINDOW_WIDTH=550
WINDOW_HEIGHT=300

# Color Constants
RED = (200,0,0)
WHITE = (255, 255, 255)
LIGHT_GREEN = (0, 204, 0) 
DARK_GREEN = (0, 153, 0) 
LIGHT_BLUE = (102, 178, 255)
LIGHT_GRAY = (224, 224, 224)
GRAY = (192, 192, 192)
BLACK = (0, 0, 0)

TRACK_COLOR = (0, 0, 0)
TRACK_COLOR_2 = (192, 192, 192)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()
# defining a font
smallfont = pygame.font.SysFont('Corbel',35)

def draw_grid(width, surface):
    space_between_lines = GRID_SQUARE_SIZE
    for i in range(int(0+(GRID_SQUARE_SIZE/2)), width, space_between_lines):
        x, y = i, i
        pygame.draw.line(surface, LIGHT_GREEN, (x, 0), (x, width))
        pygame.draw.line(surface, LIGHT_GREEN, (0, y), (width, y))

buffer = []
drawn_lines = []
def save_track(screen):
    if len(drawn_lines) < 2:
        print('Error saving track. 2 lines are required (outer and inner boundaries)')
        return
    x, y = screen.get_size()
    track_definition = {
        "track_dimensions": [x, y], 
        "track_background_color": list(LIGHT_GREEN),
        "outer_track_limits": drawn_lines[0],
        "inner_track_limits": drawn_lines[1],
    }
    output_file_name = "track_" + str(random.randrange(0, 10000)).zfill(5) + ".json"
    out_file = open(output_file_name, "a")
    out_file.write(json.dumps(track_definition))
    out_file.close()
    print(f"Track saved to {output_file_name}")


class Cursor:
    def __init__(self):
        self.last_click = datetime(1, 1, 1)

    def update(self, clicked):
        x, y = pygame.mouse.get_pos()
        column_num = x // GRID_SQUARE_SIZE
        row_num = y // GRID_SQUARE_SIZE
        self.cx, self.cy = column_num * GRID_SQUARE_SIZE, row_num * GRID_SQUARE_SIZE
        center_x = column_num * GRID_SQUARE_SIZE + int(GRID_SQUARE_SIZE/2)
        center_y = row_num * GRID_SQUARE_SIZE  + int(GRID_SQUARE_SIZE/2)

        self.center = (center_x, center_y)
        self.clicked = clicked 


    def draw(self, surface):
        global buffer

        # enforce a minimum time between clicks to avoid double-click after finishing a line
        if self.clicked and (datetime.now() - self.last_click).total_seconds() > 0.2:
            self.last_click = datetime.now()

            if len(buffer) == 0:
                buffer.append(self.center)
            elif buffer[-1] != self.center:
                buffer.append(self.center)

            if len(buffer) >= 2:
                if buffer[0] == buffer[-1]:
                    drawn_lines.append(copy.deepcopy(buffer))
                    buffer = []
        pygame.draw.circle(screen, WHITE, (self.center[0], self.center[1]), 4)
        #pygame.draw.rect(surface, (255, 255, 255), self.square)

class SaveButton:
    def __init__(self, pos, width, height, text_color=BLACK, default_color=WHITE, hover_color=LIGHT_GRAY, pressed_color=LIGHT_BLUE):
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.text = smallfont.render(' save' , True , text_color)
        self.state = "" # hover, pressed, or empty string
        self.last_click = datetime(1, 1, 1)
        self.default_color = default_color
        self.hover_color = hover_color
        self.pressed_color = pressed_color

    def check_for_click(self, mouse_pos, screen):
        if self.rect.collidepoint(mouse_pos):
            self.state = "pressed"
            self.last_click = datetime.now()
            save_track(screen)
            return True
        else:
            return False
        

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.state = "hover"
        else:
            self.state = ""

    def draw(self, screen):
        # Keep the highlighted color longer than the actual event for a button press
        if (datetime.now() - self.last_click).total_seconds() < 0.2:
            button_color = self.pressed_color
        elif self.state == "hover":
            button_color = self.hover_color
        else:
            button_color = self.default_color

        pygame.draw.rect(screen, button_color, self.rect)
        screen.blit(self.text, self.rect)


cursor = Cursor()
save_button = SaveButton((40, 10), 70, 24)

run = True
while run:
    clock.tick(60)
    screen.fill(DARK_GREEN)
    mouse_pressed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # checks if mouse position is over the button
            captured_click = save_button.check_for_click(event.pos, screen)

            # if we didn't handle the click, pass it on
            mouse_pressed = not captured_click
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                buffer = []
            if event.key == pygame.K_BACKSPACE and len(buffer) >= 1:
                buffer.pop()

    mouse_pos = pygame.mouse.get_pos()
    
    cursor.update(mouse_pressed)
    save_button.update(mouse_pos)

    draw_grid(screen.get_width(), screen)
    # Draw current line
    if len(buffer) == 1:
        # Add the first point
        pygame.draw.circle(screen, TRACK_COLOR, buffer[0], 1)
    if len(buffer) > 1:
        # Draw line segment
        pygame.draw.lines(screen, TRACK_COLOR, False, buffer, width=2)
    
    # Draw the guide-line segment
    if len(buffer) >= 1:
        pygame.draw.lines(screen, TRACK_COLOR, False, [buffer[-1], (cursor.center[0], cursor.center[1])], width=2)

    # Draw previously saved lines
    for line in drawn_lines:
        pygame.draw.lines(screen, TRACK_COLOR_2, False, line, width=2)


    cursor.draw(screen)
    save_button.draw(screen)
    pygame.display.flip()