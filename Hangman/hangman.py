import pygame as pg
import random
import math

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREEN1 = (150, 250, 120)
YELLOW = (255, 255, 0)
ORANGE = (255, 140, 0)
MAROON = (128, 0, 0)
PURPLE = (170, 128, 200)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE

# game settings
TITLE = "Hangman!"
WIDTH = 1024
HEIGHT = 600

pg.init()    # initialize pygame

# screen
screen = pg.display.set_mode((WIDTH, HEIGHT))
# title
pg.display.set_caption(TITLE)


# data loading
images = []
for i in range(7):
	img = pg.image.load("hangman" + str(i) + ".png")
	images.append(img)

# main game variables 
hangman_now = 0
WORDS = ["PYTHON", "BANG", "MOVIE"]
word = random.choice(WORDS)
guessed = [""]

print(images)

# buttons
RADIUS = 30
GAP = 15
letters = []                                 # letter[x,y,"ltr",boolean]
X = round((WIDTH - (RADIUS * 2 + GAP) * 13 ) / 2)
Y = 450

# LETTER base
A = 65

for i in range(26):
	x = X + GAP * 2 + ((RADIUS * 2 + GAP) * ( i % 13))
	y = Y + ((i // 13) * (GAP + RADIUS * 2))
	letters.append([x, y, chr(A + i), True])

# font initialize
font = pg.font.SysFont('comicsans', 40)
wordfont = pg.font.SysFont('comicsans', 50)
titlefont = pg.font.SysFont('comicsans', 70)

def draw():
	screen.fill(WHITE)
	text = titlefont.render("HANGMAN!!", 1, BLACK)
	screen.blit(text, (WIDTH / 2 - text.get_width() / 2, 25))
	# draw word
	display_word = ""
	for letter in word:
		if letter in guessed:
			display_word += letter + " "
		else:
			display_word += "_ "
	text = wordfont.render(display_word, 1, BLACK)
	screen.blit(text, (450, 250))

	# drawing buttons
	for letter in letters:
		x, y, ltr, visible = letter
		if visible:
			pg.draw.circle(screen, BLACK, (x, y), RADIUS, 3)
			text = font.render(ltr, 1, BLACK)
			screen.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

	screen.blit(images[hangman_now], (150, 130))       
	pg.display.update()

def message(message):
	pg.time.delay(1000)	
	screen.fill(WHITE)
	text = wordfont.render(message, 1, BLACK)
	screen.blit(text, (WIDTH / 2 - text.get_width() / 2,HEIGHT / 2 - text.get_height() / 2 ))
	pg.display.update()
	pg.time.delay(4000)

def game():
	global hangman_now
	# clock
	clock = pg.time.Clock()      # to control rate of speed of game
	FPS = 60

	# gameLoop
	running = True
	while running:
		# keep the loop running at the right speed
		clock.tick(FPS)

		# PROCESS INPUTS (EVENTS)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False
			if event.type == pg.MOUSEBUTTONDOWN:
				mx, my = pg.mouse.get_pos()
				for letter in letters:
					x, y, ltr, visible = letter
					if visible:
						s = math.sqrt((x - mx) ** 2 + (y - my) ** 2)
						if s < RADIUS:
							letter[3] = False
							guessed.append(ltr)
							if ltr not in word:
								hangman_now += 1

		draw()

		win = True
		for letter in word:
			if letter not in guessed:
				win = False
				break

		if win:
			message("You Won!!")
			break

		if hangman_now == 6:
			message("You Lost!!")
			break

game()
pg.quit()