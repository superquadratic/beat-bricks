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

    def run(self):
        self.running = True
        start_time = time.time()
        last_step = -1

        while self.running:
            delta_time = time.time() - start_time
            current_step = int(delta_time / self.step_time) % 16
            if current_step != last_step:
                last_step = current_step
                self.trigger_step(current_step)

    def trigger_step(self, step):
        note = 36
        for channel in self.pattern:
            if channel[step]:
                self.out.send_message([0x90, note, 100])
                self.out.send_message([0x80, note, 100])
            note += 1

if __name__ == '__main__':
    player = PatternPlayer(120)
    try:
        while True:
            pass
    except:
        player.running = False
