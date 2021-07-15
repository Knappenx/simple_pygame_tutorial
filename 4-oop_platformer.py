import pygame
pygame.init()

# Window settings
win_height = 480
win_width = 500
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("First game")

# Clock speed
clock = pygame.time.Clock()

# Char Sprite load
walk_right = [pygame.image.load(f'Game/R{sprite}.png') for sprite in range(1,10)]
walk_left = [pygame.image.load(f'Game/L{sprite}.png') for sprite in range(1,10)]
background = pygame.image.load('Game/bg.jpg')
char = pygame.image.load('Game/standing.png')

class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 10
        self.is_jump = False
        self.jump_count = 10
        self.left_move = False
        self.right_move = False
        self.walk_count = 0

    def draw_player(self, window):
        if self.walk_count + 1 >= 27:
            self.walk_count = 0
        if self.left_move:
            window.blit(walk_left[self.walk_count//3], (self.x,self.y))
            self.walk_count += 1
        elif self.right_move:
            window.blit(walk_right[self.walk_count//3], (self.x,self.y))
            self.walk_count += 1
        else:
            window.blit(char, (self.x,self.y))

def redraw_game_window():
    window.blit(background, (0,0))
    hero.draw_player(window)
    pygame.display.update()

# Main loop
hero = Player(300, 410, 64, 64)
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
        if hero.x > 0:
            hero.x -= hero.vel
        else:
            hero.x = 0
        hero.left_move = True
        hero.right_move = False
    elif keys[pygame.K_RIGHT]:
        if hero.x < (win_width-hero.width):
            hero.x += hero.vel
        else:
            hero.x = win_width-hero.width
        hero.left_move = False
        hero.right_move = True
    else:
        hero.left_move = False
        hero.right_move = False
        hero.walk_count = 0

    if not hero.is_jump:
        # Jump
        if keys[pygame.K_SPACE]:
            hero.is_jump = True
    else:
        if hero.jump_count >= -10:
            neg = 1
            if hero.jump_count < 0:
                neg = -1
            hero.y -= (hero.jump_count**2) * 0.5 * neg
            hero.jump_count -= 1
        else:
            hero.is_jump = False
            hero.jump_count = 10

pygame.quit()