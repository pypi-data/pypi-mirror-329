from enum import Enum

class WaveformType(Enum):
    SINE = "SIN"
    SQUARE = "SQU"
    RAMP = "RAMP"
    PULSE = "PULS"
    NOISE = "NOIS"
    DC = "DC"
    ARB = "ARB"  # Arbitrary


class AmplitudeUnit(Enum):
    VPP = "VPP"
    VRMS = "VRMS"
    DBM = "DBM"


class FrequencyUnit(Enum):
    HZ = "HZ"
    KHZ = "KHZ"
    MHZ = "MHZ"
