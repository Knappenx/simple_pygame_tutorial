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

	if keys[pygame.K_UP]:
		if y > 0:
			y -= vel
		else:
			y = 0
	if keys[pygame.K_DOWN]:
		if y < (win_height-height):
			y += vel
		else:
			y = win_height-height
		
	window.fill((0, 0, 0))
	pygame.draw.rect(window, (145, 200, 96), (x, y, width, height))
	pygame.display.update()

pygame.quit()
