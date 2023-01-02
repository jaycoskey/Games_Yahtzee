#!/usr/bin/env python

import unittest

from dice import Dice


class DiceTest(unittest.TestCase):
    def test_reroll(self):
        roll1 = Dice.roll()
        roll2 = Dice.reroll(roll1, [0,1,2,3,4])
        assert(roll1 != roll2)


if __name__ == '__main__':
    unittest.main()
