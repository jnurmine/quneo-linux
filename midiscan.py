#!/bin/env python
# -*- coding: iso-8859-15 -*-
# (C) 2012-2015 J. Nurminen <slinky@iki.fi>

# a simple MIDI message scanner

import sys

from simplemidi.messages import *

# messages we want to scan for
msgs = [SysexUniversal(), ControlChange(), ProgramChange(), \
        NoteOn(), NoteOff(), PitchWheel(), \
        UnknownMessage()]

if len(sys.argv) != 2:
    print "%s alsadevice" % sys.argv[0]
    print ""
    print "alsadevice - path to ALSA MIDI device, e.g. /dev/snd/midiC2D0"
    sys.exit()

device = sys.argv[1]

print "Using ALSA MIDI device %s" % device
print "Hit ctrl-C to stop"
print ""

dev = open(device, "rb")

# main loop
while True:
    x = read_byte(dev)
    for m in msgs:
        if m.process(x, dev):
            break

dev.close()
