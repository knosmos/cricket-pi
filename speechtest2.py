import snowboydecoder
import sys
import signal
import time
from threading import Thread
import midi_play

# Demo code for listening two hotwords at the same time

interrupted = False


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

def load_model_list(listFName):
    models = []
    with open(listFName) as fpIn:
        for line in fpIn:
	    if 'pmdl' in line:
                 models.append(line.rstrip())

    return models

def hotword_callback(hotword_detector, word_detector, word_callbacks):
    hotword_detector.terminate()
    print '++++++++++++++++++++ hotword_callback called!++++++++++++++++++++++'
    word_detector.start(detected_callback=word_callbacks,
                   interrupt_check=interrupt_callback,
                   sleep_time=0.5)


def word_callback(idx, word, hotword_detector, word_detector, word_callbacks):
    word_detector.terminate()
    print '********************* Word #%d [%s] recognized!********************* ' % (idx, word)
    hotword_callbacks = [lambda: hotword_callback(hotword_detector,word_detector,word_callbacks),
                         lambda: hotword_callback(hotword_detector,word_detector,word_callbacks)]
    hotword_detector.start(detected_callback=hotword_callbacks,
                   interrupt_check=interrupt_callback,
                   sleep_time=0.5)



def my_callback(idx, hotword):
    print 'Hotword #%d [%s] Detected!' % (idx, hotword)

def my_callback2(idx):
    print 'My Hotword #%d Detected!' % (idx)

def speechrec_main(listFName):
  models = load_model_list(listFName)
  print 'models = ', models
  time.sleep(1)

  # capture SIGINT signal, e.g., Ctrl+C
  signal.signal(signal.SIGINT, signal_handler)


  hotword_models = models[0:2]
  hotword_sensitivity = [0.5]*len(hotword_models)
  hotword_detector = snowboydecoder.HotwordDetector(hotword_models, sensitivity=hotword_sensitivity)

  word_models = models[2:20]
  word_sensitivity = [0.5]*len(word_models)
  word_detector = snowboydecoder.HotwordDetector(word_models, sensitivity=word_sensitivity)

  word_callbacks = [lambda: word_callback(2, models[2], hotword_detector, word_detector, word_callbacks),
                    lambda: word_callback(3, models[3], hotword_detector, word_detector, word_callbacks),
                    lambda: word_callback(4, models[4], hotword_detector, word_detector, word_callbacks),
                    lambda: word_callback(5, models[5], hotword_detector, word_detector, word_callbacks),
                    lambda: word_callback(6, models[6], hotword_detector, word_detector, word_callbacks),
                    lambda: word_callback(7, models[7], hotword_detector, word_detector, word_callbacks),
                    lambda: word_callback(8, models[8], hotword_detector, word_detector, word_callbacks),
                    lambda: word_callback(9, models[9], hotword_detector, word_detector, word_callbacks),
                    lambda: word_callback(10, models[10], hotword_detector, word_detector, word_callbacks),
                    lambda: word_callback(11, models[11],  hotword_detector, word_detector, word_callbacks),
                    lambda: word_callback(12, models[12], hotword_detector, word_detector, word_callbacks),
                    lambda: word_callback(13, models[13], hotword_detector, word_detector, word_callbacks),
                    lambda: word_callback(14, models[14], hotword_detector, word_detector, word_callbacks),
                    lambda: word_callback(15, models[15], hotword_detector, word_detector, word_callbacks),
                    lambda: word_callback(16, models[16], hotword_detector, word_detector, word_callbacks),
                    lambda: word_callback(17, models[17], hotword_detector, word_detector, word_callbacks),
                    lambda: word_callback(18, models[18], hotword_detector, word_detector, word_callbacks),
                    lambda: word_callback(19, models[19], hotword_detector, word_detector, word_callbacks)]

  hotword_callbacks = [lambda: hotword_callback(hotword_detector,word_detector,word_callbacks),
                       lambda: hotword_callback(hotword_detector,word_detector,word_callbacks)]
  hotword_detector.start(detected_callback=hotword_callbacks,
                   interrupt_check=interrupt_callback,
                   sleep_time=0.5)

  print('Listening... Press Ctrl+C to exit')

  hotword_detector.terminate()


'''
detector1 = ...  models[0:2]   
detector1.start(callback1, ...)
detector2 = ...  models[2:20]  

def callback1:
    detector1.terminate()
    detector2.start(callback2, ...)

def callback2:
    detector2.terminate()
    do xxxx
    dectector1.start(callback1, ...)
'''



if __name__ == "__main__":
    t = Thread(target = speechrec_main('CricketHotwords.lst'))
    t.daemon = True
    t.start()
    while not interrupted:
      time.sleep(1)
