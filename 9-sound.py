import pygame
pygame.init()

# Window settings
win_height = 480
win_width = 500
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("First game")

# General settings
score = 0

# Audio
bullet_sound = pygame.mixer.Sound('Game/Game_bullet.wav')
hit_sound = pygame.mixer.Sound('Game/Game_hit.wav')
music = pygame.mixer.music.load('Game/music.wav')
pygame.mixer.music.play(-1)

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
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.between_shots = 0
        self.health = 100
        self.visible = False

    def move_player(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.between_shots == 0:
            if self.left_move:
                facing = -1
            else:
                facing = 1
            if len(bullets) < 15:
                bullets.append(proyectile(round(self.x + self.width // 2), round(self.y + self.height // 2), 6, (0, 145, 145), facing))
            bullet_sound.play()
            self.between_shots = 1
            
        if keys[pygame.K_LEFT]:
            if self.x > 0:
                self.x -= self.vel
            else:
                self.x = 0
            self.left_move = True
            self.right_move = False
            self.standing = False
        elif keys[pygame.K_RIGHT]:
            if self.x < (win_width-self.width):
                self.x += self.vel
            else:
                self.x = win_width-self.width
            self.left_move = False
            self.right_move = True
            self.standing = False
        else:
            self.standing = True
            self.walk_count = 0
        if not self.is_jump:
            # Jump
            if keys[pygame.K_UP]:
                self.is_jump = True
        else:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.y -= (self.jump_count**2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.is_jump = False
                self.jump_count = 10
                
    def draw_player(self, window):
        if self.walk_count + 1 >= 27:
            self.walk_count = 0
        if not(self.standing):
            if self.left_move:
                window.blit(walk_left[self.walk_count//3], (self.x,self.y))
                self.walk_count += 1
            elif self.right_move:
                window.blit(walk_right[self.walk_count//3], (self.x,self.y))
                self.walk_count += 1
        else:
            if self.right_move:
                window.blit(walk_right[0], (self.x, self.y))
            else:
                window.blit(walk_left[0], (self.x, self.y))
                
        #pygame.draw.rect(window, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, self.health//2, 10))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(window, (255,0,0), self.hitbox, 2)
    
    def hit(self):
        self.x = 60
        self.y = 410
        self.walk_count = 0
        font_damage = pygame.font.SysFont('ubuntumono', 25)
        text_damage = font_damage.render('You got hit! Score -5', 1, (255,0,0))
        window.blit(text_damage, (win_width//4, win_height//2))
        pygame.display.update()
        hit_pause = 0
        while hit_pause < 100:
            pygame.time.delay(10)
            hit_pause += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    hit_pause =101
                    pygame.quit()


class proyectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

class Enemy(object):
    walk_right = [pygame.image.load(f'Game/R{sprite}E.png') for sprite in range(1,12)]
    walk_left = [pygame.image.load(f'Game/L{sprite}E.png') for sprite in range(1,12)]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.vel = 5
        self.walk_count = 0
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, window):
        self.move()
        if self.visible:
            if self.walk_count + 1 >= 33:
                self.walk_count = 0

            if self.vel > 0:
                window.blit(self.walk_right[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
            else:
                window.blit(self.walk_left[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
            pygame.draw.rect(window, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(window, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            #pygame.draw.rect(window, (255,0,0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walk_count = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel 
            else:
                self.vel = self.vel * -1
                self.walk_count = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print("Hit")

def redraw_game_window():
    window.blit(background, (0,0))
    text = font.render(f"Score: {score}", 1, (0,0,0))
    window.blit(text, (350, 10))
    hero.draw_player(window)
    villain.draw(window)
    for bullet in bullets:
        bullet.draw(window)
    pygame.display.update()

def quit_game(run_game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False
    return run_game

# Main loop
font = pygame.font.SysFont('ubuntumono', 25, True, True)
# Checks all available fonts
# print(pygame.font.get_fonts()) 
hero = Player(300, 410, 64, 64)
villain = Enemy(100, 410, 64, 64, 450)
between_shots = 0
bullets = []
run = True
while run:
    clock.tick(27)
    run = quit_game(run)

    if hero.hitbox[1] < villain.hitbox[1] + villain.hitbox[3] and hero.hitbox[1] + hero.hitbox[3] > villain.hitbox[1]:
        if hero.hitbox[0] + hero.hitbox[2] > villain.hitbox[0] and hero.hitbox[0] < villain.hitbox[0] + villain.hitbox[2]:
            hero.hit()
            score -= 5

    if hero.between_shots > 0:
        hero.between_shots += 1
    if hero.between_shots > 3:
        hero.between_shots = 0
    for bullet in bullets:
        if bullet.y - bullet.radius < villain.hitbox[1] + villain.hitbox[3] and bullet.y + bullet.radius > villain.hitbox[1]:
            if bullet.x + bullet.radius > villain.hitbox[0] and bullet.x - bullet.radius < villain.hitbox[0] + villain.hitbox[2]:
                villain.hit()
                hit_sound.play()
                score += 1
                bullets.pop(bullets.index(bullet))

        if bullet.x < 500 and bullet.x >0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    hero.move_player()
    redraw_game_window()
    
pygame.quit()