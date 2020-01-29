import snowboydecoder
import threading
import Queue

import sys
import signal
import time
import subprocess
import midi_play
#from assistant import Assistant

import speech_recognition as sr

#using_google_cloud_speech = False
using_google_cloud_speech = True
voice_on = False

def process_voice_command(command):
  print '*** VOICE COMMAND = [%s] ***' % (command)
  if 'play' in command or 'replay' in command:
      midi_play.Replaypress()
  if 'faster' in command:
      midi_play.Fastpress()
  if 'slower' in command:
      midi_play.Slowpress()
  if 'louder' in command:
      midi_play.Loudpress()
  if 'softer' in command:
      midi_play.Softpress()
  if 'tempo' in command or 'speed' in command or 'BPM' in command:
      if 'increase' in command or 'raise' in command:
          midi_play.Fastpress()
      if 'decrease' in command or 'lower' in command:
          midi_play.Slowpress()
  if 'volume' in command:
      if 'increase' in command or 'raise' in command:
          midi_play.Loudpress()
      if 'decrease' in command or 'lower' in command:
          midi_play.Softpress()
  if 'metronome' in command:
      if 'change' in command:
          midi_play.Changebeat()
      else:
          midi_play.Metropress2()
  if 'pause' in command or 'wait a' in command or 'resume' in command or 'continue' in command: 
      midi_play.Pausepress()
  if 'stop' in command:
      midi_play.Endpress()


def sprec():
  r = sr.Recognizer()
  m = sr.Microphone()

  try:
    print("A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source)
    if r.energy_threshold > 500:
        r.energy_threshold = 500
    #r.energy_threshold = 250
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    if True:
        print("Say something!")
        with m as source: audio = r.listen(source)
        print("Got it! Now to recognize it...")

        if not using_google_cloud_speech: 
          try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)

            # we need some special handling here to correctly print unicode characters to standard output
            if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                print(u"You said {}".format(value).encode("utf-8"))
            else:  # this version of Python uses unicode for strings (Python 3+)
                print("You said {}".format(value))
            process_voice_command(value)

          except sr.UnknownValueError:
            print("Oops! Didn't catch that")
          except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
        else:
          # recognize speech using Google Cloud Speech
          try:
            value = r.recognize_google_cloud(audio, credentials_json=None, preferred_phrases=['play the music', 'pause', 'wait a second', 'resume', 'continue', 'stop the music', 'lower the tempo', 'increase the tempo', 'increase the speed', 'lower the speed', 'increse BPM', 'decrease BPM', 'play the metronome', 'change metronome beat', 'increase the volume', 'lower the volume', 'louder', 'softer', 'faster', 'slower'])
            print("Google Cloud Speech thinks you said ", value)
            process_voice_command(value)
          except sr.UnknownValueError:
            print("Google Cloud Speech could not understand audio")
          except sr.RequestError as e:
            print("Could not request results from Google Cloud Speech service; {0}".format(e))
  except KeyboardInterrupt:
    pass


#def setVolume(vol):
#    subprocess.call(['amixer', 'cset', 'numid=4', '%d%%' % (vol)])


class ThreadedDetector(threading.Thread):
    """
    Wrapper class around detectors to run them in a separate thread
    and provide methods to pause, resume, and modify detection
    """

    def __init__(self, models, **kwargs):
        """
        Initialize Detectors object. **kwargs is for any __init__ keyword
        arguments to be passed into HotWordDetector __init__() method.
        """
        threading.Thread.__init__(self)
        self.models = models
         
        detector_callbacks = [lambda: self.detect_callback(),
                              lambda: self.detect_callback()]
        self.callbacks = detector_callbacks
        self.init_kwargs = kwargs
        self.interrupted = True
        self.commands = Queue.Queue()
        self.vars_are_changed = True
        self.detectors = None  # Initialize when thread is run in self.run()
        self.run_kwargs = None  # Initialize when detectors start in self.start_recog()

    def initialize_detectors(self):
        """
        Returns initialized Snowboy HotwordDetector objects
        """
        self.detectors = snowboydecoder.HotwordDetector(self.models, **self.init_kwargs)
    def detect_callback(self):
        global voice_on
        self.detectors.terminate()
        #snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
        print 'callback is called'
        voice_on = True
        midi_play.setVolume(30)
        #assistant.assist()
        #snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
        sprec()
        time.sleep(1)
        print 'restart the detector'
        midi_play.setVolume(midi_play.volume)
        voice_on = False
        #global interrupted
        #interrupted = False
        #self.detectors.start(detected_callback=self.callbacks, interrupt_check=interrupt_callback, sleep_time=0.03)
        self.detectors.start(detected_callback = self.callbacks, interrupt_check=lambda: self.interrupted, **self.run_kwargs)


    def run(self):
        """
        Runs in separate thread - waits on command to either run detectors
        or terminate thread from commands queue
        """
        try:
            while True:
                command = self.commands.get(True)
                if command == "Start":
                    self.interrupted = False
                    if self.vars_are_changed:
                        # If there is an existing detector object, terminate it
                        if self.detectors is not None:
                            self.detectors.terminate()
                        self.initialize_detectors()
                        self.vars_are_changed = False
                    # Start detectors - blocks until interrupted by self.interrupted variable
                    self.detectors.start(detected_callback = self.callbacks, interrupt_check=lambda: self.interrupted, **self.run_kwargs)
                elif command == "Terminate":
                    # Program ending - terminate thread
                    break
        finally:
            if self.detectors is not None:
                self.detectors.terminate()

    def start_recog(self, **kwargs):
        """
        Starts recognition in thread. Accepts kwargs to pass into the
        HotWordDetector.start() method, but does not accept interrupt_callback,
        as that is already set up.
        """
        assert "interrupt_check" not in kwargs, \
            "Cannot set interrupt_check argument. To interrupt detectors, use Detectors.pause_recog() instead"
        self.run_kwargs = kwargs
        self.commands.put("Start")

    def pause_recog(self):
        """
        Halts recognition in thread.
        """
        self.interrupted = True

    def terminate(self):
        """
        Terminates recognition thread - called when program terminates
        """
        self.pause_recog()
        self.commands.put("Terminate")

    def is_running(self):
        return not self.interrupted

    def change_models(self, models):
        if self.is_running():
            print("Models will be changed after restarting detectors.")
        if self.models != models:
            self.models = models
            self.vars_are_changed = True

    def change_sensitivity(self, sensitivity):
        if self.is_running():
            print("Sensitivity will be changed after restarting detectors.")
        if self.init_kwargs['sensitivity'] != sensitivity:
            self.init_kwargs['sensitivity'] = sensitivity
            self.vars_are_changed = True
