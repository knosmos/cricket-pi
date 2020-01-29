import snowboydecoder
import sys
import signal
import time
import logging
import subprocess
#from assistant import Assistant

interrupted = False

logging.basicConfig()
logger = logging.getLogger("daemon")
logger.setLevel(logging.DEBUG)


import speech_recognition as sr

def sprec():
  r = sr.Recognizer()
  m = sr.Microphone()

  try:
    print("A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    if True:
        print("Say something!")
        with m as source: audio = r.listen(source)
        print("Got it! Now to recognize it...")
        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)

            # we need some special handling here to correctly print unicode characters to standard output
            if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                print(u"You said {}".format(value).encode("utf-8"))
            else:  # this version of Python uses unicode for strings (Python 3+)
                print("You said {}".format(value))
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))

        # recognize speech using Google Cloud Speech
        try:
            print("Google Cloud Speech thinks you said " + r.recognize_google_cloud(audio, credentials_json=None, preferred_phrases=['play the music', 'pause', 'wait a second', 'stop the music', 'lower the tempo', 'increase the tempo', 'play the metronome', 'increase the volume', 'lower the volume']))
        except sr.UnknownValueError:
            print("Google Cloud Speech could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Cloud Speech service; {0}".format(e))



  except KeyboardInterrupt:
    pass


if len(sys.argv) < 3:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model1 your.model2")
    sys.exit(-1)

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

model = [sys.argv[1], sys.argv[2]]
# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

sensitivities = [0.45] * len(model)
detector = snowboydecoder.HotwordDetector(model, sensitivity=sensitivities)
#assistant = Assistant()

def setVolume(vol):
    subprocess.call(['amixer', 'cset', 'numid=4', '%d%%' % (vol)])

def detect_callback(detector_callbacks):
    detector.terminate()
    #snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
    print 'callback is called'
    setVolume(20)
    #assistant.assist()
    #snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
    sprec()
    time.sleep(1)
    print 'restart the detector'
    setVolume(100)
    #global interrupted
    #interrupted = False
    detector.start(detected_callback=detector_callbacks, interrupt_check=interrupt_callback, sleep_time=0.03)


print('Listening... Press Ctrl+C to exit')

# main loop
detector_callbacks = [lambda: detect_callback(detector_callbacks),
                      lambda: detect_callback(detector_callbacks)]
detector.start(detected_callback=detector_callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
