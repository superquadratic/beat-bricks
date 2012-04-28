import threading
import time

import rtmidi_python as rtmidi

class PatternPlayer(threading.Thread):
    def __init__(self, pattern, bpm):
        threading.Thread.__init__(self)
        self.out = rtmidi.MidiOut()
        self.out.open_virtual_port('Beat Bricks')
        self.step_time = 60.0 / bpm / 4
        self.pattern = pattern
        self.start()

    def stop(self):
        self.event.set()

    def run(self):
        self.event = threading.Event()
        step = -1
        while not self.event.is_set():
            step = (step + 1) % 16
            self.trigger_step(step)
            self.event.wait(self.step_time)

    def trigger_step(self, step):
        note = 36
        for channel in self.pattern:
            if channel[step]:
                self.out.send_message([0x90, note, 100])
                self.out.send_message([0x80, note, 100])
            note += 1
