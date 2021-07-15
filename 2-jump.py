import pygame
pygame.init()

# Window settings
win_height = 500
win_width = 500
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("First game")

# Character attributes
x = 50
y = 350
width = 40
height = 60
vel = 10

is_jump = False
jump_count = 10


# Main loop
run = True
while run:
	pygame.time.delay(50)

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
	if keys[pygame.K_RIGHT]:
		if x < (win_width-width):
			x += vel
		else:
			x = win_width-width
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
	

	window.fill((0, 0, 0))
	pygame.draw.rect(window, (145, 200, 96), (x, y, width, height))
	pygame.display.update()

pygame.quit()
