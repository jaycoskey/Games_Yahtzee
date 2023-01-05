#!/usr/bin/env python

import numpy as np
import random as r

from box import Box
from collections import Counter
from config import Config
from util import Util


class Scorecard:
    UPPER_BONUS = 35
    UPPER_THRESHOLD = 63
    YAHTZEE_BONUS = 100

    boxes_section_upper = [ Box.ACES, Box.TWOS, Box.THREES,
                            Box.FOURS, Box.FIVES, Box.SIXES ]
    boxes_score_sum = [Box.KIND3, Box.KIND4, Box.CHANCE]
    boxes_other_scores = {Box.FULL_HOUSE: 25,
                          Box.STRAIGHT_SMALL: 30,
                          Box.STRAIGHT_LARGE: 40,
                          Box.YAHTZEE: 50}

    def __init__(self):
        self.box_score = np.zeros(Box.nonnone_count(), dtype=int)
        self.is_box_used = np.empty(Box.nonnone_count(), dtype=bool)
        self.is_box_used.fill(False)
        self.yahtzee_bonus_count = 0

    def get_array_scoring(self, vals):
        counter = Counter(vals)
        pips = counter.keys()
        counts = counter.values()
        lcs = Util.longest_consecutive_sequence(vals)

        boxes = np.zeros(Box.nonnone_count(), dtype=int)
        if 1 in pips:
            boxes[Box.ACES.to_index()]   = 1
        if 2 in pips:
            boxes[Box.TWOS.to_index()]   = 1
        if 3 in pips:
            boxes[Box.THREES.to_index()] = 1
        if 4 in pips:
            boxes[Box.FOURS.to_index()]  = 1
        if 5 in pips:
            boxes[Box.FIVES.to_index()]  = 1
        if 6 in pips:
            boxes[Box.SIXES.to_index()]  = 1
        if 3 in counts:
            boxes[Box.KIND3.to_index()]  = 1
        if 4 in counts:
            boxes[Box.KIND4.to_index()]  = 1
            boxes[Box.KIND3.to_index()]  = 1
        if sorted(counts) == [2, 3]:
            boxes[Box.FULL_HOUSE.to_index()] = 1
        if lcs.length >= 4:
            boxes[Box.STRAIGHT_SMALL.to_index()] = 1
        if lcs.length >= 5:
            boxes[Box.STRAIGHT_LARGE.to_index()] = 1
        if 5 in counts:
            boxes[Box.YAHTZEE.to_index()] = 1
            boxes[Box.KIND4.to_index()] = 1
            boxes[Box.KIND3.to_index()] = 1

        # JOKER RULE
        is_yahtzee = boxes[Box.YAHTZEE.to_index()] == 1
        if is_yahtzee and Config.DO_USE_JOKER_RULE:
            is_yahtzee_already_used = self.box_score[Box.YAHTZEE.to_index()] > 0
            if is_yahtzee_already_used:
                is_upper_box_already_used = self.is_box_used[vals[0]]
                if is_upper_box_already_used or (not Config.DO_USE_JOKER_RULE_UPPER_SECTION):
                    boxes[Box.KIND3.to_index()]  = 1
                    boxes[Box.KIND4.to_index()]  = 1
                    boxes[Box.FULL_HOUSE.to_index()] = 1
                    boxes[Box.STRAIGHT_SMALL.to_index()] = 1
                    boxes[Box.STRAIGHT_LARGE.to_index()] = 1

        boxes[Box.CHANCE.to_index()] = 1
        return boxes

    def get_box_score(self, box, roll):
        assert(not self.is_box_used[box.to_index()])
        scoring_boxes = self.get_array_scoring(roll)
        is_yahtzee = scoring_boxes[Box.YAHTZEE.to_index()]

        if not scoring_boxes[box.to_index()]:
            score = 0
        elif box in Scorecard.boxes_section_upper:
            target = int(box)
            score = sum([val for val in roll if val == target])
        elif box in Scorecard.boxes_score_sum:
            score = sum(roll)
        else:
            score = self.boxes_other_scores[box]
        return (score, is_yahtzee)

    def get_boxes_unused(self):
        return [b for b in Box
                if b != Box.NONE and not self.is_box_used[b.to_index()]]

    def get_random_unused_box(self):
        return r.choice(self.get_boxes_unused())

    def get_score(self):
        score_upper_raw = self.get_score_upper_raw()
        score_upper_bonus = (Scorecard.UPPER_BONUS
                             if score_upper_raw >= Scorecard.UPPER_THRESHOLD
                             else 0)
        score_lower_raw = self.box_score[6:14].sum()
        yahtzee_bonus = Scorecard.YAHTZEE_BONUS * self.yahtzee_bonus_count
        score = (score_upper_raw + score_upper_bonus
                    + score_lower_raw + yahtzee_bonus)
        return score

    def get_score_upper_raw(self):
        return self.box_score[0:6].sum()

    def print(self, do_print_score=False):
        self.print_full(do_print_score)

    def print_brief(self):
        print(f'====================')
        for scorecard_field in box:
            print(f'\t{box(r).name}\t{self.box_score[scorecard_field]}')
        print(f'Total score: {self.get_score()}')
        print(f'====================')

    def print_full(self, do_print_score=False):
        def get_score_str(n):
            return self.box_score[n] if self.is_box_used[n] else ''

        score_upper_raw = self.get_score_upper_raw()
        score_upper_bonus = Scorecard.UPPER_BONUS if score_upper_raw >= Scorecard.UPPER_THRESHOLD else 0

        text = (f'==========================\n'
                f'  Upper Section   | Score\n'
                f'==================+=======\n'
                f'  Aces (Ones)     | {get_score_str(0):>4}\n'
                f'------------------+-------\n'
                f'  Twos            | {get_score_str(1):>4}\n'
                f'------------------+-------\n'
                f'  Threes          | {get_score_str(2):>4}\n'
                f'------------------+-------\n'
                f'  Fours           | {get_score_str(3):>4}\n'
                f'------------------+-------\n'
                f'  Fives           | {get_score_str(4):>4}\n'
                f'------------------+-------\n'
                f'  Sixes           | {get_score_str(5):>4}\n'
                f'==================+=======\n'
                f'  Upper Bonus     | {score_upper_bonus:>4}\n'
                f'==================+=======\n'
                f'  3 of a Kind     | {get_score_str(6):>4}\n'
                f'------------------+-------\n'
                f'  4 of a Kind     | {get_score_str(7):>4}\n'
                f'------------------+-------\n'
                f'  Full House      | {get_score_str(8):>4}\n'
                f'------------------+-------\n'
                f'  Small Straight  | {get_score_str(9):>4}\n'
                f'------------------+-------\n'
                f'  Large Straight  | {get_score_str(10):>4}\n'
                f'------------------+-------\n'
                f'  YAHTZEE         | {get_score_str(11):>4}\n'
                f'------------------+-------\n'
                f'  Chance          | {get_score_str(12):>4}\n'
                f'==================+=======\n'
                f'  Yahtzee Bonus   | {Scorecard.YAHTZEE_BONUS * self.yahtzee_bonus_count:>4}\n'
                f'==================+=======')
        if do_print_score:
                text += '\n' + f'  Total           | {self.get_score():>4}\n'
                text +=        f'==================+======='
        print(text)

    def use_box(self, roll, box):
        assert(not self.is_box_used[box.to_index()])
        (score, is_yahtzee) = self.get_box_score(box, roll)
        self.box_score[box.to_index()] = score
        self.is_box_used[box.to_index()] = True
        if (Config.DO_USE_YAHTZEE_BONUS
                and self.box_score[Box.YAHTZEE.to_index()] > 0
                and is_yahtzee):
            self.yahtzee_bonus_count += 1
