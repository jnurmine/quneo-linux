#!/bin/env python
# -*- coding: iso-8859-15 -*-
# (C) 2012 J. Nurminen <slinky@iki.fi>

# quick and dirty codecs for various MIDI messages

def read_byte(dev, count=None):
    if count is None:
        return ord(dev.read(1))
    else:
        x = []
        for i in range(count):
            x.append(ord(dev.read(1)))
        return x

class Msg:
    """Base class for the known MIDI messages
    """
    def __init__(self, name, mask):
        self.name = name
        self.mask = mask

    def accepts(self, val):
        if ((val & 0b11110000) & (self.mask << 4)) == self.mask << 4:
            return True
        return False

    def channel(self, status_byte):
        # zero based
        return (status_byte & 0b00001111) + 1

    def prefix(self, status_byte):
        return "[%s] %s:" % (self.channel(status_byte), self.name)

# the specialized classes start here

class ControlChange(Msg):
    def __init__(self):
        Msg.__init__(self, "Control Change", 0b1011)

    def process(self, status_byte, dev):
        if not self.accepts(status_byte):
            return False
        x = read_byte(dev, 2)
        controller = x[0] & 0b01111111
        value = x[1] & 0b01111111
        s = self.prefix(status_byte)
        if status_byte in range(120, 127+1):
            # channel mode messages
            if controller == 120:
                assert value == 0, "All Sound Off should have value = 0"
                s += " All Sound Off"
            if controller == 121:
                s += " Reset All Controllers"
            if controller == 122:
                s += " Local Control: "
                if value == 0:
                    s += "Off"
                elif value == 127:
                    s += "On"
                else:
                    print "Warning: potentially bad value %s" % value
            if controller == 123:
                assert value == 0, "All Notes Off should have value = 0"
                s += " All Notes Off"
            if controller == 123:
                assert value == 0, "All Notes Off should have value = 0"
                s += " All Notes Off"
            if controller == 124:
                assert value == 0, "Omni Off should have value = 0"
                s += " Omni Mode Off"
            if controller == 125:
                assert value == 0, "Omni On should have value = 0"
                s += " Omni Mode On"
            if controller == 126:
                if value == 0:
                    s += " Poly Mode On, Omni On"
                else:
                    s += " Poly Mode On, Omni Off, channels=%s" % value
            if controller == 127:
                assert value == 0, "Poly Off should have value = 0"
                s += " Poly Mode Off"
        else:
            # control change
            s += " controller=%s value=%s" % (controller, value)
        print s
        return True


class NoteOff(Msg):
    def __init__(self):
        Msg.__init__(self, "Note Off", 0b1000)

    def process(self, status_byte, dev):
        if not self.accepts(status_byte):
            return False
        s = self.prefix(status_byte)
        x = read_byte(dev, 2)
        key = x[0] & 0b01111111
        velocity = x[1] & 0b01111111
        s += " note=%s velocity=%s" % (key, velocity)
        print s
        return True


class NoteOn(Msg):
    def __init__(self):
        Msg.__init__(self, "Note On", 0b1001)

    def process(self, status_byte, dev):
        if not self.accepts(status_byte):
            return False
        s = self.prefix(status_byte)
        x = read_byte(dev, 2)
        key = x[0] & 0b01111111
        velocity = x[1] & 0b01111111
        s += " note=%s velocity=%s" % (key, velocity)
        print s
        return True


class ProgramChange(Msg):
    def __init__(self):
        Msg.__init__(self, "Program Change", 0b1100)

    def process(self, status_byte, dev):
        if not self.accepts(status_byte):
            return False
        s = self.prefix(status_byte)
        x = read_byte(dev)
        patch = x & 0b01111111
        s += " number=%s" % patch
        print s
        return True


class PitchWheel(Msg):
    def __init__(self):
        Msg.__init__(self, "Pitch Wheel", 0b1110)

    def process(self, status_byte, dev):
        if not self.accepts(status_byte):
            return False
        s = self.prefix(status_byte)
        x = read_byte(dev, 2)
        lsb = x & 0b01111111
        msb = x & 0b01111111
        # 14-bit value
        val = msb << 7 + lsb
        s += " value=%s" % val
        print s
        return True


class UnknownMessage(Msg):
    """Unknown message type, always accept and print with hex dump of
    received value. Make sure this is the last handler in the chain.
    """
    def __init__(self):
        Msg.__init__(self, "Unknown", 0b1111)

    def process(self, status_byte, dev):
        s = " hex: %s" % hex(status_byte)
        print s
        return True
