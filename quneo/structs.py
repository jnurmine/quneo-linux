#!/bin/env python
# -*- coding: iso-8859-15 -*-
# Python version (C) 2012-2015 J. Nurminen <slinky@iki.fi>

# based on "sysexCompiler_1.1.x_ForumRelease" 
# copyright 2012 Keith McMillen Instruments
# original author - daniel mcanulty <dan@keithmcmillen.com>

# structs for firmware 1.2.x
# the order is relevant!!!


TRANSPORT_BUTTONS = "TransportButtons"
PADS = "Pads"
LR_BUTTONS = "LeftRightButtons"
ROTARIES = "Rotaries"
LONG_SLIDERS = "LongSliders"
H_SLIDERS = "HSliders"
V_SLIDERS = "VSliders"
UD_BUTTONS = "UpDownButtons"
RHOMBUS_BUTTONS = "RhombusButtons"
MODE_BUTTONS = "ModeButtons"

pads = [
        "enableGrid",
        "padChannel",
        "outDmNote",
        "outDmNotePressMode",
        "outDmPress",
        "outDmPressValue",
        "outDmVelocityValue",
        "outDmXCC",
        "outDmXYReturn",
        "outDmXReturn",
        "outDmYCC",
        "outDmYReturn",
        "padSensitivityPerPad",

        # NOTE: this is shared. supports
        # multiple channels in the pad grid
        # if supported by the editor?
        "padChannel",
        "outGmNoteNW",
        "outGmNotePressModeNW",
        "outGmPressNW",
        "outGmPressValueNW",
        "outGmVelocityValueNW",

        "padChannel",
        "outGmNoteNE",
        "outGmNotePressModeNE",
        "outGmPressNE",
        "outGmPressValueNE",
        "outGmVelocityValueNE",

        "padChannel",
        "outGmNoteSE",
        "outGmNotePressModeSE",
        "outGmPressSE",
        "outGmPressValueSE",
        "outGmVelocityValueSE",

        "padChannel",
        "outGmNoteSW",
        "outGmNotePressModeSW",
        "outGmPressSW",
        "outGmPressValueSW",
        "outGmVelocityValueSW",
        ]


def build_rotaries():
    # repepetititition helper
    rotaries = []
    rotary_params = ["Channel", "outLocation", "outNote", "outNotePressMode",
            "outPress", "outPressValue", "outVelocityValue",
            "outLocPassThruRange", "outDirection", "outDirectionEnable",
            "outSpeed"]

    for bank in xrange(1, 5):
        for parameter in rotary_params:
            rotaries.append("rB%s%s" % (bank, parameter))
    return rotaries

def build_longsliders():
    # repepetititition helper
    longsliders = []
    longslider_params = [
            "Channel", "outLocation", "outNote", "outNotePressMode",
            "outPress", "outPressValue", "outVelocityValue",
            "outLocPassThruRange", "outWidth"]

    for bank in xrange(1,5):
        for parameter in longslider_params:
            longsliders.append("lB%s%s" % (bank, parameter))
    return longsliders


def build_hsliders():
    # repepetititition helper
    hsliders = []
    hslider_params = [
            "Channel", "outLocation", "outNote", "outNotePressMode",
            "outPress", "outPressValue", "outVelocityValue",
            "outLocPassThruRange"]

    for bank in xrange(1,5):
        for parameter in hslider_params:
            hsliders.append("hB%s%s" % (bank, parameter))
    return hsliders


def build_vsliders():
    # repepetititition helper
    vsliders = []
    vslider_params = [
            "Channel", "outLocation", "outNote", "outNotePressMode",
            "outPress", "outPressValue", "outVelocityValue",
            "outLocPassThruRange"]

    for bank in xrange(1,5):
        for parameter in vslider_params:
            vsliders.append("vB%s%s" % (bank, parameter))
    return vsliders


lrswitches = [
        "leftrightEnableSwitch",

        "leftrightChannel",
        "leftrightLOutNote",
        "leftrightLOutNotePressMode",
        "leftrightLOutPress",
        "leftrightLOutPressValue",
        "leftrightLOutVelocityValue",

        "leftrightChannel",
        "leftrightROutNote",
        "leftrightROutNotePressMode",
        "leftrightROutPress",
        "leftrightROutPressValue",
        "leftrightROutVelocityValue",
        ]

udswitches = [
        "updownEnableSwitch",
        "updownBankControl",

        "updownChannel",
        "updownUOutNote",
        "updownUOutNotePressMode",
        "updownUOutPress",
        "updownUOutPressValue",
        "updownUOutVelocityValue",

        "updownChannel",
        "updownDOutNote",
        "updownDOutNotePressMode",
        "updownDOutPress",
        "updownDOutPressValue",
        "updownDOutVelocityValue",
        ]

rhswitches = [
        "rhombusEnableSwitch",
        "rhombusBankControl",
        "rhombusInNoteG",
        "rhombusInNoteR",
        "rhombusChannel",

        "rhombusOutNote",
        "rhombusOutNotePressMode",
        "rhombusOutPress",
        "rhombusOutPressValue",
        "rhombusOutVelocityValue",
        ]

tbuttons = [
        "transportChannel",
        "transportOutNote",
        "transportOutNotePressMode",
        "transportOutPress",
        "transportOutPressValue",
        "transportOutVelocityValue",
        ]

mswitches = [
        "modeOutVelocityValue",
        "modeEnableSwitch",
        "modeChannel",
        "modeOutNote",
        "modeOutPress",
        ]

globalpaths = [
        [PADS,'padBankChangeMode'],

        # input channels
        [H_SLIDERS,'hSliderInChannel'],
        [LR_BUTTONS,'leftrightInChannel'],
        [LONG_SLIDERS,'lSliderInChannel'],
        [PADS, 'padDrumInChannel'],
        [PADS, 'padGridDiscreteInChannel'],
        [PADS, 'padGridDualInChannel'],
        [RHOMBUS_BUTTONS, 'rhombusInChannel'],
        [ROTARIES, 'rotaryInChannel'],
        [TRANSPORT_BUTTONS, 'transportInChannel'],
        [UD_BUTTONS, 'updownInChannel'],
        [V_SLIDERS, 'vSliderInChannel'],

        # transpose intervals
        [PADS,'bank1TransposeInterval'],
        [PADS,'bank2TransposeInterval'],
        [PADS,'bank3TransposeInterval'],
        [PADS,'bank4TransposeInterval'],

        # thresholds
        [V_SLIDERS,'vSliderOffThreshold'],
        [V_SLIDERS,'vSliderOnThreshold'],
        [UD_BUTTONS,'updownOffThreshold'],
        [UD_BUTTONS,'updownOnThreshold'],
        [TRANSPORT_BUTTONS,'transportOffThreshold'],
        [TRANSPORT_BUTTONS,'transportOnThreshold'],
        [ROTARIES,'rotaryOffThreshold'],
        [ROTARIES,'rotaryOnThreshold'],
        [RHOMBUS_BUTTONS,'rhombusOffThreshold'],
        [RHOMBUS_BUTTONS,'rhombusOnThreshold'],
        [MODE_BUTTONS,'modeOffThreshold'],
        [MODE_BUTTONS,'modeOnThreshold'],
        [LONG_SLIDERS,'lSliderOffThreshold'],
        [LONG_SLIDERS,'lSliderOnThreshold'],
        [LR_BUTTONS,'leftrightOffThreshold'],
        [LR_BUTTONS,'leftrightOnThreshold'],
        [H_SLIDERS,'hSliderOffThreshold'],
        [H_SLIDERS,'hSliderOnThreshold'],
        [PADS,'padOffset'],
        [PADS,'padOffThreshold'],
        [PADS,'padOnThreshold'],
        [PADS,'cornerIsolation'],

        # sensitivities
        [PADS,'padSensitivity'],
        [ROTARIES,'rotarySensitivity'],
        [LONG_SLIDERS,'lSliderSensitivity'],
        [H_SLIDERS,'hSliderSensitivity'],
        [V_SLIDERS,'vSliderSensitivity'],
        [LR_BUTTONS,'leftrightSensitivity'],
        [UD_BUTTONS,'updownSensitivity'],
        [RHOMBUS_BUTTONS,'rhombusSensitivity'],
        [TRANSPORT_BUTTONS,'transportSensitivity'],
        [MODE_BUTTONS,'modeSensitivity'],

        # LED controls
        [PADS,'localLEDControl'],
        [ROTARIES,'rotaryLocalLEDControl'],
        [LONG_SLIDERS,'lSliderLocalLEDControl'],
        [H_SLIDERS,'hSliderLocalLEDControl'],
        [V_SLIDERS,'vSliderLocalLEDControl'],
        [LR_BUTTONS,'leftrightLocalLEDControl'],
        [UD_BUTTONS,'updownLocalLEDControl'],
        [RHOMBUS_BUTTONS,'rhombusLocalLEDControl'],
        [TRANSPORT_BUTTONS,'transportLocalLEDControl'],
        [MODE_BUTTONS,'modeLocalLEDControl'],
        ]
