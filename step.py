import numpy
import pypm

from pattern import Pattern, PatternListener

LATENCY = 8


class StepSequencer(object):
    def __init__(self, pattern=Pattern()):
        pypm.Initialize()
        self.bpm = 120
        self.pattern = pattern
        self.output = pypm.Output(pypm.GetDefaultOutputDeviceID(), LATENCY)

    @property
    def bpm(self):
        return 15000.0 / self._step_time

    @bpm.setter
    def bpm(self, bpm):
        self._step_time = 15000.0 / bpm

    def play(self):
        next_time = pypm.Time()
        step = -1
        while True:
            if pypm.Time() >= next_time:
                step = (step + 1) % 16
                self.trigger_step(step, next_time)
                if pypm.Time() - next_time > LATENCY:
                    print 'WARNING: Inaccurate timing. Increase LATENCY.'
                next_time += self._step_time

    def trigger_step(self, step, timestamp):
        for track, note_on in enumerate(self.pattern.steps[step]):
            if note_on and not self.pattern.muted[track]:
                self.output.Write([[[0x90, 36 + track, 100], timestamp]])
                self.output.Write([[[0x80, 36 + track], timestamp]])


if __name__ == '__main__':
    pattern_listener = PatternListener()
    pattern_listener.start()
    step = StepSequencer(pattern_listener.pattern)
    step.play()
