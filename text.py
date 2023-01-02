#!/usr/bin/env python

from enum import auto, Enum


class HelpTopic(Enum):
    OVERVIEW = auto()
    CHOICE_BOX_SYNTAX = auto()
    CHOICE_ROLL_SYNTAX = auto()


class HelpText:
    OVERVIEW = r"""This game assumes that the user is familiar with the rules of Yahtzee.
        This game follows those rules, including the Yahtzee Bonus Rule, and
        the Joker Rule. The user has 13 rounds to fill in a scorecard,
        collecting points along the way.

        Options:
            help      This message. A question mark can be used instead of "help".
            ? roll    Show how to enter which dice to re-roll.
            ? box     Show how to enter which box to fill in.
            ? moves   Show which (positive) scoring moves are available.
            ? status  Show the scorecard and the curent dice roll.

        <Dice IDs to be re-rolled>  Specify which dice to re-roll, after roll #1 or #2.
        <Scorecard box to use>      Specify which box to use, after any roll.

    """

    CHOICE_BOX_SYNTAX = r"""Each turn involves recording a score in a scorecard box.
        After your third roll, you must choose to do so, because there are no rolls left.
        To choose a box from the upper portion of the scorecard (Ones, Twos, Threes, etc),
        use one of the following codes: B1, B2, B3, B4, B5, or B6.

        To pick a boxes from the lower section of the scorecard, choose one of these:
            Three of a Kind: K3
            Four of a Kind:  K4
            Full House:      FH
            Small Straight:  SS
            Large Straight:  LS
            Yahtzee:         Y
            Chance:          C

        Note: All the entries are case-insensitive. So if you have the roll:
              ID:          1   2   3   4   5
              Roll value:  3   6   4   5   2
            You could then enter the box ID "LS", for "long straight".
            Your more>   ls
    """

    CHOICE_ROLL_SYNTAX = r"""
        On the first or second roll, you can choose which dice to re-roll.
        To do this, list at the prompt the IDs of those dice to be re-rolled.
        For example, if the first roll is
            ID:          1   2   3   4   5
            Roll value:  4   6   4   5   1
        To specify that you want to re-roll die #5, you would enter
            Your more>   1  5
        """
