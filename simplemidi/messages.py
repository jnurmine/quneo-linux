#!/bin/env python
# -*- coding: iso-8859-15 -*-
# (C) 2012-2015 J. Nurminen <slinky@iki.fi>

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


class SysexMsg:
    """Base class for the known MIDI System Exclusive messages
    """
    def __init__(self, name, subid1, subid2):
        self.name = name
        self.subid1 = subid1
        self.subid2 = subid2

    def accepts(self, subid1, subid2):
        if subid1 != self.subid1:
            return False
        if subid2 != self.subid2:
            return False
        return True

    def prefix(self, channel):
        return "[%s] %s:" % (channel, self.name)


# the specialized classes start here
class SysexGeneralInfo(SysexMsg):
    GENERAL_INFORMATION = 0x6
    IDENTITY_REPLY = 0x2

    def __init__(self):
        SysexMsg.__init__(self, "SysEx General Information",
                SysexGeneralInfo.GENERAL_INFORMATION,
                SysexGeneralInfo.IDENTITY_REPLY)

    def process(self, channel, subid1, subid2, dev):
        if not self.accepts(subid1, subid2):
            return False
        self.name = "SysEx Identity Reply"

        s = self.prefix(channel)

        mfg_id = read_byte(dev, 3)
        special = ""
        if mfg_id == [0x00, 0x01, 0x5f]:
            special = " (KMI)"
        s += " Manufacturer ID: %s%s\n" % (' '.join(hex(x) for x in mfg_id), special)

        is_quneo = False
        family_code = read_byte(dev, 2)
        special = ""
        if family_code == [0x1e, 0x00]:
            special = " (QuNeo)"
            is_quneo = True
        s += " Family code: %s%s\n" % (' '.join(hex(x) for x in family_code), special)

        model_number = read_byte(dev, 2)
        s += " Model number: %s\n" % (' '.join(hex(x) for x in model_number))
        version_number = read_byte(dev, 4)
        if is_quneo:
            fw_build = version_number[2]
            fw_major = version_number[3] >> 4
            fw_minor = version_number[3] & 0xf
            special = " (Firmware %s.%s.%s)" % (fw_major, fw_minor, fw_build)
        s += " Version number: %s%s\n" % (' '.join(hex(x) for x in version_number), special)
        print s
        return True


class SysexQuneoPreset(SysexMsg):
    GENERAL_INFORMATION = 0x6
    PRESET_REPLY = 0x3

    def __init__(self):
        SysexMsg.__init__(self, "SysEx Preset Reply",
                SysexQuneoPreset.GENERAL_INFORMATION,
                SysexQuneoPreset.PRESET_REPLY)

    def process(self, channel, subid1, subid2, dev):
        if not self.accepts(subid1, subid2):
            return False

        s = self.prefix(channel)

        mfg_id = read_byte(dev, 3)
        #if mfg_id != [0x00, 0x01, 0x5f]:
        #    print "Manufacturer not KMI?"

        family_code = read_byte(dev, 2)
        #if family_code != [0x1e, 0x00]:
        #    print "Device not QuNeo?"

        version_number = read_byte(dev, 4)
        zero = read_byte(dev)
        preset = read_byte(dev)
        s += " preset: %s" % (preset)
        print s
        return True


class SysexDump(SysexMsg):
    def __init__(self):
        SysexMsg.__init__(self, "SysEx Hex Dump", 0, 0)

    def accepts(self, subid1, subid2):
        # any sysex will be accepted
        return True

    def process(self, channel, subid1, subid2, dev):
        s = self.prefix(channel)
        s += " %s" % hex(0b11110000)    # 0xf0
        s += " %s" % hex(0x7e)          # 0x7e, we know these two
        s += " %s" % hex(channel)
        s += " %s" % hex(subid1)
        s += " %s" % hex(subid2)
        while True:
            r = read_byte(dev)
            s += " %s" % hex(r)
            if r == 0xf7: # sysex end
                break
        print s
        return True


class SysexUniversal(Msg):
    def __init__(self):
        Msg.__init__(self, "System Exclusive Universal Message", 0b1111)
        self.handlers = [SysexGeneralInfo(), SysexQuneoPreset(), SysexDump()]

    def process(self, status_byte, dev):
        if not self.accepts(status_byte):
            return False
        non_rt = read_byte(dev)
        # TODO fix for general sysex, not just non-realtime
        if non_rt != 0x7e:
            return False
        channel = read_byte(dev)
        subid1 = read_byte(dev)
        subid2 = read_byte(dev)

        for handler in self.handlers:
            if handler.process(channel, subid1, subid2, dev):
                assert read_byte(dev) == 0xf7 # sysex end
                return True
        return False


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
