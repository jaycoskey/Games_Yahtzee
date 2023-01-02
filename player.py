#!/usr/bin/env python

from abc import ABC
from collections import defaultdict
from copy import deepcopy

from box import Box
from dice import Dice
from scorecard import Scorecard
# from strategy import Strategy


class Player(ABC):
    def __init__(self):
        self._scorecard = None
        self._roll = None
        self._roll_num = None
        self._turn_num = 1

    def _exec_policy(self):
        """Carries out moves, whether computed or from a human player.
        Calls self._reroll(dice_indices) and self._use_box(box).
        """
        raise NotImplementedError('Player._exec_policy()')

    def _init_roll(self):
        """Carries out first dice roll for each turn.
        Subsequent dice rolls within each turn result from calls to self._reroll().
        """
        self._roll = Dice.roll()
        self._roll_num = 1

    def _print_new_game(self):
        pass

    def _print_reroll(self, old_roll, reroll, new_roll):
        context_str = f'Turn #{self._turn_num}, roll #{self._roll_num}'
        to_die_num = lambda x: x+1
        reroll_str = ' '.join(map(str, list(map(to_die_num, reroll))))
        action_str = f'rerolling {reroll_str}'
        print(f'{context_str}: {action_str}: {old_roll} ==> {new_roll}')

    def _print_roll(self):
        roll_str = '  '.join(map(str, self._roll))
        print(f'Dice ID:  1  2  3  4  5')
        print(f'Roll #{self._roll_num}:  {roll_str}')

    def _print_scorecard(self):
        self._scorecard.print()

    def _print_summary(self):
        print(flush=True)
        self._scorecard.print(do_print_score=True)

    def _print_turn_beginning(self):
        print('.', end='', flush=True)

    def _print_turn_num(self):
        print(f'Turn #{self._turn_num}')

    def _report_new_game(self):
        pass

    def _report_reroll(self, old_roll, reroll, new_roll):
        pass

    def _report_roll(self):
        pass

    def _report_scorecard(self):
        pass

    def _report_summary(self):
        pass

    def _report_turn_beginning(self):
        pass

    def _reroll(self, reroll):
        assert(self._roll_num <= 2)
        old_roll = self._roll
        new_roll = Dice.reroll(self._roll, reroll)
        self._report_reroll(old_roll, reroll, new_roll)
        self._roll = new_roll
        self._roll_num += 1

    def _use_box(self, box):
        self._scorecard.use_box(self._roll, box)
        self._init_roll()
        self._turn_num += 1

    def play(self):
        self._report_new_game()
        self._scorecard = Scorecard()
        self._turn_num = 1
        self._init_roll()
        while self._turn_num <= Box.nonnone_count():
            if self._roll_num == 1:
                self._report_turn_beginning()
            self._exec_policy()
        self._report_summary()
        return self._scorecard.get_score()
