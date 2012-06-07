import liblo
import numpy


class Pattern(object):
    def __init__(self, tracks=8, steps=16):
        self.steps = numpy.zeros((steps, tracks), bool)
        self.muted = numpy.zeros(tracks, bool)

    @property
    def num_tracks(self):
        return self.steps.shape[1]

    @property
    def num_steps(self):
        return self.steps.shape[0]

    def set_step(self, track, step):
        self.steps[step, track] = True

    def clear_step(self, track, step):
        self.steps[step, track] = False

    def mute(self, track):
        self.muted[track] = True

    def unmute(self, track):
        self.muted[track] = False


class SharedPattern(Pattern):
    def __init__(self, address=8765):
        Pattern.__init__(self)
        self.target = liblo.Address(address)

    def set_step(self, track, step):
        if not self.steps[step, track]:
            liblo.send(self.target, '/pattern/set', track, step)
        Pattern.set_step(self, track, step)

    def clear_step(self, track, step):
        if self.steps[step, track]:
            liblo.send(self.target, '/pattern/clear', track, step)
        Pattern.clear_step(self, track, step)

    def mute(self, track):
        if not self.muted[track]:
            liblo.send(self.target, '/pattern/mute', track)
        Pattern.mute(self, track)

    def unmute(self, track):
        if self.muted[track]:
            liblo.send(self.target, '/pattern/unmute', track)
        Pattern.unmute(self, track)


class PatternListener(liblo.ServerThread):
    def __init__(self, address=8765):
        liblo.ServerThread.__init__(self, address)
        self.pattern = Pattern()

    @liblo.make_method('/pattern/set', 'ii')
    def set_callback(self, path, args):
        track, step = args
        self.pattern.set_step(track, step)

    @liblo.make_method('/pattern/clear', 'ii')
    def clear_callback(self, path, args):
        track, step = args
        self.pattern.clear_step(track, step)

    @liblo.make_method('/pattern/mute', 'i')
    def mute_callback(self, path, track):
        self.pattern.mute(track)

    @liblo.make_method('/pattern/unmute', 'i')
    def unmute_callback(self, path, track):
        self.pattern.unmute(track)
