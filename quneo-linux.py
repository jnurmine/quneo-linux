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
from quneo.exporter import reload_preset, query_sysex_id, query_sysex_preset

parser = argparse.ArgumentParser(description="KMI Quneo preset tool")
subparsers = parser.add_subparsers(help="help for subcommand, subcommand --help", dest="subcommand")

parser_debug = subparsers.add_parser("debug", help="debugging options (use at your own risk)")
parser_debug.add_argument("--query_id", action="store_true", required=False, default=None, help="build SysEx ID query")
parser_debug.add_argument("--query_preset", action="store_true", required=False, default=None, help="build SysEx preset query")

parser_preset = subparsers.add_parser("preset", help="Preset commands")
parser_preset.add_argument('--preset_file', metavar='name', \
        type=argparse.FileType('rb'), required=True, \
        help='preset file (JSON) containing one or many presets')

parser_preset.add_argument('--in', dest="in_preset", metavar='number', type=int, \
        required=False, default=None, \
        help="preset number (0..15) from preset file")

parser_preset.add_argument('--out', metavar='number', dest="out_preset", type=int, \
        required=False, default=None, \
        help="preset number (0..15) to overwrite on device (default: 0)")

parser.add_argument('--device', metavar='device', type=str, \
        required=False, default=None, help="ALSA MIDI device to send output to (default: write to file)")

parser.add_argument('--output', metavar='output', type=argparse.FileType('wb'), \
        required=False, default='preset.syx', help="output file for SysEx (default: preset.syx)")

args = parser.parse_args()
if args.device is None:
    print "NOTE: No device given, will write to file %s" % args.output.name

# handle debugging commands
# TODO refactor with callbacks...
if args.subcommand == "debug":
    if args.query_id:
        print "DEBUG: SysEx ID query"
        query = query_sysex_id()
        args.output.write(query)
        args.output.close()
        print "Wrote to %s" % args.output.name
        sys.exit()
    if args.query_preset:
        print "DEBUG: SysEx preset query"
        query = query_sysex_preset()
        args.output.write(query)
        args.output.close()
        print "Wrote to %s" % args.output.name
        sys.exit()
    print "Don't know what to do. Bye."
    sys.exit()

if args.subcommand == "preset":
    if args.out_preset is None:
        print "NOTE: No output preset defined, using 0."
        args.out_preset = 0

    in_json = json.load(args.preset_file)
    args.preset_file.close()

    if in_json.get("QuNeo Presets", None) is not None:
        if args.in_preset is None:
            print "NOTE: The input file contains multiple presets."
            print "Define which one you want with --in."
            sys.exit()
        preset = in_json["QuNeo Presets"]["Preset %s" % args.in_preset]
    else:
        if args.in_preset is not None:
            print "NOTE: File contains only one preset, input preset number ignored."
            args.in_preset = None
        preset = in_json

    print "Processing preset: \"%s\"" % preset['presetName']

    binary = json2syx(preset["ComponentSettings"], args.out_preset)
    load_preset = reload_preset(args.out_preset)

    print "Stored as preset %s" % args.out_preset

    print "Preset size %s bytes." % (len(binary))

    if args.device is None:
        # write a standalone preset file
        args.output.write(binary)
        # append preset loader to the .syx
        args.output.write(load_preset)
        # existing editor null-terminates Sysex stream
        args.output.write(chr(0))
        args.output.close()
        print "Wrote to %s" % args.output.name
    else:
        # device given, write to it directly
        dev = open(args.device, 'wb')
        dev.write(binary)
        dev.write(load_preset)
        dev.write(chr(0)) # for 1:1 with existing editor
        dev.close()
        print "Enjoy your preset %s" % args.out_preset
