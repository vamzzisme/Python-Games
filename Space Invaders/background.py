import pygame
import sys
import pygame.sprite as sprite

theClock = pygame.time.Clock()

background = pygame.image.load('bg.jpg')

background_size = background.get_size()
background_rect = background.get_rect()
screen = pygame.display.set_mode(background_size)
x = 0
y = 0
w,h = background_size
running = True

while running:
    screen.blit(background,background_rect)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if(y > h):
        y = 0
    else:
        y += 0.1
    screen.blit(background,(x,y))
    pygame.display.flip()
    pygame.display.update()
    theClock.tick(10)
