import pygame
pygame.init()

# Window settings
win_height = 480
win_width = 500
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("First game")

# Clock speed
clock = pygame.time.Clock()

# Character attributes
width = 64
height = 64
x = 50
y = win_height - height -10
vel = 10

# Jump attributes
is_jump = False
jump_count = 10

# Char Sprite load
walk_right = [pygame.image.load(f'Game/R{sprite}.png') for sprite in range(1,10)]
walk_left = [pygame.image.load(f'Game/L{sprite}.png') for sprite in range(1,10)]
background = pygame.image.load('Game/bg.jpg')
char = pygame.image.load('Game/standing.png')
print(walk_right)
# Char walk attributes
left = False
right = False
walk_count = 0

def redraw_game_window():
    global walk_count
    window.blit(background, (0,0))
    if walk_count + 1 >= 27:
        walk_count = 0
    if left:
        window.blit(walk_left[walk_count//3], (x,y))
        walk_count += 1
    elif right:
        window.blit(walk_right[walk_count//3], (x,y))
        walk_count += 1
    else:
        window.blit(char, (x,y))
    pygame.display.update()

# Main loop
run = True
while run:
    clock.tick(27)
    redraw_game_window()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
	# Movement
    if keys[pygame.K_LEFT]:
        if x > 0:
            x -= vel
        else:
            x = 0
        left = True
        right = False
    elif keys[pygame.K_RIGHT]:
        if x < (win_width-width):
            x += vel
        else:
            x = win_width-width
        left = False
        right = True
    else:
        left = False
        right = False
        walk_count = 0

    if not is_jump:
        # Jump
        if keys[pygame.K_SPACE]:
            is_jump = True
    else:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            y -= (jump_count**2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jump = False
            jump_count = 10

pygame.quit()