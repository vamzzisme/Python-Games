import pygame as pg
import time
from pygame import mixer

# global Colors
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)
blue = (0 ,0, 250)
teal =(0, 128, 128)
white = (255, 255, 255)
brown = (165, 42, 42)
orange = (255, 153, 31)
purple = (170, 128, 200)
maroon = (128, 0, 0)
yellow = (255, 255, 0)
# Variables
screen_width = 800
screen_height = 596

# Initialize pygame
pg.init()

# The screen and icon    
screen = pg.display.set_mode((screen_width, screen_height))                    # screen
pg.display.set_caption('Ping Pong')                                            # title
icon = pg.image.load('icon.png')                                               # icon
pg.display.set_icon(icon)     
bg = pg.image.load('bg.png')                                                   # background

# left bat
bat_a_img = pg.image.load('bat_a.png')
bat_a_x = 30
bat_a_y = 250
bat_a_y_change = 0

# right bat
bat_b_img = pg.image.load('bat_b.png')
bat_b_x = 750
bat_b_y = 250
bat_b_y_change = 0

# ball
ball_x = 410
ball_y = 305
ball_radius = 11
ball_x_change = 5
ball_y_change = 5

# scoring
score_a = 0
score_b = 0
score_font = pg.font.Font('freesansbold.ttf', 18)

#gameIntro
def game_intro_window():                                                       # for intro window
	bbg = pg.image.load('bbg.png')
	
	intro = True                                                        	
	while intro:
		screen.fill(black)                                                     # --> Not neseccesary <--
		screen.blit(bbg, (0, -20))
		intro_font = pg.font.Font('adistro.ttf',120)                           # Font for intro_text
		intro_text = intro_font.render("Pong Off...", True, yellow)            # Render intro_text
		screen.blit(intro_text, (180, 100))                                    # Draw the intro text
# if u wnt 	use -->	pg.draw.rect(screen, white, [400,210,400,400]) 	<---
		
		# buttons
		play_text_font = pg.font.Font('freesansbold.ttf', 20)                  # Font for play_text
		play_text = play_text_font.render('PLAY', True, black)                 # Render play_text
		pg.draw.rect(screen, green, [350,410,100,50])                          # Draw button for play_text
		screen.blit(play_text, (374, 426))                                     # Draw rendered play_text
		close_text_font = pg.font.Font('freesansbold.ttf', 15)                 # Font for close_text
		close_text = close_text_font.render('X', True, white)                  # Render close_text
		pg.draw.circle(screen, red, (785, 15), 9)                              # Draw button for close_text
		screen.blit(close_text, (779, 8))                                      # Draw the rendered close_text
		# pg.draw.circle(screen, green, (779, 229), 11)  
		# settings = pg.image.load('settings.png')       
		# screen.blit(settings, (771, 221))              
		
		pg.display.update()                                                    # Display the drawn screen
		
		for event in pg.event.get():                                           # Ctch the vent happening on the screen
			if event.type == pg.QUIT:                                          # If window's quit button clicked or not
				pg.quit()
				quit()
				
			if event.type == pg.KEYDOWN:                                       # Catch if a key is pressed on keyboard
				if event.key == pg.K_SPACE:                                    # If SPACE is pressed continue to gameLoop
					intro = False
					
				if event.key == pg.K_ESCAPE:                                   # If ESCAPE is pressed quit the game
					quit()
										
			if event.type == pg.MOUSEBUTTONDOWN:                               # Catch if a button is pressed on mouse
				x,y = event.pos                                                # Get the position of clicked place
				if x > 350 and x < 450 and y > 410 and y < 460:                # Check if play button clicked or not
					intro = False                                              # If play button is pressed continue to gameLoop
				
				if x > 776 and x < 794 and y > 6 and y < 24:                   # Check if close button clicked or not
					quit()                                                     # if close button pressed quit the game	

# gameOver
def game_over_window():
	# gbg = pg.image.load('gbg.png')
	game_over = True
	while game_over:
		pg.draw.rect(screen, purple, [200, 210, 400, 300])                     # For gameOver box
		pg.draw.rect(screen, black, [200, 210, 400, 300], 5)	               # border for gameover box
		over_text_font = pg.font.Font('freesansbold.ttf', 35)                  # Font for over_text
		if score_a == 10:
			score_a_text = over_text_font.render("Player A WINS!!!", True, maroon)
			screen.blit(score_a_text, (270, 240))                              # Draw the rendered over_text
			
		if score_b == 10:
			score_b_text = over_text_font.render("Player B WINS!!!", True, maroon)
			screen.blit(score_b_text, (270, 240))                              # Draw the rendered over_text			
					
		# rebuttons
		reclose_text_font = pg.font.Font('freesansbold.ttf', 18)               # Font for reclose_text
		reclose_text = reclose_text_font.render("Quit", True, white)           # Render reclose_text
		pg.draw.rect(screen, red, [350, 450, 100, 50])                         # Draw button for reclose text
		screen.blit(reclose_text, (379, 465))                                  # Draw the rendered text
		# screen.blit(gbg, (336, 316))
		# screen.blit(gbg, (400, 316))
		pg.display.update()                                                    # Update the newly drawn screen
		
		for event in pg.event.get():                                           # Catches the event happening on the screen
			if event.type == pg.QUIT:                                          # If window's quit button clicked or not
				pg.quit()
				quit()
								
			if event.type == pg.MOUSEBUTTONDOWN:                               # Catches the button is it is pressed on mouse
				x,y = event.pos                                                # collects the position of clicked place
				if x > 350 and x < 450 and y > 450 and y < 500:                # 'X' button clicked or not
					quit()                                                     # If 'X' is clicked quit game
					
			if event.type == pg.KEYDOWN:                                       # Catches if the key pressed is on keyboard
				if event.key == pg.K_ESCAPE:                                   # if key pressed is ESCAPE
					quit()                                                     # Quit the game											
game_intro_window()
# main loop
game_run = True
while game_run:
	screen.blit(bg, (0,0))                                                     # table background
	
	screen.blit(bat_a_img, (bat_a_x, bat_a_y))                                 # left bat
	screen.blit(bat_b_img, (bat_b_x, bat_b_y))                                 # right bat
	
	pg.draw.line(screen, white, (29, 40), (29, 570))                           # left out line
	pg.draw.line(screen, white, (772, 40), (772, 570))                         # right out line
	pg.draw.circle(screen, orange, (ball_x, ball_y), ball_radius)              # ball 
	
	close_text_font = pg.font.Font('freesansbold.ttf', 17)                     # Font for close text
	close_text = close_text_font.render('X', True, white)                      # Render the close_text
	pg.draw.circle(screen, red, (788, 325), 10)                                # button for close text
	screen.blit(close_text, (782, 317))                                        # Draw the rendered close text
	
	pause = pg.image.load('pause.png')	                                       # Load the image for pause
	screen.blit(pause, (776, 268))                                             # Draw the loaded pause image
			
	for event in pg.event.get():
		# window's QUIT button
		if event.type == pg.QUIT:
			game_run = False
		
		# quit and pause button	
		if event.type == pg.MOUSEBUTTONDOWN:                                   # Catches the button if pressed on mouse
			x,y = event.pos                                                    # Collects the position of clicked place
			if x > 778 and x < 798 and y > 315 and y < 335:                    # Check if 'X' button clicked or not
				game_run = False	                                           # Quit if pressed
			if x > 776 and x < 799 and y > 268 and y < 291:                    # Check if pause button is pressed or not
				pg.time.delay(6000)                                            #pause for 6000 milliseconds if pressed		
		
		# Bat movements and pause
		if event.type == pg.KEYDOWN:                                           # We have done many games like this just understand 
			if event.key == pg.K_w:
				bat_a_y_change = -15
			if event.key == pg.K_s:
				bat_a_y_change = 15
			if event.key == pg.K_SPACE:
				pg.time.delay(6000)
			if event.key == pg.K_UP:
				bat_b_y_change = -15
			if event.key == pg.K_DOWN:
				bat_b_y_change = 15
				
		if event.type == pg.KEYUP:
			if event.key == pg.K_w:
				bat_a_y_change = 0
			if event.key == pg.K_s:
				bat_a_y_change = 0
			if event.key == pg.K_UP:
				bat_b_y_change = 0
			if event.key == pg.K_DOWN:
				bat_b_y_change = 0
				
	bat_a_y += bat_a_y_change                                                  # line of code of bat_a movement
	bat_b_y += bat_b_y_change                                                  # line of code of bat_b movement
						
	# bat boundaries
	if bat_a_y > 466:                                                          # lower right boundary
		bat_a_y = 466          
	if bat_a_y < 0:                                                            # upper left boundary
		bat_a_y = 0
	if bat_b_y > 466:                                                          # lower right boundary
		bat_b_y = 466
	if bat_b_y < 0:                                                            # lower left boundary
		bat_b_y = 0	
		
	# Ball movements
	ball_x += ball_x_change                                                    # For continous movement we use '_change' concept
	ball_y += ball_y_change	
	
	# Ball boundaries on top and bottom												
	if ball_y + 11 > 596: 
		ball_y_change = -5
	if ball_y - 11 < 0:
		ball_y_change = 5
	
	# Check if ball and bat collided
	if ball_x + 11 > 750 and ball_x + 11 < 752 and ball_y + 11 > bat_b_y and ball_y - 11 < bat_b_y + 141:
		ball_x_change = -5                                                     # Draw and understand the coordinates
		mixer.music.load("pong_bounce.mp3")                                    # For background music
		mixer.music.set_volume(0.4)                                            # For volume control
		mixer.music.play()                                                     # play
	if ball_x - 11 > 45 and ball_x - 11 < 52 and ball_y + 11 > bat_a_y and ball_y - 11 < bat_a_y + 141:
		ball_x_change = 5                                                      # Draw and understand the coordinates
		mixer.music.load("pong_bounce.mp3")                                    # For background music
		mixer.music.set_volume(0.4)                                            # For volume control
		mixer.music.play()                                                     # play
		
	# Check if ball went out (left or right)
	if ball_x - 11 > 800:                                                      # If ball went out on right side
		ball_x = 410                                                           # Send the ball back to cente
		ball_y = 305
		score_a += 1                                                           # And add '1' to score_a
		mixer.music.load("bounce.wav")                                         # For background music
		mixer.music.set_volume(0.4)                                            # For volume control
		mixer.music.play()                                                     # play	
		pg.time.delay(1000)                                                    # stop for 1 second		
		
	if ball_x + 11 < 0:                                                        # If ball went out on left side
		ball_x = 410                                                           # Send back to centre
		ball_y = 305                      
		score_b += 1                                                           # And add '1' to score_b
		mixer.music.load("bounce.wav")                                         # For background music
		mixer.music.set_volume(0.4)                                            # For volume control
		mixer.music.play()                                                     # play
		pg.time.delay(1000)                                                    # stop for 1 second		
			
	score_text = score_font.render("Player A: " + str(score_a) + '     ' + "Player B: " + str(score_b), True, black) # Show score on screen
	screen.blit(score_text, (300, 10))
	
	# To check who is winner
	if score_a == 10:                                                          # First one to reach score of 10 is winner
		game_over_window()                                                     # call game_over_window
	elif score_b == 10:
		game_over_window()
		
	pg.display.update()
