import sys, pygame, json
from racingline.lib.color import RED, DARK_GRAY, WHITE
from racingline.lib.line_generator import calc_normal_line, upsample_line

### Load Track ###
TRACK_FILE='conf/tracks/basic_square.json'

track_definition = {}
with open(TRACK_FILE, "r") as f:
    track_definition = json.load(f)

track_size = tuple(track_definition['track_dimensions'])
background_color = tuple(track_definition['track_background_color'])
finish_line = track_definition['finish_line']
outer_track_limits = track_definition['outer_track_limits']
inner_track_limits = track_definition['inner_track_limits']
TRACK_COLOR = DARK_GRAY
inner_track_limits = upsample_line(inner_track_limits)

### Initialized Pygame ###
pygame.init()
# Create the window, saving it to a variable.
screen = pygame.display.set_mode(track_size, pygame.RESIZABLE)
pygame.display.set_caption("Max Verstappen - WDC")


### Main Loop ###
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    screen.fill(background_color)

    pygame.draw.polygon(screen, TRACK_COLOR, outer_track_limits)
    pygame.draw.polygon(screen, background_color, inner_track_limits)
    pygame.draw.line(screen, WHITE, finish_line[0], finish_line[1], 3)

    for point in outer_track_limits + inner_track_limits:
        pygame.draw.circle(screen, WHITE, point, 2)

    for index in range(0, len(inner_track_limits) - 1 ):
        second_index = (index + 1) % ( len(inner_track_limits) - 1 )
        normal_line = calc_normal_line(inner_track_limits[index], inner_track_limits[second_index])
        pygame.draw.line(screen, RED, normal_line[0], normal_line[1], 1)

    pygame.display.flip()