import pygame as pg
import random as rdm                                                    # For the sake of random positioning of aliens
import math                                                             # For the distance check while collision
from pygame import mixer                                            # For sounds
import time

# Initialize pygame
pg.init()

# Screen dimensions
screen_width = 1200
screen_height = 650

# Colors
maroon = (128, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)

# A screen for pygame
screen = pg.display.set_mode((screen_width, screen_height))

# Backgound
bg = pg.image.load('bg.png')

mixer.music.load("background.mp3")
mixer.music.set_volume(0.7)
mixer.music.play(-1)


# Title and Icon.
pg.display.set_caption("Space invaders")      # Title
icon = pg.image.load('ufo.png')               # Icon
pg.display.set_icon(icon)


# Player Ship.
ship_img = pg.image.load('ship.png')          # Loading the ship
ship_x = 560                                  # Coordinates of ship
ship_y = 550
ship_x_change = 0

# Enemy alien ship.
alien_img = []
alien_x = []
alien_y = []
alien_x_change = []
alien_y_change = []
num_of_alien = 6
for i in range(num_of_alien):
	alien_img.append(pg.image.load('alien.png'))          # Loading the alien
	alien_x.append(rdm.randint(0,1135))                  # Coordinates of alien
	alien_y.append(rdm.randint(50, 150))
	alien_x_change.append(8)
	alien_y_change.append(10)

# Bullet.
bullet_img = pg.image.load('bullet.png')          # Loading the bullet
bullet_x = 0                                      # Coordinates of bullet
bullet_y = 550
bullet_x_change = 0
bullet_y_change = 20
bullet_state = "rest"                            # Rest - you can't see the bullet currently on the screen

# Score
score_value = 0
font = pg.font.Font('freesansbold.ttf', 25)
text_x = 10
text_y =10

# High score
highscore_font = pg.font.Font('freesansbold.ttf', 32)
hs_text_x = 950
hs_text_y = 10
# New score
newscore_text_x = 440
newscore_text_y = 300

# Game over
over_text = pg.font.Font('freesansbold.ttf', 72)

def show_score(x, y):
	score = font.render("Your Score: " + str(score_value), True, black)
	screen.blit(score, (x, y))
	
def high_score(hs_text_x, hs_text_y):
	filename = 'highscore.txt'
	with open(filename) as hs:
		try:
			highscore_value = int(hs.read())
		except:
			highscore_value = 0
	if score_value > highscore_value:
		highscore_value = score_value
		with open(filename, 'w') as obj:
			obj.write(str(score_value))		
	high_score_text = highscore_font.render("High Score: " + str(highscore_value), True, white)
	screen.blit(high_score_text, (hs_text_x, hs_text_y))	
	
###

def player(x, y):
	screen.blit(ship_img, (x, y))   # Draw the image loaded using blit().
	
def enemy(x, y, i):
	screen.blit(alien_img[i], (x, y))   # Draw the image loaded using blit().
	
def fire_bullet(x, y):
	global bullet_state
	bullet_state = "fire"            # Fire - bullet is currently in motion
	screen.blit(bullet_img, (x+16, y+10))
	
def isCollision(alien_x, alien_y, bullet_x, bullet_y):
	distance = math.sqrt((math.pow(alien_x - bullet_x, 2)) + (math.pow(alien_y - bullet_y, 2)))
	if distance < 27:
		return True
	else:
		return False
#Time
clock = pg.time.Clock()
# Game loop
game_run = True

while game_run:
	
	screen.fill(maroon)                       # Background first since all others are drawn upon it.
	screen.blit(bg, (0, 0))	                  # Space background
	
	for event in pg.event.get():              # Catches the events happening on the screen.
		if event.type == pg.QUIT:             # Closes the screen if close button is clicked.
			game_run = False
			
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_RIGHT:
				ship_x_change = 12
			if event.key == pg.K_LEFT:
				ship_x_change = -12
			if event.key == pg.K_SPACE:        # If SPACE is detected call fire_bullet()
				if bullet_state is "rest":
					bullet_sound = mixer.Sound("laser.wav")
					bullet_sound.set_volume(0.5)
					bullet_sound.play()
					bullet_x = ship_x
					fire_bullet(bullet_x, bullet_y)
				
		if event.type == pg.KEYUP:
			if event.key == pg.K_RIGHT:
				ship_x_change = 0
			if event.key == pg.K_LEFT:
				ship_x_change = 0
				

	# Checking for boundaries so that it doesn't cross the bounds.
	ship_x += ship_x_change
	
	if ship_x <= 0:
		ship_x = 0
		
	elif ship_x >= 1136:
		ship_x = 1136
	# Enemy movement	
	for i in range(num_of_alien):
		# Game over
		if alien_y[i] > 300:
			for j in range(num_of_alien):
				alien_y = 2000
			game_over_text()
			break
		alien_x[i] += alien_x_change[i]
	
		if alien_x[i] <= 0:
			alien_x_change[i] = 8
			alien_y[i] += alien_y_change[i]
		
		elif alien_x[i] >= 1136:
			alien_x_change[i] = -8
			alien_y[i] += alien_y_change[i]
			
		# Collision
		collision = isCollision(alien_x[i], alien_y[i], bullet_x, bullet_y)
		if collision:
			alien_sound = mixer.Sound("exp.wav")
			alien_sound.set_volume(0.4)
			alien_sound.play()
			bullet_y = 550
			bullet_state = "rest"
			score_value += 1
			alien_x[i] = rdm.randint(0,1135)                   # Coordinates of alien
			alien_y[i] = rdm.randint(50, 150)
			
		enemy(alien_x[i], alien_y[i], i)

			 
	# Bullet movement
	if bullet_y <= 0:
		bullet_y = 550
		bullet_state = "rest"
		
	if bullet_state is "fire":
		fire_bullet(bullet_x, bullet_y)
		bullet_y -= bullet_y_change
		
	player(ship_x, ship_y)
	show_score(text_x, text_y)
	high_score(hs_text_x, hs_text_y)
	pg.display.update()

