#!/bin/env python
# -*- coding: iso-8859-15 -*-
# Python version (C) 2012 J. Nurminen <slinky@iki.fi>

# based on "sysexCompiler_1.1.x_ForumRelease" 
# copyright 2012 Keith McMillen Instruments
# original author - daniel mcanulty <dan@keithmcmillen.com>

# structs for firmware 1.1.x
# the order is relevant

pads = [
        "enableGrid",
        "padChannel",
        "outDmNote",
        "outDmPress",
        "outDmVelocity",
        "outDmXCC",
        "outDmXYReturn",
        "outDmYCC",
        "padSensitivityPerPad",

        "padChannel",
        "outGmNoteNW",
        "outGmPressNW",
        "outGmVelocityNW",

        "padChannel",
        "outGmNoteNE",
        "outGmPressNE",
        "outGmVelocityNE",

        "padChannel",
        "outGmNoteSE",
        "outGmPressSE",
        "outGmVelocitySE",

        "padChannel",
        "outGmNoteSW",
        "outGmPressSW",
        "outGmVelocitySW",
        ]

rotaries = [
        "rB1Channel",
        "rB1outLocation",
        "rB1outNote",
        "rB1outPress",
        "rB1outVelocity",
        "rB1outLocPassThruRange",

        "rB1outDirection",
        "rB1outDirectionEnable",
        "rB1outSpeed",

        "rB2Channel",
        "rB2outLocation",
        "rB2outNote",
        "rB2outPress",
        "rB2outVelocity",
        "rB2outLocPassThruRange",

        "rB2outDirection",
        "rB2outDirectionEnable",
        "rB2outSpeed",

        "rB3Channel",
        "rB3outLocation",
        "rB3outNote",
        "rB3outPress",
        "rB3outVelocity",
        "rB3outLocPassThruRange",

        "rB3outDirection",
        "rB3outDirectionEnable",
        "rB3outSpeed",

        "rB4Channel",
        "rB4outLocation",
        "rB4outNote",
        "rB4outPress",
        "rB4outVelocity",
        "rB4outLocPassThruRange",

        "rB4outDirection",
        "rB4outDirectionEnable",
        "rB4outSpeed",
        ]

longsliders = [
        "lB1Channel",
        "lB1outLocation",
        "lB1outNote",
        "lB1outPress",
        "lB1outVelocity",
        "lB1outLocPassThruRange",

        "lB1outWidth",

        "lB2Channel",
        "lB2outLocation",
        "lB2outNote",
        "lB2outPress",
        "lB2outVelocity",
        "lB2outLocPassThruRange",

        "lB2outWidth",

        "lB3Channel",
        "lB3outLocation",
        "lB3outNote",
        "lB3outPress",
        "lB3outVelocity",
        "lB3outLocPassThruRange",

        "lB3outWidth",

        "lB4Channel",
        "lB4outLocation",
        "lB4outNote",
        "lB4outPress",
        "lB4outVelocity",
        "lB4outLocPassThruRange",

        "lB4outWidth",
        ]


hsliders = [
        "hB1Channel",
        "hB1outLocation",
        "hB1outNote",
        "hB1outPress",
        "hB1outVelocity",
        "hB1outLocPassThruRange",

        "hB2Channel",
        "hB2outLocation",
        "hB2outNote",
        "hB2outPress",
        "hB2outVelocity",
        "hB2outLocPassThruRange",

        "hB3Channel",
        "hB3outLocation",
        "hB3outNote",
        "hB3outPress",
        "hB3outVelocity",
        "hB3outLocPassThruRange",

        "hB4Channel",
        "hB4outLocation",
        "hB4outNote",
        "hB4outPress",
        "hB4outVelocity",
        "hB4outLocPassThruRange",
        ]

vsliders = [
        "vB1Channel",
        "vB1outLocation",
        "vB1outNote",
        "vB1outPress",
        "vB1outVelocity",
        "vB1outLocPassThruRange",

        "vB2Channel",
        "vB2outLocation",
        "vB2outNote",
        "vB2outPress",
        "vB2outVelocity",
        "vB2outLocPassThruRange",

        "vB3Channel",
        "vB3outLocation",
        "vB3outNote",
        "vB3outPress",
        "vB3outVelocity",
        "vB3outLocPassThruRange",

        "vB4Channel",
        "vB4outLocation",
        "vB4outNote",
        "vB4outPress",
        "vB4outVelocity",
        "vB4outLocPassThruRange",
        ]

lrswitches = [
        "leftrightEnableSwitch",

        "leftrightChannel",
        "leftrightLOutNote",
        "leftrightLOutPress",
        "leftrightLOutVelocity",

        "leftrightChannel",
        "leftrightROutNote",
        "leftrightROutPress",
        "leftrightROutVelocity",
        ]

udswitches = [
        "updownEnableSwitch",
        "updownBankControl",

        "updownChannel",
        "updownUOutNote",
        "updownUOutPress",
        "updownUOutVelocity",


        "updownChannel",
        "updownDOutNote",
        "updownDOutPress",
        "updownDOutVelocity",
        ]

rhswitches = [
        "rhombusEnableSwitch",
        "rhombusBankControl",
        "rhombusInNoteG",
        "rhombusInNoteR",

        "rhombusChannel",
        "rhombusOutNote",
        "rhombusOutPress",
        "rhombusOutVelocity",
        ]

tbuttons = [
        "transportChannel",
        "transportOutNote",
        "transportOutPress",
        "transportOutVelocity",
        ]

mswitches = [
        "modeOutVelocity",
        "modeEnableSwitch",
        "modeChannel",
        "modeOutNote",
        "modeOutPress",
        ]

globalpaths = [
        # thresholds
        ['VSliders','vSliderOffThreshold'],
        ['VSliders','vSliderOnThreshold'],
        ['UpDownButtons','updownOffThreshold'],
        ['UpDownButtons','updownOnThreshold'],
        ['TransportButtons','transportOffThreshold'],
        ['TransportButtons','transportOnThreshold'],
        ['Rotaries','rotaryOffThreshold'],
        ['Rotaries','rotaryOnThreshold'],
        ['RhombusButtons','rhombusOffThreshold'],
        ['RhombusButtons','rhombusOnThreshold'],
        ['ModeButtons','modeOffThreshold'],
        ['ModeButtons','modeOnThreshold'],
        ['LongSliders','lSliderOffThreshold'],
        ['LongSliders','lSliderOnThreshold'],
        ['LeftRightButtons','leftrightOffThreshold'],
        ['LeftRightButtons','leftrightOnThreshold'],
        ['HSliders','hSliderOffThreshold'],
        ['HSliders','hSliderOnThreshold'],
        ['Pads','padOffset'],
        ['Pads','padOffThreshold'],
        ['Pads','padOnThreshold'],
        ['Pads','cornerIsolation'],
        # sensitivities
        ['Pads','padSensitivity'],
        ['Rotaries','rotarySensitivity'],
        ['LongSliders','lSliderSensitivity'],
        ['HSliders','hSliderSensitivity'],
        ['VSliders','vSliderSensitivity'],
        ['LeftRightButtons','leftrightSensitivity'],
        ['UpDownButtons','updownSensitivity'],
        ['RhombusButtons','rhombusSensitivity'],
        ['TransportButtons','transportSensitivity'],
        ['ModeButtons','modeSensitivity'],
        # LED controls
        ['Pads','localLEDControl'],
        ['Rotaries','rotaryLocalLEDControl'],
        ['LongSliders','lSliderLocalLEDControl'],
        ['HSliders','hSliderLocalLEDControl'],
        ['VSliders','vSliderLocalLEDControl'],
        ['LeftRightButtons','leftrightLocalLEDControl'],
        ['UpDownButtons','updownLocalLEDControl'],
        ['RhombusButtons','rhombusLocalLEDControl'],
        ['TransportButtons','transportLocalLEDControl'],
        ['ModeButtons','modeLocalLEDControl'],
        ]
