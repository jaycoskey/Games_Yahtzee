#!/usr/bin/env python

import unittest

from box import Box
from player_bot import Player_MonteCarlo_Fast
from scorecard import Scorecard


class Player_MonteCarlo_Fast_Test(unittest.TestCase):
    def test_monte_carlo_fast(self):
        player = Player_MonteCarlo_Fast()

        # Custom initialization
        player._scorecard = Scorecard()
        player._turn_num = 1
        player._roll_num = 1
        player._roll = [6, 6, 6, 6, 6]  # YAHTZEE

        player._exec_policy()
        assert(player._roll_num == 2)
        assert(player._roll == [6, 6, 6, 6, 6])

        player._exec_policy()
        assert(player._roll_num == 3)
        assert(player._roll == [6, 6, 6, 6, 6])

        player._exec_policy()
        assert(player._turn_num == 2)
        assert(player._roll_num == 1)
        assert(player._scorecard.is_box_used[Box.YAHTZEE.to_index()] == 1)


if __name__ == '__main__':
    unittest.main()
