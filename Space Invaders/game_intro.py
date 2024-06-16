def game_intro():                                                       # For welcome screen
	intro = True                                                        
		
	while intro:
		screen.fill(maroon)	
		bbg = pg.image.load('bbgg.jpg')
		screen.blit(bbg, (0, 0))							
		intro_font = pg.font.Font('freesansbold.ttf',100)
		intro_text = intro_font.render("Space Invaders", True, yellow)
		screen.blit(intro_text, (250, 70))
		pg.draw.rect(screen, white, [400,210,400,400]) 		
				
		# buttons
		play_text = pg.font.Font('freesansbold.ttf', 20)
		play = play_text.render('PLAY', True, white)
		pg.draw.rect(screen, black, [550,510,100,50]) 
		screen.blit(play, (575, 525))
		close_text = pg.font.Font('freesansbold.ttf', 18)
		close = close_text.render('X', True, white)
		pg.draw.circle(screen, red, (1180, 20), 11)
		screen.blit(close, (1173, 11))
		# for settings  ---> pg.draw.circle(screen, green, (779, 189), 11)
		
		pg.display.update()
		
		for event in pg.event.get():
			if event.type == pg.QUIT:                                  # If window's qiut button clicked or not
				pg.quit()
				quit()
								
			if event.type == pg.MOUSEBUTTONDOWN:
				x,y = event.pos
				if x > 550 and x < 650 and y > 510 and y < 560:        # Play button clicked or not
					intro = False
				
				if x > 1169 and x < 1191 and y > 9 and y < 31:         # 'X' button clicked or not
					quit()
