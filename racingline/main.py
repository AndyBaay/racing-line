import sys, pygame, json
pygame.init()

size = width, height = 660, 420
speed = [2, 2]
black = 0, 0, 0
grey = 160, 160, 160 
green = 0, 153, 0

TRACK_FILE='conf/tracks/basic_square.json'
# Track format is X, Y where X is distance from the left and Y is distance from the top of the screen

# Create the window, saving it to a variable.
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption("Example resizable window")


ball = pygame.image.load("intro_ball.gif")
ballrect = ball.get_rect()


#while 1:
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT: sys.exit()
#
#    ballrect = ballrect.move(speed)
#    if ballrect.left < 0 or ballrect.right > width:
#        speed[0] = -speed[0]
#    if ballrect.top < 0 or ballrect.bottom > height:
#        speed[1] = -speed[1]
#
#    screen.fill(black)
#    screen.blit(ball, ballrect)
#    pygame.display.flip()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    screen.fill(green)

    # Draw a red rectangle that resizes with the window.
    pygame.draw.rect(screen, (200,0,0), (screen.get_width()/3,
    screen.get_height()/3, screen.get_width()/3,
    screen.get_height()/3))
    TRACK_FILE
    f = open(TRACK_FILE, "r")
    contents = f.read()
    f.close()
    track = json.loads(contents)
    track_coords = track['track']
    print(track_coords)
    pygame.draw.polygon(screen, grey, track_coords)
    #    screen.blit(ball, ballrect)
    pygame.display.flip()