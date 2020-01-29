import snowboydecoder
import sys
import signal

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


if len(sys.argv) != 2:
    print("Error: need to specify model list filename")
    print("Usage: python models.list")
    sys.exit(-1)

listFName = sys.argv[1]
models = load_model_list(listFName)
print 'models = ', models

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

sensitivity = [0.5]*len(models)
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
#callbacks = [lambda: snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING),
#             lambda: snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)]
callbacks = []
for i in range(len(models)):
    if i % 2 == 0:
	callbacks.append(lambda: snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING))
    else:
	callbacks.append(lambda: snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG))
print('Listening... Press Ctrl+C to exit')

# main loop
# make sure you have the same numbers of callbacks and models
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
