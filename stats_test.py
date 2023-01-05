#!/usr/bin/env python

import unittest

from itertools import combinations_with_replacement as cwr
from statistics import mean

from box import Box
from stats import Stats


class StatsTest(unittest.TestCase):
    def test_crw(self):
        assert(list(cwr(range(1, 7), 5))[76] == (1,2,3,4,5))

    def test_reroll_prob(self):
        EPS = 10e-6
        def eq_approx(a, b):
            return abs(a - b) < EPS

        def is_one_sixth(srid2):
            return eq_approx(1/6, Stats.stat_reroll_prob[76, 2, srid2])
        assert(all(map(is_one_sixth, [28, 63, 73, 76, 78, 79])))


    def test_rerolls(self):
        assert(Stats.stat_rerolls[0] == [])
        assert(Stats.stat_rerolls[1] == [4])
        assert(Stats.stat_rerolls[2] == [3])
        assert(Stats.stat_rerolls[3] == [3, 4])
        assert(Stats.stat_rerolls[7] == [2, 3, 4])
        assert(Stats.stat_rerolls[15] == [1, 2, 3, 4])
        assert(Stats.stat_rerolls[31] == [0, 1, 2, 3, 4])


    def test_score_stats(self):
        assert(Stats.stat_scores[0, 0] == 5)
        assert(Stats.stat_scores[251, 12] == 30)

        exp_rr_ds = Stats.get_exp_reroll_delta(76, 7, Box.nonnone_boxes())
        assert(exp_rr_ds > 0)


    def test_srolls(self):
        assert(Stats.stat_srolls[0] == (1, 1, 1, 1, 1))
        assert(Stats.stat_srolls[1] == (1, 1, 1, 1, 2))
        assert(Stats.stat_srolls[251] == (6, 6, 6, 6, 6))

        assert(Stats.stat_sroll_to_srid[(1, 1, 1, 1, 1)] == 0)
        assert(Stats.stat_sroll_to_srid[(1, 1, 1, 1, 2)] == 1)
        assert(Stats.stat_sroll_to_srid[(6, 6, 6, 6, 6)] == 251)


    def test_unsort(self):
        def test_unsort_impl(roll):
            (sroll, srid, inds, uinds, f_sort, f_unsort) = Stats.stat_roll_to_sroll_data[roll]
            assert(f_unsort(sroll) == list(roll))

        test_unsort_impl((1,2,3,4,5))
        test_unsort_impl((5,4,3,2,1))
        test_unsort_impl((3,1,4,5,2))


if __name__ == '__main__':
    unittest.main()
