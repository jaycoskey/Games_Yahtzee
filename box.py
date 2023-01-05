#!/usr/bin/env python

from enum import IntEnum


class Box(IntEnum):
    NONE           = 0

    ACES           = 1   # B1
    TWOS           = 2   # B2
    THREES         = 3   # B3
    FOURS          = 4   # B4
    FIVES          = 5   # B5
    SIXES          = 6   # B6

    KIND3          = 7   # K3
    KIND4          = 8   # K4
    FULL_HOUSE     = 9   # FH
    STRAIGHT_SMALL = 10  # SS
    STRAIGHT_LARGE = 11  # LS
    YAHTZEE        = 12  # Y
    CHANCE         = 13  # C

    @staticmethod
    def from_code(s):
        mapping = {'B1': Box.ACES,  'B2': Box.TWOS,  'B3': Box.THREES,
                'B4': Box.FOURS, 'B5': Box.FIVES, 'B6': Box.SIXES,
                'K3': Box.KIND3, 'K4': Box.KIND4, 'FH': Box.FULL_HOUSE,
                'SS': Box.STRAIGHT_SMALL, 'LS': Box.STRAIGHT_LARGE,
                'Y':  Box.YAHTZEE, 'C': Box.CHANCE}
        if s in mapping:
            return mapping[s]
        else:
            return Box.NONE

    @staticmethod
    def nonnone_boxes():
        return [b for b in Box if b != Box.NONE]

    @staticmethod
    def nonnone_count():
        return len(Box) - 1

    def to_index(b):
        return b.value - 1
