# Cricket Pi
Cricket Pi is a voice-controllable MIDI player with playback, tempo, and volume control. Along with features including metronome and alarm clock (to remind you when to practice), Cricket is a cute and amazing "little" accompanist for violin students. 

---

## Getting Started

Clone or download the repository to your computer.

### Running on Windows
* Simply run `python CricketPi.py`.

### Running on Raspberry Pi
* As the Raspberry Pi does not have a hardware synthesizer, Cricket Pi uses TiMidity++ for a sequencer port in order to play MIDI files. In terminal, run `sudo apt-get install timidity`.
* Then run `timidity -iAqq`. This starts TiMidity++ and opens some sequencer ports.
* Then run `python CricketPi.py`.
