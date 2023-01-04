#!/usr/bin/env python

from collections import Counter, defaultdict
from copy import deepcopy
from statistics import mean

import numpy as np

from box import Box
from dice import Dice
from stats import OptimalPlay
from util import Util


class Strategy:
    DEFAULT_MC_ITERATIONS_ROLL1 = 6  # Number of times roll #2 (& beyond) is sampled
    DEFAULT_MC_ITERATIONS_ROLL2 = 6  # Number of times roll #3 is sampled

    @staticmethod
    def _get_delta_1_mean_by_goal(p, bs, n=DEFAULT_MC_ITERATIONS_ROLL1):
        def get_delta_mean_from_reroll(p, reroll1, n):
            return mean([get_delta_sample_from_reroll(p, reroll1) for _ in range(n)])

        def get_delta_sample_from_reroll(p, reroll1):
            player = deepcopy(p)
            player._reroll(reroll1)
            boxes_unused2 = player._scorecard.get_boxes_unused()
            g2s = Strategy._get_delta_2_mean_by_goal(player, boxes_unused2)
            score = max(g2s.values())
            return score

        assert(p._roll_num == 1)
        g2r = Strategy.goals_to_rerolls(p._roll, bs)
        g2s = {b: get_delta_mean_from_reroll(p, g2r[b], n) for b in bs}
        return g2s

    @staticmethod
    def _get_delta_2_mean_by_goal(p, bs, n=DEFAULT_MC_ITERATIONS_ROLL2):
        def get_delta_mean_from_reroll(p, reroll2, n):
            return mean([get_delta_sample_from_reroll(p, reroll2)
                               for _ in range(n)])

        def get_delta_sample_from_reroll(p, reroll2):
            player = deepcopy(p)
            player._reroll(reroll2)
            final_outcomes = {
                box: player._scorecard.get_box_score(box, player._roll)[0]
                         - OptimalPlay.AVG_BOX_SCORES[box.to_index()]
                for box in player._scorecard.get_boxes_unused()
                }
            score = max(final_outcomes.values())
            return score

        assert(p._roll_num == 2)
        g2r = Strategy.goals_to_rerolls(p._roll, bs)
        g2s = {b: get_delta_mean_from_reroll(p, g2r[b], n) for b in bs}
        return g2s

    @staticmethod
    def _get_reroll_by_pip(roll, target_pip_value):
        """Get the re-roll that re-rolls all dice other than those with the target pip value.
        """
        reroll = [k for k in range(Dice.COUNT) if roll[k] != target_pip_value]
        return reroll

    # Rough guide to which dice to re-roll.
    @staticmethod
    def goals_to_rerolls(roll, boxes):
        """Returns which dice to re-roll, based on heuristics. Return values are zero-based indices.
        TODO: Handle multiple simultaneous goals (e.g., a fallback goal). Consider risk/reward payoff.
              Example: When roll1 = [3,3,3,6,6] and only Box.K3 is open, re-roll the 3s or the 6s?
        TODO: Handling of the impact of the Upper Bonus and Yahtzee Bonus on choice of re-rolls.
        """
        result = defaultdict(list)
        for box in boxes:
            if box in [Box.ACES, Box.TWOS, Box.THREES,
                       Box.FOURS, Box.FIVES, Box.SIXES]:
                result[box] = Strategy._get_reroll_by_pip(roll, box.value)
                continue

            counter = Counter(roll)
            pips = list(counter.keys())
            counts = sorted(counter.values())
            count_max = max(counts)
            lcs = Util.longest_consecutive_sequence(roll)
            modes = [k for k in pips if counter[k] == count_max]
            mode_max = max(modes)

            if box == Box.KIND3 or box == Box.KIND4:
                if count_max == 3:
                    reroll = [k for k in range(Dice.COUNT)
                              if roll[k] not in modes and roll[k] < 4]
                    result[box] = reroll
                    continue
                else:
                    result[box] = Strategy._get_reroll_by_pip(roll, mode_max)
                    continue
            elif box == Box.KIND4:
                if count_max == 4:
                    reroll = [k for k in range(Dice.COUNT)
                              if roll[k] not in modes and roll[k] < 4]
                    result[box] = reroll
                    continue
                else:
                    result[box] = Strategy.nontarget_dice(roll, mode_max)
                    continue
            elif box == Box.FULL_HOUSE:
                if counts == [2, 3]:
                    result[box] = []
                    continue
                elif counts == [5]:  # Yahtzee
                    result[box] = [3, 4]
                    continue
                elif counts == [1, 4]:  # Four of a kind
                    non_k4 = [k for k in range(Dice.COUNT) if roll[k] != mode_max]
                    k4s = [k for k in range(Dice.COUNT) if roll[k] == mode_max]
                    result[box] = non_k4 + [k4s[0]]
                    continue
                else:
                    # Re-roll all except the two most frequent values
                    keep = [k for k,v in sorted(counter.items(),
                             key=lambda item: item[1])[-2:]]
                    reroll = [k for k in range(Dice.COUNT) if roll[k] not in keep]
                    result[box] = reroll
                    continue
            elif box == Box.STRAIGHT_SMALL:
                if lcs.length >= 4:
                    result[box] = []
                    continue

                reroll_lcs_dupes = []
                if count_max > 1:
                    lcs_dupe_vals = [pip for pip, count in counter.items()
                                     if lcs.contains(pip) and counter[pip] > 1]
                    reroll_lcs_dupes = [k for k in range(Dice.COUNT)
                                        if (roll[k] in lcs_dupe_vals
                                            and k > roll.index(roll[k]))
                                        ]
                outsiders = [k for k in range(Dice.COUNT)
                             if lcs.distance(roll[k]) > 2
                             ]
                result[box] = reroll_lcs_dupes + outsiders
                continue
            elif box == Box.STRAIGHT_LARGE:
                if lcs.length >= 5:
                    result[box] = []
                    continue

                # Handle "double-inside" straights (e.g., roll=[1,1,3,3,5], box=STRAGHT_LARGE)
                if pips == [1, 3, 5] or pips == [2, 4, 6]:
                    result[box] = [k for k in range(Dice.COUNT) if k > roll.index(roll[k])]
                    continue

                reroll_lcs_dupes = []
                if count_max > 1:
                    lcs_dupe_vals = [pip for pip, count in counter.items()
                                     if lcs.contains(pip) and counter[pip] > 1]
                    reroll_lcs_dupes = [k for k in range(Dice.COUNT)
                                        if (roll[k] in lcs_dupe_vals
                                            and k > roll.index(roll[k]))
                                        ]
                outsiders = [k for k in range(Dice.COUNT)
                             if (lcs.length <= 3 and lcs.distance(roll[k]) > 2)
                                 or (lcs.length == 4 and lcs.distance(roll[k]) > 1)
                             ]
                result[box] = reroll_lcs_dupes + outsiders
                continue
            elif box == Box.YAHTZEE:
                if count_max == 5:
                    result[Box.YAHTZEE] = []
                    continue
                else:
                    result[box] = Strategy._get_reroll_by_pip(roll, mode_max)
                    continue
            elif box == Box.CHANCE:
                result[box] = [k for k in range(Dice.COUNT) if roll[k] < 4]
                continue
            else:
                raise ValueError('Unrecognized box: {box}')

        f_is_reroll_valid = lambda roll: all([0 <= x <= 4 for x in roll])
        is_result_valid = all([f_is_reroll_valid(reroll) for reroll in result.values()])
        if not is_result_valid:
            for b,r in result.items():
                print(f'Greedy roll for {b.name:<10} is {r}')
        return result
