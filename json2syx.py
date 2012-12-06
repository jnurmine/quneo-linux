#!/bin/env python
# -*- coding: iso-8859-15 -*-
# Python version (C) 2012 J. Nurminen <slinky@iki.fi>

# based on "sysexCompiler_1.1.x_ForumRelease" 
# copyright 2012 Keith McMillen Instruments
# original author - daniel mcanulty <dan@keithmcmillen.com>

import sys
import struct
import json

from quneo.exporter import json2syx

infile = open(sys.argv[1], "rb")
in_json = json.load(infile)
infile.close()

num = int(sys.argv[2])
preset = in_json['QuNeo Presets']['Preset %s' % num]
print "Processing preset: \"%s\"" % preset['presetName']

binary = json2syx(preset['ComponentSettings'], 1)

print "Encoded %s bytes." % (len(binary))
outfile = open("test.syx", "wb")
outfile.write(binary)
outfile.close()
