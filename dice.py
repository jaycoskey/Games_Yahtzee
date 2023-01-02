#!/usr/bin/env python

from copy import copy
import random as r


class Dice:
    SIDES = 6
    COUNT = 5

    @staticmethod
    def reroll(roll, indices):
        result = copy(roll)
        for i in indices:
            result[i] = r.randint(1, Dice.SIDES)
        return result

    @staticmethod
    def roll():
        values = [r.randint(1, Dice.SIDES) for k in range(Dice.COUNT)]
        return values

    @staticmethod
    def seed(s):
        r.seed(s)
