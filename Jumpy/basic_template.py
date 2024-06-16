import pygame as pg
import random
from settings import *

pg.init()    # initialize pygame
pg.mixer.init()    # initialize sound module

# screen
screen = pg.display.set_mode((screen_width, screen_height))

# title
pg.display.set_caption("basic_for_all")

# clock
clock = pg.time.Clock()      # to control rate of speed of game

all_sprites = pg.sprite.Group()  # sprite list

# gameLoop
running = True
while running:
	# keep the loop running at the right speed
	clock.tick(FPS)

	# PROCESS INPUTS (EVENTS)
	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
			
	# UPDATE
	all_sprites.update()
	
	# draw
	screen.fill(white)        
	all_sprites.draw(screen)      # draw all sprites in the group
	# *after* drawing everything , flip the display
	pg.display.flip()
	
