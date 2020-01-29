import pygame, sys, random
from pygame.locals import *
#from Queue import Queue
from threading import Thread
#import pygame.midi
import time
import midi_play
#import ticky
#pygame.mixer.init()
#pygame.midi.init()
import Clocki
import subprocess
#import speechrec
import snowboythreaded
import signal
import gcpspeechthreaded
import os
import sys

        
use_speech = True
use_google_speech = False
stop_program = False
org_play_speed = 0
#idle_time = 0

def signal_handler(signal, frame):
    global stop_program
    stop_program = True

#signal.signal(signal.SIGINT, signal_handler)


def load_model_list(listFName):
    models = []
    with open(listFName) as fpIn:
        for line in fpIn:
	    if 'pmdl' in line:
                 models.append(line.rstrip())

    return models

def my_callback(idx, hotword):
    print 'Hotword #%d [%s] Detected!' % (idx, hotword)

def my_callback2(idx):
    print 'My Hotword #%d Detected!' % (idx)

def gcpspeech_main(listFName):
    models = load_model_list(listFName)
    print 'models = ', models
    time.sleep(1)

    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    #sensitivities = [0.5]*len(models)
    sensitivities = [0.55, 0.6]
    print('Listening... Press Ctrl+C to exit')
    threaded_detector = gcpspeechthreaded.ThreadedDetector(models, sensitivity=sensitivities)
    threaded_detector.start()
    threaded_detector.start_recog(sleep_time = 0.03)
    time.sleep(1)
    return threaded_detector

def speechrec_main(listFName):
  models = load_model_list(listFName)
  print 'models = ', models
  time.sleep(1)

  # capture SIGINT signal, e.g., Ctrl+C
  signal.signal(signal.SIGINT, signal_handler)

  sensitivities = [0.55]*len(models)
  sensitivities[4:8] = [0.45]*4
  sensitivities[8:10] = [0.6]*2
  #detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
  callbacks = [lambda: my_callback(0, models[0]),
             lambda: my_callback(1, models[1]),
             lambda: midi_play.Replaypress(),#2
             lambda: midi_play.Replaypress(),#3
             lambda: midi_play.Pausepress(), #4
             lambda: midi_play.Pausepress(), #5
             lambda: midi_play.Pausepress(), #6
             lambda: midi_play.Pausepress(), #7
             lambda: midi_play.Fastpress(), #8
             lambda: midi_play.Fastpress(), #9
             lambda: midi_play.Slowpress(), #10
             lambda: midi_play.Slowpress(), #11
             lambda: midi_play.Loudpress(), #12
             lambda: midi_play.Loudpress(), #13
             lambda: midi_play.Softpress(), #14
             lambda: midi_play.Softpress(), #15
             lambda: midi_play.Metropress2(), #16
             lambda: midi_play.Metropress2(), #17
             lambda: midi_play.Endpress(), #18
             lambda: midi_play.Endpress()] #19
  print('Listening... Press Ctrl+C to exit')
  threaded_detector = snowboythreaded.ThreadedDetector(models, callbacks, sensitivity=sensitivities)
  threaded_detector.start()
  threaded_detector.start_recog(sleep_time = 0.03)
  time.sleep(1)
  return threaded_detector

#def setVolume(vol):
  #print 'Set the Volume to %d%%' % vol
  #subprocess.call(['amixer', 'cset', 'numid=4', '%d%%' % (vol)]

def click(RECT, x, y):
    if RECT.collidepoint(x, y) == True:
        return True

def loadMusic(filename):
    listname = []
    with open(filename, 'rU') as f:
        for line in f:
            if '.mid' in line or '.MID' in line:
                listname.append(line.rstrip())
    midi_play.lastsong = listname[0]
    return listname

def drawnotes(listname, screen, note):
    for x in listname:
        screen.blit(note,(x[0], x[1]))
        x[0] += x[2]
        x[1] += x[3]
def drawsignal(listname, screen, signal, signal2,height,width):
    for x in listname:
        screen.blit(signal, (x, height*0.45))
        screen.blit(signal2,(width - x, height*0.45))

def main():
    global use_google_speech
    global use_speech

    initGUI = True # quick way to make sure everything is in right scale at the beginning

    if len(sys.argv) >= 2:
        if sys.argv[1] == 'gcp':
            use_google_speech = True
            gcpspeechthreaded.using_google_cloud_speech = True
        elif sys.argv[1] == 'google':
            use_google_speech = True
            gcpspeechthreaded.using_google_cloud_speech = False
        elif sys.argv[1] == 'snowboy':
            use_google_speech = False
        elif sys.argv[1] == 'no_speech':
            use_speech = False

    midiplay_thread = Thread(target = midi_play.midiPlay)
    midiplay_thread.daemon = True
    midiplay_thread.start()
    midi_play.setVolume(90)
    '''metronome_thread = Thread(target = ticky.beat)
    metronome_thread.daemon = True
    metronome_thread.start()'''
    beetbug_main_thread = Thread(target = midi_play.beetbug_main)
    beetbug_main_thread.daemon = True
    beetbug_main_thread.start()
    voiceline = Thread(target = midi_play.voicelineControl)
    voiceline.daemon = True
    voiceline.start()
    pygame.init()
    width = 1000
    height = 700
    DISPLAYSURF = pygame.display.set_mode((width, height),pygame.RESIZABLE)
    musicNote = pygame.image.load('musicnote.png')
    musicNote = pygame.transform.scale(musicNote, (20,20))      
    pygame.display.set_icon(musicNote)
    pygame.display.set_caption('Cricket Pi v3.2')
    splash = pygame.transform.scale(pygame.image.load('Splash_Screen_CricketPi.png'),(width,height))
    DISPLAYSURF.blit(splash,(0,0))
    pygame.display.update()
    BLACK = (0,0,0)
    WHITE = (255, 255, 255, 80)
    RED = (255, 100, 100, 80)
    MANGO = (220,200,50)
    GREEN = (50, 255, 50, 80)
    BLUE = (100, 100, 255, 80)
    SILVER = (100, 100, 100, 80)
    AQUA = (50, 255, 255, 80)
    FUCHSIA = (255, 100, 255, 80)
    TAN = (100, 100, 60, 80)
    DarkFuchsia = (200,0,200)
    VeryDarkFuchsia = (50, 0, 50)
    BACKGROUND = (0,0,0)
    MIDNIGHT = (153,155,216)
    MINT = (78,232,180)
    GREY = (30,20,10)
    COLOR = [FUCHSIA,FUCHSIA,FUCHSIA,FUCHSIA]
    COLOR2  = [BLUE,BLUE,BLUE,BLUE,BLUE]
    COLOR3 = [MANGO,MANGO]
    colorScheme = 'Default'
    buttonRects = [
    #play
        pygame.Rect(50,80,70,25),
    #pause
        pygame.Rect(175, 80, 70, 25),
    #resume
        pygame.Rect(300, 80, 70, 25),
    #stop
        pygame.Rect(425, 80, 70, 25)
    ]
    buttonlist = ['play', 'pause', 'resume', 'stop']
    
    '''buttonRects2 = [
    #faster
        pygame.Rect(50,310,70,25),
    #slower
        pygame.Rect(130,310,70,25),
    #louder
        pygame.Rect(210, 310, 70, 25),
    #softer
        pygame.Rect(290, 310, 70, 25),
    #loop
        pygame.Rect(370, 310, 70, 25)
    ]'''
    blist2 = ['faster', 'slower', 'louder', 'softer', 'loop']

    ''' buttonRects3 = [
        #metronome
        pygame.Rect(450,55,70,20),
        #clock
        pygame.Rect(450,135,70,20)
    ]'''
    blist3 = ['Metronome', 'Alarm']
    metromidi = ['m440.mid','m441.mid','m442.mid','m443.mid','m444.mid','m445.mid','m446.mid']
    currentmetro = 0
    metronomeOn = False
    settings = pygame.Rect(520,320,70,25)
    playlist = pygame.Rect(10,115,100,200)
    #ButtonFont = pygame.font.SysFont(None, 20)
    #SensorFont = pygame.font.SysFont(None,25)
    #TitleFont = pygame.font.SysFont(None, 40)

    ButtonFont = pygame.font.SysFont(None, int(round(width*0.025)))  
    TitleFont = pygame.font.SysFont(None, int(round(width*0.08)))
    SensorFont = pygame.font.SysFont(None, int(round(width*0.05)))

    '''def makeList(width,listlength,y):
        newList = []
        for item in range(listlength):
            xpos = 50 + item * (width-200)/len(listlength)
            newList.append(pygame.Rect(xpos,y,70,25))
        return newList
    buttonRow1 = makeList(width,4,80)'''
    #button'''
    '''def drawButton(buttonlist,y,mx,my,colorlist,ncol,ccol):
        for item in range(len(buttonlist)):
            if click(item, mx, my) == True:
                colorlist[item] = ccol
            else:
                colorlist[item] = ncol               
            xpos = 55 + item * (width-200)/len(buttonlist)
            pygame.draw.ellipse(DISPLAYSURF, colorlist[item], (xpos-5, y, 70, 25))
            Print = ButtonFont.render(buttonlist[item], 1, VeryDarkFuchsia)
            DISPLAYSURF.blit(Print, (xpos, 85))'''

    musicNote = pygame.image.load('musicnote.png')
    musicNote = pygame.transform.scale(musicNote, (32,32))

    ''' Logo '''
    logo = pygame.image.load('logo.png')
    logoReg = pygame.transform.scale(logo, (120,120))
    logoLg = pygame.transform.scale(logo, (150,150))
    logoSz = logoReg

    signal = pygame.image.load('signal.png')
    signal = pygame.transform.scale(signal, (40,50))
    signal2 = pygame.image.load('signal2.png')
    signal2 = pygame.transform.scale(signal2, (40,50))

    '''musicnotes and signals'''
    musicnotes = []
    signals = []
    MAKENOTE = 26
    pygame.time.set_timer(MAKENOTE, 1000)  


    ''' Music Tempo '''
    MusicList = []
    musicShow = []
    #pygame.mixer.pre_init(44100, -16, 2, 2048)
    #popSound = pygame.mixer.Sound('pop.wav') 
    #alarm = pygame.mixer.Sound('boxing_bell.wav')
    fpsClock = pygame.time.Clock()
    tempo = 60
    Tempobeat = 25
    pygame.time.set_timer(Tempobeat,60000/tempo)
    #volume = 100
    '''''''images'''''''


    ''' Logo '''
    logo = pygame.image.load('logo.png')
    logoReg = pygame.transform.scale(logo, (120,120))
    logoLg = pygame.transform.scale(logo, (150,150))
    logoSz = logoReg
    logoRegWidth = 120
    logoLgWidth = 150

    signal = pygame.image.load('signal.png')
    signal = pygame.transform.scale(signal, (40,50))
    signal2 = pygame.image.load('signal2.png')
    signal2 = pygame.transform.scale(signal2, (40,50))

    '''musicnotes and signals'''
    musicnotes = []
    signals = []
    MAKENOTE = 26
    pygame.time.set_timer(MAKENOTE, 1000)

    #load music in Songlist file
    MusicList = loadMusic('Songlist.txt')
    if len(MusicList) > 9:
        for x in range(9):
            musicShow.append(MusicList[x])
    else:
        musicShow = MusicList

    scroll = pygame.Rect(10,155,30,40)
    showstart = 0
    playing = False
    listPos = []
    clock = False
    beat = 27
    #pygame.time.set_timer(beat, 60000/ticky.bpm)
    for pos in range(0,len(musicShow)):
        Ypos = height*0.3 + pos*21
        listPos.append(pygame.Rect(width*0.08,Ypos,70,20))


    if use_speech:
        if use_google_speech:
            threaded_detector = gcpspeech_main('HeyCricket.lst')
        else:
            threaded_detector = speechrec_main('CricketHotwords.lst')
    else:
        print '*** SPEECH RECOGNITION TURNED OFF ***'

    print 'Entering the pygame Loop'

    global stop_program
    global org_play_speed

    arcstart = 0
    while not stop_program:
        #find mouse coordinates
        #make cricket go to sleep if cricket has been idle for 2000 frames        
        x, y = pygame.mouse.get_pos()
        midi_play.idle_time += 1
        DISPLAYSURF.fill(BACKGROUND)
        Print = TitleFont.render("CRICKET PI", 40, WHITE)
        DISPLAYSURF.blit(Print, (40,20))

        '''DRAW BUTTONS'''
        for item in range(len(buttonlist)):
            xpos = 55 + item * (width-200)/len(buttonlist) - width*0.008     
            ypos = height*0.2 - width*0.008    
            buttonwidth = width*0.1
            buttonheight = height*0.05   
            if click(pygame.Rect(xpos,ypos,buttonwidth,buttonheight), x, y) == True:
                COLOR[item] = DarkFuchsia
            else:
                COLOR[item] = FUCHSIA
            pygame.draw.ellipse(DISPLAYSURF, COLOR[item], (xpos, ypos, buttonwidth, buttonheight))
            Print = ButtonFont.render(buttonlist[item], 1, VeryDarkFuchsia)
            DISPLAYSURF.blit(Print, (xpos + width*0.02, ypos + width*0.008))

        '''for item in range(len(blist2)):
            if click(buttonRects2[item], x, y) == True:
                COLOR2[item] = AQUA
            else:
                COLOR2[item] = BLUE
            xpos = 55 + item * (width-150)/len(blist2)
            pygame.draw.ellipse(DISPLAYSURF, COLOR2[item], (xpos-width*0.008, height*0.8 - 5, width*0.1, height*0.05))
            Print = ButtonFont.render(blist2[item], 1, VeryDarkFuchsia)
            DISPLAYSURF.blit(Print, (xpos, height*0.8))'''
        for item in range(len(blist2)):
            ypos = height*0.8
            buttonwidth = width*0.1
            buttonheight = height*0.05
            xpos = 55 + item * (width-150)/len(blist2)
            if click(pygame.Rect(xpos,ypos,buttonwidth,buttonheight),x,y) == True:
                COLOR2[item] = AQUA
            else:
                COLOR2[item] = BLUE
            pygame.draw.ellipse(DISPLAYSURF,COLOR2[item], (xpos - width*0.01,ypos - width*0.008,buttonwidth,buttonheight))
            Print = ButtonFont.render(blist2[item],1,VeryDarkFuchsia)
            DISPLAYSURF.blit(Print,(xpos,ypos))

        '''fix for bug in metronome'''
        if midi_play.song not in metromidi:
            midi_play.metronomeOn = False
        ''''''''''''''''''''''''''''''

        for item in range(len(blist3)):
            ypos = 55 + item * height * 0.2
            xpos = width*0.8-5
            buttonwidth = width*0.14
            buttonheight = height*0.05
            pygame.draw.ellipse(DISPLAYSURF, COLOR3[item], (xpos,ypos-5, buttonwidth, buttonheight))
            Print = ButtonFont.render(blist3[item], 1, VeryDarkFuchsia)
            #DISPLAYSURF.blit(Print, (width*0.8,ypos))
            DISPLAYSURF.blit(Print, (xpos + width * 0.02,ypos + height * 0.008))
            if click(pygame.Rect(xpos,ypos,buttonwidth,buttonheight), x, y) == True:
                COLOR3[item] = RED
            else:
                COLOR3[item] = MANGO
            if blist3[item] == 'Metronome':
                Print = SensorFont.render(midi_play.metromidi[midi_play.currentmetro].replace('.mid','').replace('m','m-'),1,RED)
                DISPLAYSURF.blit(Print,(width*0.8,ypos + height*0.05)) 
                pygame.draw.ellipse(DISPLAYSURF,BLUE,(width*0.9,ypos+height*0.05,width/30,height/20))

                if midi_play.metronomeOn == True:
                    Print = SensorFont.render('On', 1, MANGO)
                    DISPLAYSURF.blit(Print, (width*0.94, ypos))


                    
                else:
                    Print = SensorFont.render('Off', 1, MANGO)
                    DISPLAYSURF.blit(Print, (width*0.94, ypos))
            else:
                if clock == True:
                    Print = SensorFont.render('On',1,MANGO)

                else:
                    Print = SensorFont.render('Off',1,MANGO)
                DISPLAYSURF.blit(Print,(width*0.94,ypos))
                if Clocki.aminute > 9:
                    dismin = str(Clocki.aminute)
                else:
                    dismin = '0' + str(Clocki.aminute)

                Print = SensorFont.render(str(Clocki.ahour) + ' : ' + dismin,1,RED)
                DISPLAYSURF.blit(Print,(width*0.8,ypos + height*0.05))                    
        if click(settings, x, y) == True:
            pygame.draw.ellipse(DISPLAYSURF,(50,50,100),settings)
        else:
            pygame.draw.ellipse(DISPLAYSURF,(100,100,150),settings)
        Print = ButtonFont.render('exit',1,WHITE)
        settings.topleft = (width-105,height-80)
        DISPLAYSURF.blit(Print, (width-100,height-75))
        #pygame.draw.ellipse(DISPLAYSURF,MANGO,)
        if click(buttonRects[0], x, y) == True or click(playlist, x, y) == True:
            for item in range(len(musicShow)):
                Print = ButtonFont.render(musicShow[item], 1, WHITE)
                DISPLAYSURF.blit(Print, listPos[item])
            if len(MusicList) > 9:    
                pygame.draw.polygon(DISPLAYSURF,SILVER,(scroll.topleft,(scroll.centerx,scroll.bottom),scroll.topright))
        #draw notes
        drawnotes(musicnotes, DISPLAYSURF, musicNote)
        if len(musicnotes) > 20:
            musicnotes.pop(1)
        #draw icon arcs
        arcradius = width*0.1
        arcstart += 0.02
        pygame.draw.arc(DISPLAYSURF, MIDNIGHT, (width/2 - arcradius,height/2 - arcradius,arcradius*2,arcradius*2),arcstart,arcstart + 1,7)
        pygame.draw.arc(DISPLAYSURF, MIDNIGHT, (width/2 - arcradius,height/2 - arcradius,arcradius*2,arcradius*2),arcstart + 1.6,arcstart + 2.6,7)
        pygame.draw.arc(DISPLAYSURF, MIDNIGHT, (width/2 - arcradius,height/2 - arcradius,arcradius*2,arcradius*2),arcstart + 3.2,arcstart + 4.2,7)
        pygame.draw.arc(DISPLAYSURF, MIDNIGHT, (width/2 - arcradius,height/2 - arcradius,arcradius*2,arcradius*2),arcstart + 4.8,arcstart+5.8,7)

        #draw logo icon
        if logoSz == logoReg:
            DISPLAYSURF.blit(logoSz, ((width - logoRegWidth)/2, (height - logoRegWidth)/2))
        else:
            DISPLAYSURF.blit(logoSz, ((width - logoLgWidth)/2, (height - logoLgWidth)/2))

        #draw voice ring
        ringradius = int(round(width/7))
        if midi_play.running_command:
            ringcol = MINT
        elif gcpspeechthreaded.voice_on:
            ringcol = RED
        else:
            ringcol = MIDNIGHT
        pygame.draw.circle(DISPLAYSURF,ringcol,(width/2,height/2),ringradius,10)
        #draw signal waves
        
        drawsignal(signals, DISPLAYSURF, signal, signal2,height,width)
        #Take care of the alarm
        if not Clocki.timeup(Clocki.ahour,Clocki.aminute):
            if midi_play.song == 'wt.mid':
               midi_play.Endpress()
               if org_play_speed > 0:
                    midi_play.speed = org_play_speed
                    org_play_speed = 0
                    break
        if Clocki.timeup(Clocki.ahour,Clocki.aminute) and clock == True:
            if org_play_speed == 0:
                org_play_speed = midi_play.speed
                midi_play.speed = 1.0
            #midi_play.speed = 1.0 
            midi_play.song = 'wt.mid'
            midi_play.loop = False
            DISPLAYSURF.fill(WHITE)
            Print = TitleFont.render('T minus zero',1,BLACK)
            DISPLAYSURF.blit(Print,(50,50))
            Print = SensorFont.render("It's time to practice!",1,BLACK)
            DISPLAYSURF.blit(Print,(50,300))
            pygame.display.update()
            for x in range(10):
                time.sleep(1.0)
                midi_play.Fastpress()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        midi_play.song = ''
                        clock = False
                        midi_play.loop = False
                        break
                if clock == False:
                    midi_play.speed = org_play_speed
                    org_play_speed = 0
                    break


        #draw volume, Tempo, loop, metronome, and clock values
        Print = SensorFont.render('Volume: ' + str(midi_play.volume), 1, MANGO)
        DISPLAYSURF.blit(Print, (width*0.35,height*0.875))
        Print = SensorFont.render('Speed: ' + str(midi_play.speed) + 'x', 1, MANGO)
        DISPLAYSURF.blit(Print, (width*0.08,height*0.875))
        if midi_play.loop == False:
            Print = SensorFont.render('Loop Off', 1, MANGO)
        else:
            Print = SensorFont.render('Loop On',1, MANGO)
        DISPLAYSURF.blit(Print, (width*0.68,height*0.875))
        if midi_play.song !='':
            Print = SensorFont.render('Velocity: ' + str(midi_play.loudness),1,MANGO)
            DISPLAYSURF.blit(Print,(width*0.57,height*0.05))
        if playing is True:
            Print = SensorFont.render(midi_play.song,1,MANGO)
            DISPLAYSURF.blit(Print, (width*0.6,height*0.7))
        for item in range(len(signals)):
            signals[item] -= 2
        if len(signals) > 10:
            signals.pop(0)
        pressed = pygame.key.get_pressed()
        if pressed[K_q]:
            stop_program = True
            threaded_detector.terminate()
            pygame.quit()
            sys.exit()
            break
        if pressed[K_h]:
            #Clocki.changetime(True,False)
            Clocki.changetimeExt(1,0)
            time.sleep(0.1)
        if pressed[K_l]:
            Clocki.changetimeExt(-1,0)
            time.sleep(0.1)
        if pressed[K_m] or pressed[K_j]:
            #Clocki.changetime(False,True)
            Clocki.changetimeExt(0,1)
            time.sleep(0.1)
        if pressed[K_k]:
            #Clocki.changetime(False,True)
            Clocki.changetimeExt(0,-1)
            time.sleep(0.1)
        if pressed[K_e]:
            BACKGROUND = MANGO
            blist2 = ['mango','mango','mango','mango','mango']
            buttonlist = ['mango','mango','mango','mango']
        #if pressed[K_l]:
        #    width += 10
        #    DISPLAYSURF = pygame.display.set_mode((width,height))
        #if pressed[K_n]:
        #    width -= 10
        #    DISPLAYSURF = pygame.display.set_mode((width,height))
        #if pressed[K_t]:
        #    height += 10
        #    DISPLAYSURF = pygame.display.set_mode((width,height))
        #if pressed[K_s]:
        #    height -= 10
        #    DISPLAYSURF = pygame.display.set_mode((width,height))
        if pressed[K_b]:
            '''currentmetro+=1
            if currentmetro>len(metromidi)-1:
                currentmetro = 0
            if metronomeOn == True:
                midi_play.song = ''
                time.sleep(0.05)
                midi_play.song = metromidi[currentmetro]'''
            midi_play.Changebeat()
        if midi_play.noteon:
            logoSz = logoLg
        else:
            logoSz = logoReg     
        for event in pygame.event.get():
            if event.type == QUIT:
                stop_program = True
                threaded_detector.terminate()
                pygame.quit()
                sys.exit()
            if event.type == MAKENOTE:
                musicnotes.append([width/2,height/2,random.randint(-10,10),random.randint(-10,10)])
                if midi_play.song != '' and not midi_play.metronomeOn and not midi_play.paused:
                    for x in range(7):
                        musicnotes.append([width/2,height/2,random.randint(-10,10),random.randint(-10,10)])


            if event.type == beat:
                signals.append(width*0.46)
                #if metro == True:
                 #   ding.play:()wwww
            '''
            if event.type == Tempobeat:
                if logoSz == logoReg:
                    logoSz = logoLg
                else:
                    logoSz = logoReg  
            '''
            if event.type == pygame.MOUSEBUTTONDOWN:
                #popSound.play()
                for item in range(len(musicShow)):
                    if click(listPos[item], x, y) == True:
                        print musicShow[item]
                        midi_play.song = musicShow[item]
                        playing = True
		#SCROLL
                if click(scroll, x, y) == True and musicShow != MusicList:
                    if showstart == len(MusicList) - 9:
                        showstart = -1
                    showstart += 1                        
                    musicShow = []
                    for x in range(showstart,showstart+9):

                        musicShow.append(MusicList[x]) 
                elif click(settings, x, y) == True:
                    stop_program = True
                    threaded_detector.terminate()
                    pygame.quit()
                    sys.exit()

                for item in range(len(buttonlist)):
                    buttonwidth = width*0.1
                    buttonheight = height*0.05
                    xpos = 55 + item * (width-150)/len(buttonlist) - width*0.008
                    ypos = height * 0.2 - width*0.008
                    if click(pygame.Rect(xpos,ypos,buttonwidth,buttonheight),x,y) == True:
                        if buttonlist[item] == 'play':
                            midi_play.Replaypress()
                        elif buttonlist[item] == 'pause':
                            if midi_play.paused == False:
                                print 'paused'
                                playing = False
                                midi_play.paused = True
                        elif buttonlist[item] == 'resume':
                            if midi_play.paused == True:
                                print 'resumed'
                                playing = True
                                midi_play.paused = False
                        elif buttonlist[item] == 'stop':
                            midi_play.song = ''
                            playing = False                                            
                for item in range(len(blist2)):
                    ypos = height*0.8 - 5
                    buttonwidth = width*0.1
                    buttonheight = height*0.05
                    xpos = 55 + item * (width-150)/len(blist2) - width*0.008
                    if click(pygame.Rect(xpos,ypos,buttonwidth,buttonheight),x,y) == True:
                        if blist2[item] == 'faster':
                            midi_play.Fastpress()
                        #if blist2[item] == 'faster' and midi_play.speed < 10:
                        #    midi_play.speed += 0.1
                        #    tempo += 10
                            #pygame.time.set_timer(Tempobeat,60000/tempo)
                             
                        #elif blist2[item] == 'slower' and midi_play.speed > 0.1:
                        elif blist2[item] == 'slower':
                            midi_play.Slowpress()
                            #midi_play.speed -= 0.1
                            #tempo -= 10
                            #pygame.time.set_timer(Tempobeat,60000/tempo)
                            #pygame.time.set_timer(Tempobeat,midi_play*100)
                        elif blist2[item] == 'louder':
                            #volume+=10
			    #setVolume(volume)
                            midi_play.Loudpress()
                        elif blist2[item] == 'softer':
                            #volume-=10
			    #setVolume(volume)
                            midi_play.Softpress()
                        elif blist2[item] == 'loop':
                            if midi_play.loop == False:
                                midi_play.loop = True
                            else:
                                midi_play.loop = False 
                for item in range(len(blist3)):
                    ypos = 55 + item * height * 0.2
                    xpos = width*0.8-5
                    buttonwidth = width*0.14
                    buttonheight = height*0.05
                    if click(pygame.Rect(width*0.9,ypos+height*0.05,width/30,height/20),x,y) == True:
                        midi_play.Changebeat()
                        '''currentmetro+=1
                        if currentmetro>len(metromidi)-1:
                            currentmetro = 0
                        if metronomeOn == True:
                            midi_play.song = metromidi[currentmetro]'''
                    if click(pygame.Rect(xpos,ypos,buttonwidth,buttonheight), x, y) == True:
                        if blist3[item] == 'Metronome':
                            '''if metronomeOn == True:
                                metronomeOn = False
                                if midi_play.song in metromidi:
                                    midi_play.song = ''
                            else:
                                metronomeOn = True
                                midi_play.song = metromidi[currentmetro]
                                midi_play.loop = True'''
                            midi_play.Metropress2() 
                        elif blist3[item] == 'Alarm':
                            if clock == True:
                                clock = False
                            else:
                                clock = True                      
            if event.type == VIDEORESIZE or initGUI == True:
                if initGUI == False:
                    width = event.w
                    height = event.h   
                    DISPLAYSURF = pygame.display.set_mode((event.w,event.h),RESIZABLE)  
                initGUI = False

                '''resize the playlist'''
                listPos = []                
                for pos in range(len(musicShow)):
                    Ypos = height*0.3 + pos*height*0.05
                    listPos.append(pygame.Rect(50,Ypos,70,20))
                '''resize the logo'''  
                logoRegWidth = int(round(width/6))
                logoLgWidth = int(round(width/4))
                logoReg = pygame.transform.scale(logo,(int(round(width/6)),int(round(width/6)))) 
                logoLg = pygame.transform.scale(logo,(int(round(width/4)),int(round(width/4))))
                '''change fonts'''
                ButtonFont = pygame.font.SysFont(None, int(round(width*0.025)))  
                TitleFont = pygame.font.SysFont(None, int(round(width*0.08)))
                SensorFont = pygame.font.SysFont(None, int(round(width*0.05)))
                playlist = pygame.Rect(10,height*0.29,width/6,height/2)
                '''resize signal waves'''
                signal = pygame.image.load('signal.png')
                signal2 = pygame.image.load('signal2.png')
                signal = pygame.transform.scale(signal, (int(round(width*0.06)),int(round(height*0.125))))
                signal2 = pygame.transform.scale(signal2, (int(round(width*0.06)),int(round(height*0.125))))
                '''resize scroll'''
                scroll = pygame.Rect(10,height*0.38,30,40)
            if event.type == MOUSEMOTION:
                midi_play.idle_time = 0
        if midi_play.idle_time > 5000 and playing == False:
            DISPLAYSURF.fill(BLACK)
            Print = TitleFont.render('Testing, Testing...',1,WHITE)
            DISPLAYSURF.blit(Print,(50,50))
            Print = SensorFont.render('Is anyone here?',1,WHITE) 
            DISPLAYSURF.blit(Print,(50,300)) 
            DISPLAYSURF.blit(pygame.transform.scale(pygame.image.load('Question.png'),(200,150)),(width-250,height-150))            
        pygame.display.update()
        fpsClock.tick(30)

if __name__ == '__main__':
    main()

