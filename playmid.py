import sys
sys.path.insert(1, '/usr/lib/python2.7/dist-packages')
import pygame
from pygame.locals import *
print 'hello pygame'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('../twinkle_twinkle.mid')
pygame.mixer.music.play()
z = pygame.display.set_mode((300, 400))
isPause = False
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    	pressed = pygame.key.get_pressed()

    	if event.type == KEYDOWN:
            if event.key == K_q:
                pygame.quit()
                sys.exit()
	    elif event.key == K_p:
		if isPause == False:
                   pygame.mixer.music.pause()
                   isPause = True
                else:
                   pygame.mixer.music.unpause()
                   isPause = False
