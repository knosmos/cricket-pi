import time
import pygame
from pygame.locals import *
from time import localtime
ahour = (localtime()[3]) % 24
aminute = (localtime()[4] + 5) % 60
def timeup(alarmhour,alarmmin):
    if localtime()[3] == alarmhour and localtime()[4] == alarmmin:
        return True
    else:
        return False
isOn = False 
clo = pygame.time.Clock()
def checktime():
    global ahour
    global aminute
    global isOn
    #zone.fill((100,0,100))
    #pygame.draw.rect(zone,(100,100,100),(10,10,50,50))
    pygame.init()
    z = pygame.display.set_mode((100,100))
    if timeup(ahour,aminute):
        return True
    a = pygame.key.get_pressed()
    if a[K_h]:
        ahour += 1
        if ahour > 24:
            ahour = 0
        print ahour
    elif a[K_m]:
        aminute += 1
        if aminute > 60:
            aminute = 0
        print aminute
    elif a[K_q]:
        pygame.quit()
    pygame.display.update()
    clo.tick(30)

def changetime(hour,minute):
    global ahour
    global aminute
    if hour:
        ahour += 1
        if ahour > 24:
            ahour = 0
    if minute:
        aminute += 1
        if aminute > 59:
            aminute = 0

def changetimeExt(hour, minute):
    global ahour
    global aminute
    ahour = (ahour + hour + 24) % 24
    aminute = (aminute + minute + 60) % 60

'''if __name__ == '__main__':
    while True:
        checktime()'''
