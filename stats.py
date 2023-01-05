#!/usr/bin/env python

from dataclasses import dataclass
from itertools import combinations_with_replacement as cwr
from itertools import product
from statistics import mean
from typing import Callable, List

import numpy as np
import numpy.typing as npt

from box import Box
from scorecard import Scorecard
from util import Util


class OptimalPlay:
    # The following data is from Wikipedia's page on Yahtzee.
    AVG_BOX_SCORES:npt.NDArray = np.array(
        [1.88, 5.28, 8.57, 12.16, 15.69, 19.19,
        21.66, 13.10, 22.59, 29.46, 32.71, 16.87, 22.01])
    ZERO_BOX_SCORE_PROB:npt.NDArray = np.array([
        0.1084, 0.0180, 0.0095, 0.0060, 0.0050, 0.0053,
        0.0326, 0.3634, 0.0963, 0.0180, 0.1822, 0.6626, 0.0])

    UPPER_BONUS:float   = 23.84
    YAHTZEE_BONUS:float = 9.58

    ZERO_UPPER_BONUS_PROB:float   = 0.3188
    ZERO_YAHTZEE_BONUS_PROB:float = 0.9176


def inds_to_permutation(inds):
    def permutation(xs):
        return [xs[inds[0]], xs[inds[1]], xs[inds[2]],
                xs[inds[3]], xs[inds[4]]]
    return permutation


@Util.init_static
class Stats:
    """Some types of data used in this class:
      * roll: Roll of five dice.
      * rid: Roll ID. An integral index for a 5-dice roll outcome, from the generator
            product(range(1, 7), repeat=5)
      * reroll = A subset of the dice to be re-rolled, with zero-based indices.
      * rrid = Re-roll ID, ranging from 0 to 31 = 2^5 - 1.
            rrid values are the indices of the list Stats.stat_rerolls.
      * sroll: A sorted roll, dice values numerically sorted.
            There are 7,776 (= 6**5) distinct ways to roll 5 dice, but only 252 sorted outcomes.
            With this equivalence relation, (5,4,3,2,1) is considered equivalent to (1,2,3,4,5).
            Note that Yahtzee scores are independent of dice ordering.
      * srid = Sorted Roll ID, with values from 0 to 251.
            The 252 sorted outcomes, or srolls, are indexed via the generator
                itertools.combinations_with_replacement(range(1, 7), repeat=5)
      * delta = Delta from OptimalScore = Score - Mean Score using Optimal Strategy
            One possible strategy is to seek the maximum box score in each round, but this
            would place undue emphasis on pursuing FIVES and SIXES boxes before the ACES box.
    """

    @classmethod
    def _init_static(cls):
        stat_srolls = [sroll for sroll in cwr(range(1, 7), 5)]
        setattr(cls, 'stat_srolls', stat_srolls)
        # ----------------------------------------
        stat_sroll_to_srid = { sroll: k
                               for k, sroll in enumerate(cwr(range(1, 7), 5)) }
        setattr(cls, 'stat_sroll_to_srid', stat_sroll_to_srid)
        # ----------------------------------------
        stat_rerolls = [Util.reverse([(4 - pos) for pos in range(5)
                        if (k // 2**pos) % 2 == 1])
                        for k in range(0, 32)]
        setattr(cls, 'stat_rerolls', stat_rerolls)
        # ----------------------------------------
        """sroll, re-roll --> probability of subsequent sroll outcomes.
           shape=(srid, rrid, srid) = (252, 32, 252)
        """
        stat_reroll_prob = np.zeros(shape=(252, 32, 252), dtype=np.double)
        setattr(cls, 'stat_reroll_prob', stat_reroll_prob)
        for srid in range(252):
            for rrid in range(32):
                reroll = stat_rerolls[rrid]
                length = len(reroll)
                if length == 0:
                    stat_reroll_prob[srid, rrid, srid] = 1
                elif length == 1:
                    roll2 = list(stat_srolls[srid])
                    for d1 in range(1, 7):
                        roll2[reroll[0]] = d1
                        srid2 = stat_sroll_to_srid[tuple(sorted(roll2))]
                        stat_reroll_prob[srid, rrid, srid2] += 1/6
                elif length == 2:
                    roll2 = list(stat_srolls[srid])
                    for (d1,d2) in product(range(1, 7), repeat=2):
                        roll2[reroll[0]] = d1
                        roll2[reroll[1]] = d2
                        srid2 = stat_sroll_to_srid[tuple(sorted(roll2))]
                        stat_reroll_prob[srid, rrid, srid2] = 1/(6**2)
                elif length == 3:
                    roll2 = list(stat_srolls[srid])
                    for (d1,d2,d3) in product(range(1, 7), repeat=3):
                        roll2[reroll[0]] = d1
                        roll2[reroll[1]] = d2
                        roll2[reroll[2]] = d3
                        srid2 = stat_sroll_to_srid[tuple(sorted(roll2))]
                        stat_reroll_prob[srid, rrid, srid2] = 1/(6**3)
                elif length == 4:
                    roll2 = list(stat_srolls[srid])
                    for (d1,d2,d3,d4) in product(range(1, 7), repeat=4):
                        roll2[reroll[0]] = d1
                        roll2[reroll[1]] = d2
                        roll2[reroll[2]] = d3
                        roll2[reroll[3]] = d4
                        srid2 = stat_sroll_to_srid[tuple(sorted(roll2))]
                        stat_reroll_prob[srid, rrid, srid2] = 1/(6**4)
                else:  # length == 5
                    assert(length ==5)
                    roll2 = list(stat_srolls[srid])
                    for (d1,d2,d3,d4,d5) in product(range(1, 7), repeat=5):
                        roll2[reroll[0]] = d1
                        roll2[reroll[1]] = d2
                        roll2[reroll[2]] = d3
                        roll2[reroll[3]] = d4
                        roll2[reroll[4]] = d5
                        srid2 = stat_sroll_to_srid[tuple(sorted(roll2))]
                        stat_reroll_prob[srid, rrid, srid2] = 1/(6**5)
        # ----------------------------------------
        """Given a roll, return the sorted roll data:
             sroll, sorted roll ID, sort and unsort functions.
        """
        stat_roll_to_sroll_data = {}
        setattr(cls, 'stat_roll_to_sroll_data', stat_roll_to_sroll_data)
        for roll in product(range(1, 7), repeat=5):
            zipped = zip(roll, range(5))
            szipped = sorted(zipped, key=lambda pair: pair[0])
            sroll = list(map(lambda pair: pair[0], szipped))
            srid = stat_sroll_to_srid[tuple(sroll)]
            inds = list(map(lambda x: x[1], szipped))
            uinds = [inds.index(k) for k in range(5)]
            f_sort = inds_to_permutation(inds)
            f_unsort = inds_to_permutation(uinds)
            stat_roll_to_sroll_data[roll] = (sroll, srid, inds, uinds,
                                             f_sort, f_unsort)
        # ----------------------------------------
        """sroll, choice of scoring box --> resulting box score.
           So score_stats.shape = (252, 13), and dtype=int.
        """
        stat_scores = np.zeros(shape=(252, 13), dtype=int)
        setattr(cls, 'stat_scores', stat_scores)
        for k, sroll in enumerate(cwr(range(1, 7), 5)):
            for box in Box.nonnone_boxes():
                score = Scorecard().get_box_score(box, sroll)[0]
                stat_scores[k, box.to_index()] = score

    @staticmethod
    def get_exp_reroll_delta(srid, rrid, boxes_unused):
        # Return expected delta score from srid, re-rolling rrid
        result = mean(
            [Stats.stat_reroll_prob[76, 7, tgt_srid]
                * max([Stats.stat_scores[tgt_srid, box.to_index()]
                       for box in boxes_unused])
            for tgt_srid in range(252)
            ])
        return result
