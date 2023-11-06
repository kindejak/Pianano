import pianohat
import time

from mingus.core import notes, chords
from mingus.containers import *
from mingus.midi import fluidsynth

actual_octave = 4
MAX_OCTAVE = 7
MIN_OCTAVE = 1
key_num_to_note = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C-1"]
fluidsynth.init("/usr/share/sounds/sf2/FluidR3_GM.sf2", "alsa")

def handle_note(channel, pressed):
    global actual_octave
    key = key_num_to_note[channel]
    if key == "C-1":
        key = "C-" + str(actual_octave + 1)
    else:
        key = key + "-" + str(actual_octave) 
    if pressed:
        print("You pressed key {}.".format(key))
        fluidsynth.play_Note(Note(key))


def handle_octave_up(channel, pressed):
    global actual_octave
    global octaves
    if pressed and actual_octave < MAX_OCTAVE:
        actual_octave += 1
        print('Selected Octave: {}'.format(actual_octave))

def handle_octave_down(channel, pressed):
    global actual_octave
    if pressed and actual_octave > MIN_OCTAVE:
        actual_octave -= 1
        print('Selected Octave: {}'.format(actual_octave))    

# LEDky
pianohat.auto_leds(True)

# zmacknuti klavesy
pianohat.on_note(handle_note)

# zmena octavy
pianohat.on_octave_up(handle_octave_up)
pianohat.on_octave_down(handle_octave_down)


print("Now, make beautiful music...")

print("Now, press keys...")
while(True):
    time.sleep(0.001)
