#!/usr/bin/env python

from box import Box
from player import Player


class Player_NoRerolls_Random(Player):
    """Player that, on each turn, records the first dice roll in a random scoring box.
    """
    def _exec_policy(self):
        self._use_box(self._scorecard.get_random_unused_box())
