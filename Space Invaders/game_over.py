def game_over():
	game_over = True
	while game_over:
		pg.draw.rect(screen, white, [400,210,400,400]) 
		pg.draw.rect(screen, black, [400, 210, 400, 400], 5)					
		over_text_font = pg.font.Font('freesansbold.ttf', 30)
		over_text = over_text_font.render("GAME OVER", True, white)
		screen.blit(over_text, (550, 250))							
	
				
		# buttons
		regame_text = pg.font.Font('freesansbold.ttf', 20)
		regame = regame_text.render('Play Again', True, black)
		pg.draw.rect(screen, black, [550,510,100,50]) 
		screen.blit(regame, (575, 525))
		reclose_text = pg.font.Font('freesansbold.ttf', 18)
		reclose = reclose_text.render('Quit', True, white)
		pg.draw.rect(screen, red, [550, 450, 100, 50])
		screen.blit(close, (575, 465))
		pg.display.update()
		
		for event in pg.event.get():
			if event.type == pg.QUIT:                                  # If window's qiut button clicked or not
				pg.quit()
				quit()
								
			if event.type == pg.MOUSEBUTTONDOWN:
				x,y = event.pos
				if x > 550 and x < 650 and y > 510 and y < 560:        # Play button clicked or not
					game_run = True
				
				if x > 550 and x < 650 and y > 450 and y < 500:         # 'X' button clicked or not
					quit()	
