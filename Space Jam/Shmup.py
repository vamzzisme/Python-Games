# shmup prog smup = shoot 'em up
import pygame as pg
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

pg.init()    # initialize pygame
pg.mixer.init()            # initialize mixer

# screen dimensions
screen_width = 800
screen_height = 600
FPS = 60

# colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (150, 250, 120)
blue = (0, 0, 255)
yellow = (255, 255, 0)
orange = (255, 140, 0)
yellow = (255, 255, 0)
maroon = (128, 0, 0)
purple = (170, 128, 200)

# screen
screen = pg.display.set_mode((screen_width, screen_height))

# title
pg.display.set_caption("Shmup")

# clock
clock = pg.time.Clock()

font_name = pg.font.match_font('arial')                                  # match() ---> it gets the nearest match to the given font
def draw_text(surface, text, size, x, y, color):                                 # a function to write text
	font = pg.font.Font(font_name, size)
	text_surface = font.render(text, True, color)                      # True ---> for Anti-aliasing (check in internet for more)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)
	
def newmob():
		m = Mob()                   # create new mob if gets hit
		all_sprites.add(m)        # add to all_sprites group
		mobs.add(m)                    # add to mobs group
		
def draw_shieldbar(surface, x, y, prcnt):
	if prcnt < 0:
		prcnt = 0
	bar_length = 100
	bar_height = 10
	fill = (prcnt / 100) * bar_length             # filling color accordingly
	outline_rect = pg.Rect(x, y, bar_length, bar_height)
	fill_rect = pg.Rect(x, y, fill, bar_height)
	pg.draw.rect(surface, green, fill_rect)
	pg.draw.rect(surface, white, outline_rect, 2)           # 2 ---> border(thickness)

def draw_lives(surface, x, y, lives, img):
	for i in range(lives):
		img_rect = img.get_rect()
		img_rect.x = x + 30 * i
		img_rect.y = y
		surface.blit(img, img_rect)

# load all game graphics
background = pg.image.load(path.join(img_dir, "starfield.png")).convert() 
background_rect = background.get_rect()

player_img = pg.image.load(path.join(img_dir, "ship.png")).convert()
player_mini = pg.transform.scale(player_img, (25, 25))
player_mini.set_colorkey(black)

bullet_img = pg.image.load(path.join(img_dir, "bullet.png")).convert()

meteor_images = []         # for random sized meteors from the file
meteor_list = ['meteor.png','meteor1.png','meteor2.png','meteor3.png','meteor5.png','meteor6.png','meteor7.png','meteor8.png','meteor9.png']
for img in meteor_list:
	meteor_images.append(pg.image.load(path.join(img_dir, img)).convert())
	
explosion_anim = {}             # explosion dictionary
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []

for i in  range(8):
	filename = 'regularExplosion{}.png'.format(i)
	img = pg.image.load(path.join(img_dir, filename)).convert()
	img.set_colorkey(black)
	img_lg = pg.transform.scale(img, (75, 75))
	explosion_anim['lg'].append(img_lg)

	img_sm = pg.transform.scale(img, (32, 32))
	explosion_anim['sm'].append(img_sm)
	
	filename = 'sonicExplosion{}.png'.format(i)
	img = pg.image.load(path.join(img_dir, filename)).convert()
	img.set_colorkey(black)
	# img = pg.transform.scale(img, (75, 75))
	explosion_anim['player'].append(img)	
powerup_images = {}
#powerup_images['shield'] = pg.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pg.image.load(path.join(img_dir, 'bolt_gold.png')).convert()
powerup_images['healthU'] = pg.image.load(path.join(img_dir, 'pill_green.png')).convert()
powerup_images['healthD'] = pg.image.load(path.join(img_dir, 'pill_red.png')).convert()
	
# load all the game sounds
shoot_snd = pg.mixer.Sound(path.join(snd_dir, 'shoot.wav'))
green_snd = pg.mixer.Sound(path.join(snd_dir, "pow4.wav"))
power_snd = pg.mixer.Sound(path.join(snd_dir, "pow5.wav"))
exp_snd = pg.mixer.Sound(path.join(snd_dir, 'exp.wav'))
player_die_snd = pg.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))    
pg.mixer.music.load(path.join(snd_dir, 'bg.mp3')) 
pg.mixer.music.set_volume(0.2)           
# ---> for snd in ['exp3.wav', 'exp6.wav']:
# ------->exp_snds.append(pg.mixer.Sound(path.join(snd_dir, snd)))
pg.mixer.music.play(-1)                      # for continous play

# powerup time
powerup_time = 5000
class Player(pg.sprite.Sprite):                # player ---> ship
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.transform.scale(player_img, (50, 38))                     # to scale the graphic loaded
		self.image.set_colorkey(black)                                                  # to remove the black portion of the rected graphic
		# ---> self.image = pg.Surface((50, 40))
		# ---> self.image.fill(green)
		# for improved accurate collision
		self.rect = self.image.get_rect()
		self.radius = 20     # try experimenting
		# pg.draw.circle(self.image, red, self.rect.center, self.radius)             # just to check how the collision be like      
		self.rect.centerx = screen_width / 2
		self.rect.bottom = screen_height - 10
		self.x_speed = 0
		self.shield = 100                                 # health level
		self.shoot_delay = 250                          # for continous shoot of bullet when pressed SPACE
		self.last_shot = pg.time.get_ticks()
		self.lives = 3
		self.hidden = False
		self.hide_timer = pg.time.get_ticks()
		self.power = 1
		self.power_timer = pg.time.get_ticks()
		#self.protect = 1
		#self.protect_timer = pg.time.get_ticks()
		
	def update(self):
		# timeout for powerups
		if self.power >= 2 and pg.time.get_ticks() - self.power_timer > powerup_time:
			self.power -= 1 
			self.power_timer = pg.time.get_ticks()
		#if self.protect >= 2 and pg.time.get_ticks() - self.protect_timer > powerup_time:
			#self.protect -= 1
			#self.protect_timer = pg.time.get_ticks()
		
		# unhide if hidden
		if self.hidden and pg.time.get_ticks() - self.hide_timer > 1000:
			self.hidden = False
			self.rect.centerx = screen_width / 2
			self.rect.bottom = screen_height - 10
			
		self.x_speed = 0
		keystate = pg.key.get_pressed()    # list of all keys pressed
		if keystate[pg.K_LEFT]:
			self.x_speed = -8
		if keystate[pg.K_RIGHT]:                    # no need KEYUP event and all since in line 39 we set the speed to zero when updating in while loop
			self.x_speed = 8
		if keystate[pg.K_SPACE]:             # as long as u press space bar it shoots 
			self.shoot()
		
		self.rect.x += self.x_speed
		if self.rect.right > screen_width:
			self.rect.right = screen_width
		if self.rect.left < 0:
			self.rect.left = 0
	
	def powerup(self):
		self.power += 1
		self.power_timer = pg.time.get_ticks()
		
	# def protect(self):
		#self.protect = True
		#self.protect_timer = pg.time.get_ticks()
		#self.image = pg.image.load(path.join(img_dir, 'shield1.png')).convert()
		#self.image.set_colorkey(black)                                                  # to remove the black portion of the rected graphic				
		#self.rect = self.image.get_rect()
		#self.rect.top = player.rect.top
				
	def shoot(self):
		now = pg.time.get_ticks()           # for contimous shooting
		if now - self.last_shot > self.shoot_delay:
			self.last_shot = now
			if self.power == 1:
				bullet = Bullet(self.rect.centerx, self.rect.top)
				all_sprites.add(bullet)
				bullets.add(bullet)                 # add the bulet to the bullet list		
				shoot_snd.play()
			if self.power >= 2:
				bullet1 = Bullet(self.rect.left, self.rect.centery)
				bullet2 = Bullet(self.rect.right, self.rect.centery)	
				all_sprites.add(bullet1)
				all_sprites.add(bullet2)
				bullets.add(bullet1)
				bullets.add(bullet2)                 # add the bulet to the bullet list		
				shoot_snd.play()
								
	def hide(self):
		# temporarily hide
		self.hidden = True
		self.hide_timer = pg.time.get_ticks()
		self.rect.center = (screen_width / 2, screen_height + 200) 
				
class Mob(pg.sprite.Sprite):              # mob ---> alien
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image_original = random.choice(meteor_images)            # choose random img from the list                     
		self.image_original.set_colorkey(black)                               # to remove the black portion of the rected graphic		
		self.image = self.image_original.copy()                                                
		# ---> self.image = pg.Surface((40,30))
		# ---> self.image.fill(red)
		# for improved accurate collision
		self.rect = self.image.get_rect()
		self.radius = int(self.rect.width * 0.9 / 2)      # try experimenting
		# pg.draw.circle(self.image, red, self.rect.center, self.radius)		# just to check how the collision be
		self.rect.x = random.randrange(0, screen_width - self.rect.width)               # from 0 to given argumanet
		self.rect.y = random.randrange(-150, -100)
		self.speedy = random.randrange(1, 8)
		self.speedx = random.randrange(-3, 3)
		self.rot = 0                    # for ratation of meteor in degrees
		self.rot_speed = random.randrange(-8, 8)
		self.last_update = pg.time.get_ticks()

	def rotate(self):
		now = pg.time.get_ticks()
		if now - self.last_update > 50:
			self.last_update = now 
			self.rot = (self.rot + self.rot_speed) % 360            # to get back in quadrant 1 ---> ex: 361 degrees = 1 degree
			new_image = pg.transform.rotate(self.image_original, self.rot)
			# for improved rotation
			old_center = self.rect.center
			self.image = new_image
			self.rect = self.image.get_rect()
			self.rect.center = old_center                 
	
	def update(self):
		self.rotate()
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.top > screen_height + 10 or self.rect.left < -25 or self.rect.right > screen_width + 20:          # bottom boundary and left amd right
			self.rect.x = random.randrange(0, screen_width - self.rect.width)               # from 0 to given argumanet
			self.rect.y = random.randrange(-100, -40)
			self.speedy = random.randrange(1, 8)					

class Bullet(pg.sprite.Sprite):
	def __init__(self, x, y):
		pg.sprite.Sprite.__init__(self)
		self.image = bullet_img                             
		self.image.set_colorkey(black)                                                  # to remove the black portion of the rected graphic		
		# ---> self.image = pg.Surface((10,20))
		# ---> self.image.fill(yellow)   
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speed_y = -10
		
	def update(self):
		self.rect.y += self.speed_y
		# kill it if it goes of the top of screen
		if self.rect.bottom < 0:
			self.kill()              # kill ---> deletes the sprite from any of the group it may be present

class Powerups(pg.sprite.Sprite):
	def __init__(self, center):
		pg.sprite.Sprite.__init__(self)
		self.type = random.choice(['gun', 'healthU', 'healthD'])            # make sure u add 'shield' if u use the shield powerup
		self.image = powerup_images[self.type]                             
		self.image.set_colorkey(black)                                                  # to remove the black portion of the rected graphic		
		# ---> self.image = pg.Surface((10,20))
		# ---> self.image.fill(yellow)   
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.speed_y = 5
		
	def update(self):
		self.rect.y += self.speed_y
		# kill it if it goes of the top of screen
		if self.rect.top > screen_height:
			self.kill()              # kill ---> deletes the sprite from any of the group it may be present
		
class Explosion(pg.sprite.Sprite):
	def __init__(self, center, size):
		pg.sprite.Sprite.__init__(self)
		self.size = size
		self.image = explosion_anim[self.size][0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0                                          # frame----> the loaded explosion image
		self.last_update = pg.time.get_ticks()
		self.frame_rate = 50
		
	def update(self):
		now = pg.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explosion_anim[self.size]):
				self.kill()
			else:
				center = self.rect.center
				self.image = explosion_anim[self.size][self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center
				
all_sprites = pg.sprite.Group()  # sprite list
mobs = pg.sprite.Group()            # mob list
bullets = pg.sprite.Group()        # bullet list
powerups = pg.sprite.Group()          # powerup list

player = Player()
all_sprites.add(player)

number_of_mobs = 8
for i in range(number_of_mobs):
	newmob()

def game_intro_window():                                               # For intro screen
	intro = True                                                        	
	while intro:
		clock.tick(FPS)	
		screen.fill(maroon)	                                           # --> Not neseccesary <--
		intro_font = pg.font.Font('freesansbold.ttf',72)              # Font for intro_text
		intro_text = intro_font.render("Space Jam", True, yellow) # Render intro_text
		screen.blit(intro_text, (225, 120))                            # Draw the intro text
# if u wnt 	use -->	pg.draw.rect(screen, white, [400,210,400,400]) 	<---
		
		# buttons
		play_text_font = pg.font.Font('freesansbold.ttf', 20)          # Font for play_text
		play_text = play_text_font.render('PLAY', True, black)         # Render play_text
		pg.draw.rect(screen, white, [350,510,100,50])                  # Draw button for play_text
		screen.blit(play_text, (374, 526))                             # Draw rendered play_text
		close_text_font = pg.font.Font('freesansbold.ttf', 18)         # Font for close_text
		close_text = close_text_font.render('X', True, white)          # Render close_text
		pg.draw.circle(screen, red, (780, 20), 11)                    # Draw button for close_text
		screen.blit(close_text, (773, 11))                            # Draw the rendered close_text
		# pg.draw.circle(screen, green, (779, 229), 11)  if u 
		# settings = pg.image.load('settings.png')       want
		# screen.blit(settings, (771, 221))              use this settings
		
		pg.display.update()                                            # Display the drawn screen
		
		for event in pg.event.get():                                   # Ctch the vent happening on the screen
			if event.type == pg.QUIT:                                  # If window's quit button clicked or not
				pg.quit()
				quit()
				
			if event.type == pg.KEYDOWN:                               # Catch if a key is pressed on keyboard
				if event.key == pg.K_SPACE:                            # If SPACE is pressed continue to gameLoop
					intro = False
					
				if event.key == pg.K_ESCAPE:                           # If ESCAPE is pressed quit the game
					quit()
										
			if event.type == pg.MOUSEBUTTONDOWN:                       # Catch if a button is pressed on mouse
				x,y = event.pos                                        # Get the position of clicked place
				if x > 350 and x < 450 and y > 510 and y < 560:        # Check if play button clicked or not
					intro = False                                      # If play button is pressed continue to gameLoop
				
				if x > 769 and x < 791 and y > 9 and y < 31:         # Check if close button clicked or not
					pg.quit()                                             # if close button pressed quit the game
					quit()
					
			#	if x > 768 and x < 790 and y > 218 and y < 24: for settings

def game_over_window():
	game_over = True
	while game_over:
		pg.draw.rect(screen, green, [200, 110, 400, 400])              # For gameOver box
		pg.draw.rect(screen, black, [200, 110, 400, 400], 5)	       # border for gameover box
		over_text_font = pg.font.Font('freesansbold.ttf', 55)          # Font for over_text
		over_text = over_text_font.render("GAME OVER", True, black)    # Render the over_text
		screen.blit(over_text, (230, 140))                             # Draw the rendered over_text
		filename = 'highscore.txt'                                   
		with open(filename) as hs:                                     # Open highscore file
			try:
				highscore_value = int(hs.read())                       # Read the updated highscore
			except:
				highscore_value = 0	                                   # If no new score take ,== 0
		if str(score) == str(highscore_value):                   # if there is updated highscore
			draw_text(screen, "NEW HIGHSCORE !!", 32, 360, 200, purple)
			draw_text(screen, "High Score: " + str(highscore_value), 32, 315, 240, purple)
		else:
			draw_text(screen, "Your Score: " + str(score), 32, 325, 200, purple)
			draw_text(screen, "High Score: " + str(highscore_value), 32, 315, 240, purple)
						
		# rebuttons
		reclose_text_font = pg.font.Font('freesansbold.ttf', 18)       # Font for reclose_text
		reclose_text = reclose_text_font.render("Quit", True, white)   # Render reclose_text
		pg.draw.rect(screen, red, [350, 450, 100, 50])                 # Draw button for reclose text
		screen.blit(reclose_text, (379, 465))                               # Draw the rendered text
		pg.display.update()                                            # Update the newly drawn screen
		
		for event in pg.event.get():                                   # Catches the event happening on the screen
			if event.type == pg.QUIT:                                  # If window's qiut button clicked or not
				pg.quit()
				quit()
								
			if event.type == pg.MOUSEBUTTONDOWN:                       # Catches the button is it is pressed on mouse
				x,y = event.pos                                        # collects the position of clicked place
				if x > 350 and x < 450 and y > 450 and y < 500:        # 'X' button clicked or not
					quit()                                             # If 'X' is clicked quit game
					
			if event.type == pg.KEYDOWN:                               # Catches if the key pressed is on keyboard
				if event.key == pg.K_ESCAPE:                           # if key pressed is ESCAPE
					quit()                                             # Quit the game

game_intro_window()	
score = 0
# gameLoop
running = True
while running:
	# keep the loop running at the right speed
	clock.tick(FPS)

	# PROCESS INPUTS (EVENTS)
	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
		
		if event.type == pg.KEYDOWN:    
			if event.key == pg.K_ESCAPE:
				quit()
			
	# UPDATE
	all_sprites.update()
	
	# check the bullet hits the mob
	hits = pg.sprite.groupcollide(mobs, bullets, True, True)     # true ----> mob and bullet gets deleted
	for hit in hits:
		score += 50 - hit.radius                          # making the score different and worthing for different meteors ; greater the size lesser the points
		exp_snd.play()
		expl = Explosion(hit.rect.center, 'lg')
		all_sprites.add(expl)
		if random.random() > 0.7:                                           # to give random integer from 0 to 1
			powerup = Powerups(hit.rect.center)
			all_sprites.add(powerup)
			powerups.add(powerup)
		newmob()
	
	# check the collision of meteor and ship
	hits = pg.sprite.spritecollide(player, mobs, True, pg.sprite.collide_circle)        # checkfor sprite in player and sprite in mob; list of collision ; False --> no collision in the list if there comes a collision list becomes True and using if we make running False; collide_circle type of collision shape; True ----> disapper after colliding us
	for hit in hits:                                                               # hits is a list
		player.shield -= hit.radius * 2
		expl = Explosion(hit.rect.center, 'sm')
		all_sprites.add(expl)
		newmob()
		if player.shield <= 0:
			player_die_snd.play()
			death_explosion = Explosion(player.rect.center, 'player')               # explosion of player ship
			all_sprites.add(death_explosion)
			player.hide()
			player.lives -= 1
			player.shield = 100
	
	# check if collided with power up
	hits = pg.sprite.spritecollide(player, powerups, True)
	for hit in hits:
		if hit.type == 'healthU':
			player.shield += random.randrange(10, 30)
			green_snd.play()
			if player.shield >= 100:
				player.shield = 100
		if hit.type == 'healthD':
			player.shield -= 10
			if player.shield <= 0:
				player_die_snd.play()
				death_explosion = Explosion(player.rect.center, 'player')               # explosion of player ship
				all_sprites.add(death_explosion)
				player.hide()
				player.lives -= 1
				player.shield = 100	
		if hit.type == 'gun':
			player.powerup()
			power_snd.play()
		#if hit.type == 'shield':
			#player.protect()
	# if the player died and expl is finished
	if player.lives == 0 and not death_explosion.alive():                                                 # alive() ----> its is there 
		game_over_window()
		running = False
			
	# DRAW
	# ---> screen.fill(black)
	screen.blit(background, background_rect)
	all_sprites.draw(screen)
	draw_text(screen, str(score), 18, screen_width /2 , 10, white)
	draw_shieldbar(screen, 5, 5, player.shield)
	draw_lives(screen, screen_width - 100, 5, player.lives, player_mini)
	# *after* drawing everything , flip the display
	pg.display.flip()
pg.quit()	
