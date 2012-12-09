#!/bin/env python
# -*- coding: iso-8859-15 -*-
# Python version (C) 2012 J. Nurminen <slinky@iki.fi>

# based on "sysexCompiler_1.1.x_ForumRelease" 
# copyright 2012 Keith McMillen Instruments
# original author - daniel mcanulty <dan@keithmcmillen.com>

import sys
import struct
import json
import argparse

from quneo.exporter import json2syx
from quneo.exporter import reload_preset

parser = argparse.ArgumentParser(description="KMI Quneo preset tool")
parser.add_argument('--preset_file', metavar='name', \
        type=argparse.FileType('rb'), required=True, \
        help='Preset file (JSON)')
parser.add_argument('--num', metavar='preset number', type=int, \
        required=True, \
        help="Preset number to overwrite on device")
parser.add_argument('--device', metavar='device', type=str, \
        default=None, help="ALSA MIDI device to send output to (default: write to file)")
parser.add_argument('--output', metavar='output', type=argparse.FileType('wb'), \
        default='preset.syx', help="output file for SysEx (default: preset.syx)")

args = parser.parse_args()

if args.device is None:
    print "NOTE: No device given, will write to file %s" % args.output.name

in_json = json.load(args.preset_file)
args.preset_file.close()

print "Processing preset: \"%s\"" % in_json['presetName']

binary = json2syx(in_json['ComponentSettings'], args.num-1)  # zero based
load_preset = reload_preset(args.num-1) # zero based

print "Preset size %s bytes." % (len(binary))

if args.device is None:
    # write a standalone preset file
    args.output.write(binary)
    # append preset loader to the .syx
    args.output.write(load_preset)
    args.output.close()
    print "Wrote to %s" % args.output.name
else:
    # device given, write to it directly
    dev = open(args.device, 'wb')
    dev.write(binary)
    dev.write(load_preset)
    dev.close()
    print "Enjoy your preset %s" % args.num
