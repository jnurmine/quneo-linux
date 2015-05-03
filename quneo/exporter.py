#!/bin/env python
# -*- coding: iso-8859-15 -*-
# Python version (C) 2012-2015 J. Nurminen <slinky@iki.fi>

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

#[1] SysEx Identity Reply: sysexchannel=0  
# mfg_id=(0x0 0x1 0x5f)
# family_code=(0x1e 0x0)
# model_number=(0x0 0x0)
# version_number=(0x3 0x1 0x1e 0x12)
# with firmware 1.2.30
# firmware encoding: "0x1e 0x12",
# MSB byte is last version triplet
# LSB byte is: MSB nybble=major, LSB nybble=minor, 0x12=1.2

# ident magic comes after sysex start code
syx_ident_magic = [
        0x00, # manufacturer ID byte 0 (defined by next 2 bytes)
        0x01, # manufacturer ID byte 1
        0x5f, # manufacturer ID byte 2
        0x7a, # ?
        0x1e, # Quneo family code byte 0
        0x00  # Quneo family code byte 1
        ]

syx_preset_start = 0xa1

def _unwrap(s, js, fields):
    for field in fields:
        a = js[field]
        if field in ["rB%soutSpeed" % i for i in xrange(1,5)]:
            # rotaries are special, 16bit
            lsb = a & 0xff
            msb = (a >> 8) & 0xff
            s.sum_encode(msb)
            s.sum_encode(lsb)
        else:
            s.sum_encode(a)


def build_data(preset, encoder=None):
    """ Build Sysex preset data to given encoder instance
    Returns the length of newly-built data.
    If encoder is None, create a throw-away instance of the encoder, useful for
    calculating data length in caller
    """
    if encoder is None:
        encoder = SyxEncoder()

    rotaries = structs.build_rotaries()
    longsliders = structs.build_longsliders()
    hsliders = structs.build_hsliders()
    vsliders = structs.build_vsliders()

    # pads, sliders, buttons, etc.
    for i in range(16):
        _unwrap(encoder, preset[structs.PADS]["Pad%s" % i], structs.pads)

    for i in range(2):
        _unwrap(encoder, preset[structs.ROTARIES]["Rotary%s" % i], rotaries)

    _unwrap(encoder, preset[structs.LONG_SLIDERS]["LongSlider0"], longsliders)

    for i in range(4):
        _unwrap(encoder, preset[structs.H_SLIDERS]["HSlider%s" % i], hsliders)

    for i in range(4):
        _unwrap(encoder, preset[structs.V_SLIDERS]["VSlider%s" % i], vsliders)

    for i in range(4):
        _unwrap(encoder, preset[structs.LR_BUTTONS]["LeftRightButton%s" % i], structs.lrswitches)

    for i in range(2):
        _unwrap(encoder, preset[structs.UD_BUTTONS]["UpDownButton%s" % i], structs.udswitches)

    _unwrap(encoder, preset[structs.RHOMBUS_BUTTONS]["RhombusButton0"], structs.rhswitches)

    for i in range(3):
        _unwrap(encoder, preset[structs.TRANSPORT_BUTTONS]["TransportButton%s" % i], structs.tbuttons)

    _unwrap(encoder, preset[structs.MODE_BUTTONS]["ModeButton0"], structs.mswitches)

    # globals
    for path in structs.globalpaths:
        x = preset
        for item in path:
            x = x[item]
        encoder.sum_encode(x)

    # special case: velocity table
    for velocity in preset[structs.PADS]['padVelocityTable']:
        encoder.sum_encode(velocity)

    data_length = encoder.counter
    return data_length


def json2syx(preset, num):
    """ Encode json-format preset to SysEx dump for preset number 'num'.
    """
    rotaries = structs.build_rotaries()
    longsliders = structs.build_longsliders()
    hsliders = structs.build_hsliders()
    vsliders = structs.build_vsliders()

    #
    # Preamble
    #
    data = SyxEncoder()
    data.start()
    for magic in syx_ident_magic:
        data.write(magic)
    # pad with zeroes until offset 0x21
    for i in range(13*2):
        data.write(0)

    data.start_packet()
    data.crc_init()
    data.chunk_init()

    data.encode_crc(0x00)   # TYPE_MSB
    data.encode_crc(0x02)   # TYPE_LSB
    # ID: 0x1110 = firmware, 0x2220 = preset data
    # 30xx = load preset
    data.encode_crc(0x22)
    data.encode_crc(0x20)

    data.encode_crc_int()
    data.flush()

    #
    # Preset header
    #
    data.reset_sum_byte()
    data.encode(syx_preset_start)
    data.encode(num)
    data_length = build_data(preset, encoder=None)

    syx_preset_length_msb = (data_length >> 8) & 0xff
    syx_preset_length_lsb = data_length & 0xff
    data.encode(syx_preset_length_msb)
    data.encode(syx_preset_length_lsb)
    data.crc_init()

    #
    # Preset data
    #
    build_data(preset, encoder=data)

    data.encode(num) # index of this preset
    data.encode(num) # index of last preset in this SysEx
    data.encode_sum_byte()
    data.flush()

    data.stop()

    #print "data_length=%s, msb=%s, lsb=%s" % (data_length, hex(syx_preset_length_msb), hex(syx_preset_length_lsb))

    return ''.join(struct.pack("B", x) for x in data._buf)


def reload_preset(num):
    s = SyxEncoder()

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

    return ''.join(struct.pack("B", x) for x in s._buf)


def query_sysex_id():
    return ''.join(struct.pack("B", x) for x in [0xf0, 0x7e, 0x7f, 0x06, 0x01, 0xf7])

def query_sysex_preset():
    return ''.join(struct.pack("B", x) for x in \
            [0xf0, 0x00, 0x01, 0x5f, 0x7a, 0x1e, \
             0x00, 0x01, 0x00, 0x02, 0x50, 0x04, \
             0x24, 0x1b, 0x00, 0x30, 0xf7])
