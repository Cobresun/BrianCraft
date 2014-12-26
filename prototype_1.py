# Project began Dec 20, 2014 

import pygame, os

class Player(object):
	def __init__(self, x, y, width, height, falling, health, crouching):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.rect = pygame.Rect(x, y, self.width, self.height)
		self.falling = True
		self.health = 1000
		self.crouching = crouching

	def crouch(self):
		self.rect = pygame.Rect(self.rect.x, self.rect.y, self.width, self.height/2)
		self.crouching = True
	
	def uncrouch(self):
		x_cord = self.rect.x
		y_cord = self.rect.y
		for x in range(0, 900, 30):
			if x <= x_cord and x_cord <= x+30:
				x_cord = x
				index_x = x/30
		for y in range(0, 830, 30):
			if y <= y_cord <= y+30:
				y_cord = y
				index_y = y/30

		if (map[index_y][index_x][0] == 1 and map[index_y][index_x+1][0] == 1):
			return
		elif (map[index_y][index_x-1][0] == 1 and map[index_y][index_x][0] == 1): 
			return
		elif map[index_y][index_x][0] == 1:
			return
		else:
			self.rect = pygame.Rect(self.rect.x, self.rect.y, self.width, self.height)
			self.crouching = False

	def move(self, dx, dy):
		# Move each axis separately. Note that this checks for collisions both times.
		self.falling = True
		if dx != 0:
			self.move_single_axis(dx, 0)
		if dy != 0:
			self.move_single_axis(0, dy)

	def move_single_axis(self, dx, dy):
		self.rect.x += dx
		self.rect.y += dy
		
		for wall in walls:
			if self.rect.colliderect(wall.rect): # When player collies with wall
				if dx < 0: # Moving left; Hit the right side of the wall
					self.rect.left = wall.rect.right
				if dx > 0: # Moving right; Hit the left side of the wall
					self.rect.right = wall.rect.left
				if dy > 0: # Moving down; Hit the top side of the wall
					self.rect.bottom = wall.rect.top
				if dy < 0: # Moving up; Hit the bottom side of the wall
					self.rect.top = wall.rect.bottom
		for enemy in enemies:
			if self.rect.colliderect(enemy.rect): # When player collides with enemy
				self.health -= 2
				if dx < 0: # Moving left; Hit the right side of the enemy
					self.rect.left = enemy.rect.right
				if dx > 0: # Moving right; Hit the left side of the enemy
					self.rect.right = enemy.rect.left
				if dy > 0: # Moving down; Hit the top side of the enemy
					self.rect.bottom = enemy.rect.top
				if dy < 0: # Moving up; Hit the bottom side of the enemy
					self.rect.top = enemy.rect.bottom

class Enemy(object):
	def __init__(self, x, y, width, height, health):
		enemies.append(self)
		self.x = x
		self.y = y
		self.height = height
		self.width = width
		self.rect = pygame.Rect(x, y, width, height)
		self.health = health
		enemies.append(self)

	def move(self, dx, dy):
		self.rect.x += dx
		self.rect.y += dy
		
		# If you collide with a wall, move out based on velocity
		for wall in walls:
			if self.rect.colliderect(wall.rect): # When enemy collides with wall
				if dx < 0: # Moving left; Hit the right side of the wall
					self.rect.left = wall.rect.right
				if dx > 0: # Moving right; Hit the left side of the wall
					self.rect.right = wall.rect.left
				if dy > 0: # Moving down; Hit the top side of the wall
					self.rect.bottom = wall.rect.top
				if dy < 0: # Moving up; Hit the bottom side of the wall
					self.rect.top = wall.rect.bottom

		if self.rect.colliderect(player.rect): # When enemy collies with player
			player.health -= 2
			if dx < 0: # Moving left; Hit the right side of the player
				self.rect.left = player.rect.right
			if dx > 0: # Moving right; Hit the left side of the player
				self.rect.right = player.rect.left
			if dy > 0: # Moving down; Hit the top side of the player
				self.rect.bottom = player.rect.top
			if dy < 0: # Moving up; Hit the bottom side of the player
				self.rect.top = player.rect.bottom
	
class Wall(object):
	def __init__(self, x, y):
		walls.append(self) # Make it so that this adds it to the map
		self.x = x
		self.y = y
		self.rect = pygame.Rect(x, y, 30, 30)

	def destroy(self):
		walls.remove(self)

class Air(object):
	def __init__(self, x, y):
		airs.append(self)
		self.x = x
		self.y = y
		self.rect = pygame.Rect(x, y, 30, 30)

	def destroy(self):
		walls.remove(self)

def gravity(player):
	surface = False
	while surface == False:
		player.rect.y += 3
		for wall in walls:
			if player.rect.colliderect(wall.rect):
				player.rect.bottom = wall.rect.top
				player.falling = False
			surface = True		

def place(block, pos):
	x_cord = pos[0]
	y_cord = pos[1]

	#if block == "wall":
	for x in range(0, 900, 30):
		if x <= x_cord and x_cord <= x+30:
			x_cord = x
			index_x = x/30
	for y in range(0, 830, 30):
		if y <= y_cord <= y+30:
			y_cord = y
			index_y = y/30
	if enemy.rect.y-20 <= y_cord and y_cord <= enemy.rect.y+(enemy.height-5) and enemy.rect.x-20 <= x_cord and x_cord <= enemy.rect.x+20:
		return
	if player.rect.y-20 <= y_cord and y_cord <= player.rect.y+(player.height - 5) and player.rect.x-20 <= x_cord and x_cord <= player.rect.x+20:
		return
	if map[index_y][index_x][0] == 1:
		return
	map[index_y][index_x][0] = 1

def destroy(block, pos):
	x_cord = pos[0]
	y_cord = pos[1]
	#if block == "wall":
	for x in range(0, 900, 30):
		if x <= x_cord and x_cord <= x+30:
			x_cord = x
			index_x = x/30
	for y in range(0, 830, 30):
		if y <= y_cord <= y+30:
			y_cord = y
			index_y = y/30
	map[index_y][index_x][0] = 0

def map_update():
	global walls
	walls = []
	x = y = 0
	for row in map:
		for col in row:
			if col[0] == 1:
				Wall(x, y)
			#if col == "0":
				#Air(x, y)		
			x += 30
		y += 30
		x = 0

def enemy_AI():
	for enemy in enemies:
		if player.rect.x < enemy.rect.x:
			enemy.move(-1, 0)
		elif player.rect.x > enemy.rect.x:
			enemy.move(1, 0)
		elif player.rect.x == enemy.rect.x:
			enemy.move(0, 0)

# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Set up the display
pygame.display.set_caption("BrianCraft")
screen = pygame.display.set_mode((900, 830))
clock = pygame.time.Clock()

walls = [] # List to hold the walls
airs = []
enemies = [] # Lsit all the enemies
player = Player(30, 300, 25, 55, False, 100, False) # Create the player
enemy = Enemy(500, 300, 30, 90, 500) # Create the Enemy
font = pygame.font.SysFont(None, 50)
LEFT = 1
RIGHT = 3

# Move map to different file at some point
map = [
	[[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1]],
	[[1],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[1]],
	[[1],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[1]],
	[[1],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[1]],
	[[1],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[1]],
	[[1],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[1]],
	[[1],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[1]],
	[[1],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[1]],
	[[1],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[1]],
	[[1],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[1]],
	[[1],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[1]],
	[[1],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[1]],
	[[1],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[1]],
	[[1],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[1]],
	[[1],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[1]],
	[[1],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[1]],
	[[1],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[1]],
	[[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1]],
	]
map_update()

running = True

while running:

# Sets framerate
	clock.tick(60)

# Gravity
	gravity(player)
	gravity(enemy)

# Enemy AI
	enemy_AI()

# Leave game, and jump
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			running = False
		if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
			running = False
		if e.type == pygame.KEYUP:
			if e.key == pygame.K_SPACE and player.falling == False and player.crouching == False:
				player.move(0, -60)
		if e.type == pygame.MOUSEBUTTONUP and e.button == RIGHT:
			pos = pygame.mouse.get_pos()
			place("wall", pos) # Places the block at that x-y coord
			map_update() 
		if e.type == pygame.MOUSEBUTTONUP and e.button == LEFT:
			pos = pygame.mouse.get_pos()
			destroy("wall", pos) # Places the block at that x-y coord
			map_update()


# Move the player if an arrow key is pressed
	key = pygame.key.get_pressed()
	if key[pygame.K_a]:
		player.move(-3, 0)
	if key[pygame.K_d]:
		player.move(3, 0)
 	if key[pygame.K_LSHIFT]:
		player.crouch()
	else:
		player.uncrouch()

# Display Health
	player_health = font.render(str(player.health), True, (0, 128, 0))
	enemy_health = font.render(str(enemy.health), True, (255, 51, 51))

# Game Over
	if player.health < 1:
		print 'Game Over!'
		break

# Drawing the scene
	screen.fill((0, 0, 0))
	for wall in walls:
		pygame.draw.rect(screen, (100, 100, 100), wall.rect)
	for air in airs:
		pygame.draw.rect(screen, (255, 255, 255), air.rect)
	pygame.draw.rect(screen, (200, 103, 123), player.rect)
	for enemy in enemies:
		pygame.draw.rect(screen, (50, 100, 50), enemy.rect)

	screen.blit(player_health, (player.rect.x-20, player.rect.y-40))
	screen.blit(enemy_health, (enemy.rect.x-20, enemy.rect.y-40))

	pygame.display.flip()
