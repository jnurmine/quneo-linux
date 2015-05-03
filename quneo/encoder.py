#!/bin/env python
# -*- coding: iso-8859-15 -*-
# Python version (C) 2012-2015 J. Nurminen <slinky@iki.fi>

# based on "sysexCompiler_1.1.x_ForumRelease" 
# copyright 2012 Keith McMillen Instruments
# original author - daniel mcanulty <dan@keithmcmillen.com>

# Encode data to QuNeo SysEx format

class SyxEncoder:
    SX_ENCODE_LEN = 7
    SX_START = 0xf0
    SX_END = 0xf7
    SX_PACKET_START = 0x01

    def __init__(self):
        self.crc = 0
        self.sum_byte = 0
        self._buf = []
        self.chunk_init()
        self.counter = 0

    def chunk_init(self):
        self.midi_hi_bits = 0
        self.midi_hi_count = 0

    def write(self, val):
        self._buf.append(val)
        self.counter += 1

    def reset_counter(self):
        self.counter = 0

    def encode(self, val):
        self.write(val & 0x7f)
        self.midi_hi_bits |= (val & 0x80)
        self.midi_hi_bits >>= 1
        self.midi_hi_count += 1
        if self.midi_hi_count == self.SX_ENCODE_LEN:
            self.midi_hi_count = 0
            self.write(self.midi_hi_bits)
            # the encoded byte is not counted in data length
            self.counter -= 1

    def sum_encode(self, a):
        a &= 0xff
        assert a >= 0  # yes, I'm sure
        self.encode_crc(a)
        self.sum_byte += a
        self.sum_byte &= 0xff

    def encode_crc_int(self):
        val = self.crc
        self.encode_crc((val >> 8) & 0xff)
        self.encode_crc(val & 0xff)

    def encode_int(self, val):
        self.encode((val >> 8) & 0xff)
        self.encode(val & 0xff)

    def encode_crc(self, val):
        self.crc_byte(val)
        self.encode(val)

    def reset_sum_byte(self):
        self.sum_byte = 0

    def encode_sum_byte(self):
        self.encode(self.sum_byte)

    def flush(self):
        while self.midi_hi_count != 0:
            self.encode_crc(0)

    def start(self):
        self.write(self.SX_START)

    def start_packet(self):
        self.write(self.SX_PACKET_START)

    def stop(self):
        self.write(self.SX_END)

    def crc_byte(self, val):
        val &= 0xff
        crc = self.crc
        temp = (crc >> 8) ^ val
        crc &= 0xffff
        crc <<= 8
        crc &= 0xffff
        quick = ((temp ^ (temp >> 4)) & 0xffff)
        crc ^= quick
        crc &= 0xffff
        quick <<= 5
        quick &= 0xffff
        crc ^= quick
        crc &= 0xffff
        quick <<= 7
        quick &= 0xffff
        crc ^= quick
        crc &= 0xffff
        self.crc = crc

    def crc_init(self):
        self.crc = 0xffff

