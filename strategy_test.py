#!/usr/bin/env python

import unittest

from box import Box
from strategy import Strategy


class StrategyTest(unittest.TestCase):
    @staticmethod
    def assert_reroll_for_box(roll, box, expected):
        observed = Strategy.goals_to_rerolls(roll, [box])[box]
        if observed != expected:
            print(f'Expected {expected}, but observed {observed}')
        assert(observed == expected)

    def test_reroll_for_box(self):
        StrategyTest.assert_reroll_for_box([1,1,2,3,3], Box.ACES,   [2,3,4])
        StrategyTest.assert_reroll_for_box([1,1,2,3,3], Box.TWOS,   [0,1,3,4])
        StrategyTest.assert_reroll_for_box([1,1,2,3,3], Box.THREES, [0,1,2])
        StrategyTest.assert_reroll_for_box([4,1,4,3,4], Box.FOURS,  [1,3])
        StrategyTest.assert_reroll_for_box([5,5,5,5,5], Box.FIVES,  [])
        StrategyTest.assert_reroll_for_box([1,2,3,4,5], Box.SIXES,  [0,1,2,3,4])

        StrategyTest.assert_reroll_for_box([1,2,3,4,5], Box.KIND3,  [0,1,2,3])

        StrategyTest.assert_reroll_for_box([1,2,3,4,5], Box.KIND4,  [0,1,2,3])

        StrategyTest.assert_reroll_for_box([1,1,1,1,1], Box.FULL_HOUSE, [3, 4])
        StrategyTest.assert_reroll_for_box([1,1,2,2,3], Box.FULL_HOUSE, [4])
        StrategyTest.assert_reroll_for_box([1,1,1,2,3], Box.FULL_HOUSE, [3])

        StrategyTest.assert_reroll_for_box([1,2,3,6,6], Box.STRAIGHT_SMALL, [3,4])
        StrategyTest.assert_reroll_for_box([1,2,4,6,6], Box.STRAIGHT_SMALL, [3,4])
        StrategyTest.assert_reroll_for_box([2,3,3,3,4], Box.STRAIGHT_SMALL, [2,3])

        StrategyTest.assert_reroll_for_box([1,2,3,4,5], Box.STRAIGHT_LARGE, [])
        StrategyTest.assert_reroll_for_box([1,2,3,4,6], Box.STRAIGHT_LARGE, [4])
        StrategyTest.assert_reroll_for_box([1,2,3,4,6], Box.STRAIGHT_LARGE, [4])
        StrategyTest.assert_reroll_for_box([1,2,4,5,6], Box.STRAIGHT_LARGE, [0])
        StrategyTest.assert_reroll_for_box([1,2,3,4,4], Box.STRAIGHT_LARGE, [4])

        StrategyTest.assert_reroll_for_box([1,1,3,5,5], Box.STRAIGHT_LARGE, [1,4])
        StrategyTest.assert_reroll_for_box([2,4,4,4,6], Box.STRAIGHT_LARGE, [2,3])

        StrategyTest.assert_reroll_for_box([1,2,3,4,5], Box.CHANCE, [0,1,2])


if __name__ == '__main__':
    unittest.main()
