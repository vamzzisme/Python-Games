import pygame as pg
import sys
import random

WIDTH = 700
HEIGHT = 512
FPS = 120

pg.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
icon = pg.image.load('img/favicon.ico').convert_alpha()
pg.display.set_icon(icon)

# font
game_font = pg.font.Font('z4f1.ttf', 40)
font = pg.font.Font('z4f1.ttf', 20)

# game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
highscore = 0

bg_surface = pg.image.load('img/background-day.png').convert()
floor_surface = pg.image.load('img/base.png').convert()
floor_x = 0

bird_downflap = pg.image.load('img/bluebird-downflap.png').convert_alpha()
bird_midflap = pg.image.load('img/bluebird-midflap.png').convert_alpha()
bird_upflap = pg.image.load('img/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, HEIGHT / 2))

BIRDFLAP = pg.USEREVENT + 1
pg.time.set_timer(BIRDFLAP, 200)

# bird_surface = pg.image.load('img/bluebird-midflap.png').convert_alpha()
# bird_rect = bird_surface.get_rect(center = (100, HEIGHT / 2))

pipe_surface = pg.image.load('img/pipe-green.png').convert()
pipe_list = []
SPAWNPIPE = pg.USEREVENT
pg.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [250, 180, 300, 310]

def move_floor():
	screen.blit(floor_surface, (floor_x, 410))
	screen.blit(floor_surface, (floor_x + WIDTH - 1, 410))                # -1 here because to cover the small gap of two blitted floors

def create_pipe():
	random_pipe_pos = random.choice(pipe_height)
	bottom_pipe = pipe_surface.get_rect(midtop = (1000, random_pipe_pos))
	top_pipe = pipe_surface.get_rect(midtop = (1000, random_pipe_pos - 550))
	return bottom_pipe, top_pipe

def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx -= 3
	return pipes

def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.bottom >= 512:
			screen.blit(pipe_surface, pipe)
		else:
			flip_pipe = pg.transform.flip(pipe_surface, False, True)
			screen.blit(flip_pipe, pipe)

def check_collision(pipes):
	for pipe in pipes:
		if bird_rect.colliderect(pipe):
			hit_snd.play()
			#lives -= 1 
			return False

	if bird_rect.top <= -10 or bird_rect.bottom >= 410:
		death_snd.play()
		return False

	return True

def rotate_bird(bird):
	new_bird = pg.transform.rotozoom(bird, -bird_movement * 3 , 1)
	return new_bird

def bird_animation():
	new_bird = bird_frames[bird_index]
	new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
	return new_bird, new_bird_rect

def score_display(game_state):
	if game_state == 'main_game':
		score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
		score_rect = score_surface.get_rect(center = (350, 50))
		screen.blit(score_surface, score_rect)
	if game_state == 'game_over':
		score_surface = game_font.render("Score: " + str(int(score)), True, (255, 255, 255))
		score_rect = score_surface.get_rect(center = (350, 30))
		screen.blit(score_surface, score_rect)

		highscore_surface = game_font.render("High score: " + str(int(highscore)), True, (255, 255, 255))
		highscore_rect = highscore_surface.get_rect(center = (350, 390))
		screen.blit(highscore_surface, highscore_rect)

		go_surface = font.render(("Press 'C' to play again"), True, (255, 255, 255))
		go_rect = go_surface.get_rect(center = (350, 250))
		screen.blit(go_surface, go_rect)

def updatescore(score, highscore):
	if score > highscore:
		highscore = score
	return highscore

game_over_surface = pg.image.load('img/gameover.png').convert_alpha()
game_overrect = game_over_surface.get_rect(center = (WIDTH / 2, HEIGHT / 2 - 50))

# sounds
flap_snd = pg.mixer.Sound('snd/wing.wav')
score_snd = pg.mixer.Sound('snd/point.wav')
death_snd = pg.mixer.Sound('snd/die.wav')
hit_snd = pg.mixer.Sound('snd/hit.wav')

game_title = pg.image.load('img/title.png').convert_alpha()

run = True
while run:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			sys.exit()
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_SPACE and game_active:
				bird_movement = 0
				bird_movement -= 5
				flap_snd.play()
			if event.key == pg.K_c and game_active == False:
				game_active = True
				pipe_list.clear()
				bird_rect.center = (100, HEIGHT / 2)
				bird_movement = 0
				score = 0

		if event.type == SPAWNPIPE:
			pipe_list.extend(create_pipe())

		if event.type == BIRDFLAP:
			if bird_index < 2:
				bird_index += 1
			else:
				bird_index = 0

			bird_surface, bird_rect = bird_animation()

	screen.blit(bg_surface, (0, 0))

	if game_active:
		# bird movement
		bird_movement += gravity
		rotated_bird = rotate_bird(bird_surface)
		bird_rect.centery += bird_movement
		screen.blit(rotated_bird, bird_rect)
		game_active = check_collision(pipe_list)

		for pipe in pipe_list:
			if pipe.centerx == 73:
				score_snd.play()
				score += 0.5

		# pipe movement
		pipe_list = move_pipes(pipe_list)
		draw_pipes(pipe_list)
		score_display('main_game')
	else:
		screen.blit(game_over_surface, game_overrect)
		highscore = updatescore(score, highscore)
		score_display('game_over')

	# floor movement
	floor_x -= 3
	move_floor()
	if floor_x <= -WIDTH:
		floor_x = 0
	pg.display.update()
	clock.tick(FPS)