import liblo
import numpy

class Pattern(object):
    def __init__(self, channels=8, steps=16):
        self.steps = numpy.zeros((steps, channels), bool)
        self.muted = numpy.zeros(channels, bool)

    @property
    def num_channels(self):
        return self.steps.shape[1]

    @property
    def num_steps(self):
        return self.steps.shape[0]

    def set_step(self, channel, step):
        self.steps[step, channel] = True

    def clear_step(self, channel, step):
        self.steps[step, channel] = False

    def mute(self, channel):
        self.muted[channel] = True

    def unmute(self, channel):
        self.muted[channel] = False

class SharedPattern(Pattern):
    def __init__(self, address=8765):
        Pattern.__init__(self)
        self.target = liblo.Address(address)

    def set_step(self, channel, step):
        if not self.steps[step, channel]:
            liblo.send(self.target, '/pattern/set', channel, step)
        Pattern.set_step(self, channel, step)

    def clear_step(self, channel, step):
        if self.steps[step, channel]:
            liblo.send(self.target, '/pattern/clear', channel, step)
        Pattern.clear_step(self, channel, step)

    def mute(self, channel):
        if not self.muted[channel]:
            liblo.send(self.target, '/pattern/mute', channel)
        Pattern.mute(self, channel)

    def unmute(self, channel):
        if self.muted[channel]:
            liblo.send(self.target, '/pattern/unmute', channel)
        Pattern.unmute(self, channel)

class PatternListener(liblo.ServerThread):
    def __init__(self, address=8765):
        liblo.ServerThread.__init__(self, address)
        self.pattern = Pattern()

    @liblo.make_method('/pattern/set', 'ii')
    def set_callback(self, path, args):
        channel, step = args
        self.pattern.set_step(channel, step)

    @liblo.make_method('/pattern/clear', 'ii')
    def clear_callback(self, path, args):
        channel, step = args
        self.pattern.clear_step(channel, step)

    @liblo.make_method('/pattern/mute', 'i')
    def mute_callback(self, path, channel):
        self.pattern.mute(channel)

    @liblo.make_method('/pattern/unmute', 'i')
    def unmute_callback(self, path, channel):
        self.pattern.unmute(channel)
