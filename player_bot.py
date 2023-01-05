#!/usr/bin/env python

from box import Box
from player import Player
from stats import OptimalPlay, Stats
from strategy import Strategy


class Player_MonteCarlo_Fast(Player):
    """Player that decides re-rolls using cached probability and scoring data.
    Each box score is compared against "optimal" play,
    according to the Yahtzee article on Wikipedia.

    Implementation overview:
        (1) Map roll to sroll.
        (2) Determine optimal reroll on sroll, using Stats data.
        (3) Using unsort, map reroll on sorted dice back to reroll on initial dice ordering.
    """
    def _exec_policy(self):
        boxes_unused = self._scorecard.get_boxes_unused()
        if self._roll_num == 1:
            g2s = Strategy._get_delta_1_mean_by_goal(self, boxes_unused, n=36)
            box_goal1 = max(g2s, key=g2s.get)
            reroll1 = Strategy.goals_to_rerolls(self._roll, [box_goal1])[box_goal1]
            self._reroll(reroll1)
            return
        elif self._roll_num == 2:
            sroll_data = Stats.stat_roll_to_sroll_data[tuple(self._roll)]
            (sroll, srid, inds, uinds, f_sort, f_unsort) = sroll_data
            srr2d = { srrid: Stats.get_exp_reroll_delta(srid, srrid, boxes_unused)
                      for srrid in range(32) }
            srrid = max(srr2d, key=srr2d.get)
            sreroll2 = Stats.stat_rerolls[srrid]  # Re-roll using sroll ordering of dice
            reroll2 = list(map(lambda x: uinds.index(x), sreroll2))
            self._reroll(reroll2)
            return
        else:  # self._roll_num == 3
            outcomes = { box: self._scorecard.get_box_score(box, self._roll)[0]
                                  - OptimalPlay.AVG_BOX_SCORES[box.value - 1]
                         for box in boxes_unused
                         }
            scoring_box = max(outcomes, key=lambda b: outcomes[b])
            self._use_box(scoring_box)
            return

    def _report_summary(self):
        print(flush=True)
        self._scorecard.print(do_print_score=True)

    def _report_turn_beginning(self):
        print('.', end='', flush=True)


class Player_MonteCarlo_Slow(Player):
    """Player that simulates roll #2 and roll #3 to determine the best outcome.
    Each final box score is compared against the outcome of an optimal player,
    according to the Yahtzee article on Wikipedia.
    The number of simulated rolls is set by the DEFAULT_MC_ITERATIONS constants
    in class Strategy.
    """
    def _exec_policy(self):
        if self._roll_num == 1:
            boxes_unused = self._scorecard.get_boxes_unused()
            g2s = Strategy._get_delta_1_mean_by_goal(self, boxes_unused, n=36)
            box_goal1 = max(g2s, key=g2s.get)
            reroll1 = Strategy.goals_to_rerolls(self._roll, [box_goal1])[box_goal1]
            self._reroll(reroll1)
            return
        elif self._roll_num == 2:
            boxes_unused = self._scorecard.get_boxes_unused()
            g2s = Strategy._get_delta_2_mean_by_goal(self, boxes_unused, n=36)
            box_goal2 = max(g2s, key=g2s.get)
            reroll2 = Strategy.goals_to_rerolls(self._roll, [box_goal2])[box_goal2]
            self._reroll(reroll2)
            return
        else:  # self._roll_num == 3
            outcomes = { box: self._scorecard.get_box_score(box, self._roll)[0]
                                  - OptimalPlay.AVG_BOX_SCORES[box.to_index()]
                         for box in self._scorecard.get_boxes_unused()
                         }
            scoring_box = max(outcomes, key=lambda b: outcomes[b])
            self._use_box(scoring_box)
            return

    def _report_summary(self):
        print(flush=True)
        self._scorecard.print(do_print_score=True)

    def _report_turn_beginning(self):
        print('.', end='', flush=True)


class Player_NoRerolls_Greedy(Player):
    """Player that on each turn records the dice roll in the best scoring box, without re-rolling.
    Each final box score is compared against the outcome of an optimal player,
    according to the Yahtzee article on Wikipedia.
    """
    def _exec_policy(self):
        outcomes = { box: self._scorecard.get_box_score(box, self._roll)[0]
                              - OptimalPlay.AVG_BOX_SCORES[box.to_index()]
                     for box in self._scorecard.get_boxes_unused()
                     }
        box = max(outcomes, key=lambda b: outcomes[b])
        self._use_box(box)


class Player_NoRerolls_Random(Player):
    """Player that, on each turn, records the first dice roll in a random scoring box.
    """
    def _exec_policy(self):
        self._use_box(self._scorecard.get_random_unused_box())
