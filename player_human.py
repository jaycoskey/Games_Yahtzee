#!/usr/bin/env python

import re

from box import Box
from dice import Dice
from player import Player
from scorecard import Scorecard
from text import HelpText, HelpTopic


class Player_Human(Player):
    def _exec_policy(self):
        self._report_roll()
        while True:
            prompt = 'Scoring box: ' if self._roll_num == 3 else 'Command (? for help): '
            user_input = input(prompt).strip().upper()
            if not user_input or user_input.startswith('?') or user_input.startswith('HELP'):
                topics = user_input.split()[1:]
                if len(topics) > 1:
                    print('Please choose a single help topic')
                    continue
                if len(topics) == 0:
                    self.print_help_topic(HelpTopic.OVERVIEW)
                    continue

                if topics[0].startswith('R'):    # HELP ROLL
                    self.print_help_topic(HelpTopic.CHOICE_ROLL_SYNTAX)
                    continue
                elif topics[0].startswith('B'):  # HELP BOX
                    self.print_help_topic(HelpTopic.CHOICE_BOX_SYNTAX)
                    continue
                elif topics[0].startswith('M'):  # HELP MOVES
                    boxes_strs = self.scorecard.get_scoring_boxes_strs(self.current_roll)
                    print(f'Scoring boxes: {"  ".join(boxes_strs)}')
                    continue
                elif topics[0].startswith('S'):  # HELP STATUS
                    self._report_turn_scorecard_roll()
                    continue
                else:
                    print(f'Unrecognized help topic {topics[0]}')
                    continue

            if re.search(r'^[1-5\s]+$', user_input):  # RE-ROLL
                if self._roll_num == 3:
                    print('On the third roll, re-rolling is not available')
                    continue
                reroll = list(map(lambda s: int(s), [c for c in user_input if c != ' ']))
                if len(set(reroll)) < len(reroll):
                    print('Please enter dictinct dice IDs')
                    continue
                print(f'Re-rolling: {", ".join(map(str, reroll))}')
                reroll_inds = map(lambda x: x - 1, reroll)
                self._reroll(reroll_inds)
                break  # ========== RE-ROLLED ==========
            else:  # BOX
                words = user_input.split()
                if len(words) > 1:
                    print('If a box is selected for scoring, a single box must be selected.')
                    continue
                if words[0] == 'R':
                    self._use_box(self._scorecard.get_random_unused_box())
                    break  # ========== USED RANDOM BOX ==========
                box = Box.from_code(words[0])
                if box == Box.NONE:
                    print('Unrecognized Box code. Enter "help box" for a list.')
                    continue
                if self._scorecard.is_box_used[box.to_index()]:
                    print('That box is not available. Try again.')
                    continue
                self._use_box(box)
                break  # ========== USED CHOSEN BOX ==========

    def _print_help_topic(self, topic:HelpTopic):
        if topic == HelpTopic.OVERVIEW:
            print(HelpText.OVERVIEW)
        elif topic == HelpTopic.CHOICE_BOX_SYNTAX:
            print(HelpText.CHOICE_BOX_SYNTAX)
        elif topic == HelpTopic.CHOICE_ROLL_SYNTAX:
            print(HelpText.CHOICE_ROLL_SYNTAX)
        else:
            raise ValueError('Player_Human.print_help_topic: Unrecognized topic: {topic}')

    def _report_new_game(self):
        print(f'**************************')
        print(f'******** New Game ********')
        print(f'**************************')

    def _report_roll(self):
        self._print_roll()

    def _report_scorecard(self):
        self._print_scorecard()

    def _report_summary(self):
        print(f'===== Final scorecard =====')
        self._scorecard.print()
        final_score = self._scorecard.get_score()
        print(f'==== Final score: {final_score} ====')
        print()

    def _report_turn_beginning(self):
        self._report_turn_num()
        self._report_scorecard()

    def _report_turn_num(self):
        self._print_turn_num()
