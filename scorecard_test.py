#!/usr/bin/env python

import unittest

from box import Box
from scorecard import Scorecard


class ScorecardTest(unittest.TestCase):
    def test_scoring_boxes(self):
        sc = Scorecard()

        def assert_scoring_boxes(roll, expected_boxes):
            bits = sc.get_array_scoring(roll)
            boxes = [b for b in Box if bits[b.to_index()] and b.name != 'NONE']
            assert(boxes == expected_boxes)

        assert_scoring_boxes([1,2,3,1,2],
                             [Box.ACES, Box.TWOS, Box.THREES, Box.CHANCE])
        assert_scoring_boxes([6,6,6,6,6],
                             [Box.SIXES, Box.KIND3, Box.KIND4, Box.YAHTZEE, Box.CHANCE])


if __name__ == '__main__':
    unittest.main()
