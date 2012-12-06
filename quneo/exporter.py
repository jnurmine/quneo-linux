#!/bin/env python
# -*- coding: iso-8859-15 -*-
# Python version (C) 2012 J. Nurminen <slinky@iki.fi>

# based on "sysexCompiler_1.1.x_ForumRelease" 
# copyright 2012 Keith McMillen Instruments
# original author - daniel mcanulty <dan@keithmcmillen.com>

#
# Export Quneo json structure to a SysEx dump
#

import sys
import struct
import json

import structs
from encoder import SyxEncoder

syx_ident_magic = [0x00, 0x01, 0x5f, 0x7a, 0x1e, 0x00]
syx_preset_start = 0xa1

syx_preset_length = 951 # FIXME
syx_preset_length_msb = syx_preset_length >> 8
syx_preset_length_lsb = syx_preset_length & 0xff

def _unwrap(s, js, fields):
    for field in fields:
        a = js[field]
        if field in ["rB%soutSpeed" % i for i in xrange(1,5)]:
            # rotaries are special
            lsb = a & 0xff
            msb = a >> 8
            s.sum_encode(msb)
            s.sum_encode(lsb)
        else:
            s.sum_encode(a)

def json2syx(preset, num):
    """ Encode json-format preset to SysEx dump for preset number 'num'.
    """
    s = SyxEncoder()
    #print preset

    s.start()
    for magic in syx_ident_magic:
        s.write(magic)
    s.start_packet()
    s.crc_init()
    s.chunk_init()

    # preamble
    s.encode_crc(0x00)
    s.encode_crc(0x02)
    # 0x1110 = firmware, 0x2220 = preset
    # 30xx = load preset xx
    s.encode_crc(0x22)
    s.encode_crc(0x20)
    s.encode_crc_int()
    s.flush()

    s.reset_sum_byte()
    s.encode(syx_preset_start)
    s.encode(num)
    s.encode(syx_preset_length_msb)
    s.encode(syx_preset_length_lsb)

    s.crc_init()

    # pads, sliders, buttons, etc.
    for i in xrange(16):
        _unwrap(s, preset['Pads']["Pad%s" % i], structs.pads)

    for i in range(2):
        _unwrap(s, preset['Rotaries']["Rotary%s" % i], structs.rotaries)

    _unwrap(s, preset['LongSliders']["LongSlider0"], structs.longsliders)

    for i in range(4):
        _unwrap(s, preset['HSliders']["HSlider%s" % i], structs.hsliders)

    for i in range(4):
        _unwrap(s, preset['VSliders']["VSlider%s" % i], structs.vsliders)

    for i in range(4):
        _unwrap(s, preset['LeftRightButtons']["LeftRightButton%s" % i], structs.lrswitches)

    for i in range(2):
        _unwrap(s, preset['UpDownButtons']["UpDownButton%s" % i], structs.udswitches)

    _unwrap(s, preset['RhombusButtons']["RhombusButton0"], structs.rhswitches)

    for i in range(3):
        _unwrap(s, preset['TransportButtons']["TransportButton%s" % i], structs.tbuttons)

    _unwrap(s, preset['ModeButtons']["ModeButton0"], structs.mswitches)

    # globals
    for path in structs.globalpaths:
        x = preset
        for item in path:
            x = x[item]
        s.sum_encode(x)

    # velocity table
    for velocity in preset['Pads']['padVelocityTable']:
        s.sum_encode(velocity)

    s.encode(num)
    s.encode(num) # TODO endNum-1
    s.encode_sum_byte()
    s.flush()
    s.stop()

    #print [hex(x) for x in s._buf]
    return ''.join(struct.pack("B", x) for x in s._buf)


def reload_preset(num):
    s = SyxEncoder()
    #print preset

    s.start()
    for magic in syx_ident_magic:
        s.write(magic)
    s.start_packet()
    s.crc_init()
    s.chunk_init()

    # preamble
    s.encode_crc(0x00)
    s.encode_crc(0x02)
    # 0x1110 = firmware, 0x2220 = preset
    # 30xx = load preset xx
    s.encode_crc(0x30)
    s.encode_crc(0x00 + num)
    s.encode_crc_int()
    s.flush()
    s.stop()
    #print [hex(x) for x in s._buf]
    return ''.join(struct.pack("B", x) for x in s._buf)

