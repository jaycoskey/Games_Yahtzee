#!/usr/bin/env python

import unittest

from util import Util


class LongestConsecutiveSequenceTest(unittest.TestCase):
    def test_consecutive_dice(self):
        assert(Util.longest_consecutive_sequence([1]).tup()         == (1,1))
        assert(Util.longest_consecutive_sequence([1,2]).tup()       == (1,2))
        assert(Util.longest_consecutive_sequence([1,2,3]).tup()     == (1,3))
        assert(Util.longest_consecutive_sequence([1,2,3,4]).tup()   == (1,4))
        assert(Util.longest_consecutive_sequence([1,2,3,4,5]).tup() == (1,5))

        assert(Util.longest_consecutive_sequence([1,2,3,4,5]).min == 1)
        assert(Util.longest_consecutive_sequence([1,2,3,4,5]).max == 5)
        assert(Util.longest_consecutive_sequence([1,2,3,4,5]).contains(3))
        assert(not Util.longest_consecutive_sequence([1,2,3,4,5]).contains(6))
        assert(Util.longest_consecutive_sequence([1,2,3,4,5]).distance(5) == 0)
        assert(Util.longest_consecutive_sequence([1,2,3,4,5]).distance(6) == 1)

    def test_consecutive_length_1(self):
        assert(Util.longest_consecutive_sequence([1,1,1,1,1]).tup() == (1,1))
        assert(Util.longest_consecutive_sequence([1,3,5,7,9]).tup() == (1,1))

        assert(Util.longest_consecutive_sequence([1,1,1,1,1]).distance(1) == 0)
        assert(Util.longest_consecutive_sequence([1,1,1,1,1]).distance(2) == 1)
        assert(Util.longest_consecutive_sequence([1,1,1,1,1]).distance(3) == 2)
        assert(Util.longest_consecutive_sequence([1,1,1,1,1]).distance(6) == 5)

    def test_consecutive_length_2(self):
        assert(Util.longest_consecutive_sequence([1,2,6,6,6]).tup() == (1,2))
        assert(Util.longest_consecutive_sequence([1,3,4,6,6]).tup() == (3,2))
        assert(Util.longest_consecutive_sequence([1,3,3,5,6]).tup() == (5,2))

    def test_consecutive_length_3(self):
        assert(Util.longest_consecutive_sequence([1,2,3,6,6]).tup() == (1,3))
        assert(Util.longest_consecutive_sequence([1,3,4,5,5]).tup() == (3,3))
        assert(Util.longest_consecutive_sequence([1,1,3,4,5]).tup() == (3,3))

    def test_consecutive_length_4(self):
        assert(Util.longest_consecutive_sequence([1,2,3,4,4]).tup() == (1,4))
        assert(Util.longest_consecutive_sequence([1,2,3,4,6]).tup() == (1,4))
        assert(Util.longest_consecutive_sequence([1,3,4,5,6]).tup() == (3,4))
        assert(Util.longest_consecutive_sequence([3,3,4,5,6]).tup() == (3,4))

        assert(Util.longest_consecutive_sequence([3,3,4,5,6]).distance(1) == 2)
        assert(Util.longest_consecutive_sequence([3,3,4,5,6]).distance(2) == 1)
        assert(Util.longest_consecutive_sequence([3,3,4,5,6]).distance(3) == 0)


if __name__ == '__main__':
    unittest.main()
