import mido
import pygame
from mido import MidiFile
import time
from threading import Thread
import subprocess

speed = 1
song = ''
message = ''
loop = False
paused = False
metro = False
loudness = 0
stop_program = False
noteon = False
metromidi = ['m440.mid','m441.mid','m442.mid','m443.mid','m444.mid','m445.mid','m446.mid']
alarmmidi = ['wt.mid']
currentmetro = 0
metronomeOn = False
volume = 90
lastsong = ''
running_command = False
idle_time = 0
def midiPlay():
    global speed
    global song
    global message
    global paused
    global metro
    global loudness
    global noteon
    global lastsong
    ChannelList = []
    activeChannels = [False]
    numChannels = []
    mido.set_backend('mido.backends.pygame')
    port = mido.open_output(mido.get_output_names()[1])
    while True:
        if song != '':
        #try:
            if song not in metromidi:
                if song not in alarmmidi:
                    lastsong = song
            psong = song
            #print 'Loading...'
            mid = MidiFile(song)
            #print 'Checking...'
            #for msg in mid:
            #    if not msg.is_meta:
            #       if msg.channel not in ChannelList:
            #            ChannelList.append(msg.channel)
            #       if msg.channel > len(activeChannels)-1:
            #            activeChannels.append(False) 
            #print 'Preparing...'                
            message = 'now playing [%s]' % song
            for msg in mid:
                #print msg
                time.sleep(msg.time/speed)
                if not msg.is_meta:    
                    if msg.channel not in ChannelList:
                        ChannelList.append(msg.channel)
                    if msg.channel > len(activeChannels)-1:
                        activeChannels.append(False) 
                    if msg.type == 'note_on':
                        #activeChannels[msg.channel] = True
                        loudness = msg.velocity
                        if not paused:
                            port.send(msg)
                            #print 'send ON', msg

                        if msg.channel == 9 or msg.channel == max(ChannelList):
                            noteon = not noteon


                    if msg.type == 'note_off':
                        if not paused or True in activeChannels:
                            port.send(msg)
                            #print 'send OFF', msg                            
                        #activeChannels[msg.channel] = False 


                if psong != song:
                    port.reset()
                    break
                
                if True not in activeChannels and paused:
                    port.panic()
                    while paused:
                        pass
            else:
                message = 'The End!'
                if loop == False:
                    song = ''
            
            #except IOError:
              #  print 'Invalid name'
               # message = 'Invalid name'
                #song = 
        else:
            time.sleep(0.5)
    port.close()        



'''
Control Functions
'''
def Playpress():
    global song
    global message
    global idle_time
    idle_time = 0
    song = raw_input('Input song: ')

def Replaypress():
    global song
    global lastsong
    global running_command
    song = lastsong
    running_command = True
    global idle_time
    idle_time = 0

def Fastpress(): 
    print '*** Fastpress ...'
    global speed
    global message
    global running_command
    global idle_time
    idle_time = 0
    running_command = True
    speed += 0.1
    if speed > 5:
        speed = 5

    message = str(speed) + 'x'
    
def Slowpress():
    print '*** Slowpress ...'
    global speed
    global message 
    global running_command
    global idle_time
    idle_time = 0
    running_command = True
    speed -= 0.1
    if speed <= 0.1:
        speed = 0.1

    message = str(speed) + 'x'

def Endpress():
    print '*** Endpress ...'
    global song
    global message
    global metronomeOn
    global running_command
    global idle_time
    global loop
    loop = False
    idle_time = 0
    running_command = True
    if song == '':
        message = 'no song to end'
    else:
        song = ''
        if metronomeOn:
           message = 'metronome ended'
           metronomeOn = False
        else:
           message = 'song ended'
    print message

def Pausepress():
    global paused
    global song
    global message
    global running_command
    global idle_time
    idle_time = 0
    running_command = True
    if paused:
        paused = False
        message = 'Resumed'
    else:
        paused = True
        message = 'Paused'
        if song == '':
            message = 'No song to pause'
            paused = False
    print message

def voicelineControl():
    global running_command
    while True:
        time.sleep(1)
        if running_command:
            time.sleep(1)
            running_command = False

'''
def Metropress():
    global song
    global metronomeOn
    global metromidi
    global loop
    if metronomeOn:
        if song in metromidi:
            song = ''
    else:
        song = metromidi[currentmetro]
        loop = True
    metronomeOn = not metronomeOn
    print 'metronome'
'''
def Changebeat():
    global currentmetro
    global song
    global idle_time
    idle_time = 0
    
    currentmetro+=1
    if currentmetro>len(metromidi)-1:
        currentmetro = 0
    if metronomeOn:
        song = metromidi[currentmetro]
    print 'changebeat'

def Metropress():
    global song
    global metronomeOn
    global loop
    global metromidi
    global idle_time
    idle_time = 0
    if metronomeOn:
        Changebeat()
        if currentmetro == len(metromidi)-1:
            metronomeOn = False
            song = ''
            loop = True
    else:
        metronomeOn = True
        song = metromidi[currentmetro]
        loop = True

def Metropress2():
    global song
    global metronomeOn
    global metromidi
    global loop
    global idle_time
    idle_time = 0
    if metronomeOn:
        Changebeat()
        #metronomeOn = False
        #song = ''
    else:
        metronomeOn = True
        song = metromidi[currentmetro]
        loop = True

    print 'metronome2' 

def setVolume(vol):
    global idle_time
    idle_time = 0
    print 'Set the Volume to %d%%' % vol
    subprocess.call(['amixer', 'cset', 'numid=4', '%d%%' % (vol)])

def Loudpress():
    global idle_time
    idle_time = 0
    global volume
    if volume <= 80:
        volume += 20
        setVolume(volume)
    #amixer.something
    print 'Loudpress'

def Softpress():
    global volume
    global idle_time
    idle_time = 0
    if volume >= 20:
        volume -= 20 
        setVolume(volume)
    print 'Softpress'

def beetbug_main():
    #t = Thread(target = midiPlay)
    #t.daemon = True
    #t.start()
    global speed
    global song
    global message
    global loop
    global paused  
    global stop_program  

    while not stop_program:
        ans = raw_input('BeetBug>')
        if ans == 'help':
            print('Prompts:')
            print('d: decrease tempo.')
            print('a: increase tempo.')
            print('s: play a song.')
            print('q: end any currently playing songs.')
            print('p: pause a song. Press again to unpause.')
            print('l: turn loop on. Press again to turn off.')
            print('exit: exit the program.')
            
        elif ans == 's':
            Playpress()
        elif ans == 'd':
            Slowpress()
        elif ans == 'a':
            Fastpress()
        elif ans == 'q': 
            Endpress()
        elif ans == 'p':
            Pausepress()
            '''
            if paused:
                paused = False
                message = 'Resumed'
            else:
                paused = True
                if song == '':
                    message = 'No song to pause'
                    paused = False
                    '''
        elif ans == 'l':
            if loop == True:
                loop = False
                message = 'Loop Off'
            else:
                loop = True
                message = 'Loop On'
        elif ans == 'm':
            Metropress()
        elif ans == 'loud':
            Loudpress()
        elif ans == 'soft':
            Softpress()
        elif ans == 'exit':
            break
        elif ans == '':
            print 'nothing there'
        else:
            print 'Invalid command'
        if message != '':
            print '[', message, ']'
            message = ''
        #'''                                                


if __name__ == '__main__':
	t = Thread(target = midiPlay)
	t.daemon = True
	t.start()
	beetbug_main()
