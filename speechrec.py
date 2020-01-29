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

  sensitivity = [0.5]*len(models)
  detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
  callbacks = [lambda: my_callback(0, models[0]),
             lambda: my_callback(1, models[1]),
             lambda: my_callback(2, models[2]),
             lambda: my_callback(3, models[3]),
             lambda: midi_play.Pausepress(),
             lambda: midi_play.Pausepress(),
             lambda: midi_play.Pausepress(),
             lambda: midi_play.Pausepress(),
             lambda: midi_play.Fastpress(),
             lambda: midi_play.Fastpress(),
             lambda: midi_play.Slowpress(),
             lambda: midi_play.Slowpress(),
             lambda: my_callback(12, models[12]),
             lambda: my_callback(13, models[13]),
             lambda: my_callback(14, models[14]),
             lambda: my_callback(15, models[15]),
             lambda: my_callback(16, models[16]),
             lambda: my_callback(17, models[17]),
             lambda: my_callback(18, models[18]),
             lambda: my_callback(19, models[19])]
  print('Listening... Press Ctrl+C to exit')

  # main loop
  # make sure you have the same numbers of callbacks and models
  detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.5)

  detector.terminate()

if __name__ == "__main__":
    t = Thread(target = speechrec_main('CricketHotwords.lst'))
    t.daemon = True
    t.start()
    while not interrupted:
      time.sleep(1)
