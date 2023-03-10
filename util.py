#!/usr/bin/env python

from dataclasses import dataclass


@dataclass
class LongestConsecutiveSequence:
    min: int
    length: int

    def contains(self, x):
        return self.min <= x <= self.max

    def distance(self, x):
        if self.min <= x <= self.max:
            return 0
        elif x < self.min:
            return self.min - x
        else:  # self.max < x
            return x - self.max

    @property
    def max(self):
        return self.min + self.length - 1

    def tup(self):
        return (self.min, self.length)


class Util:
    @staticmethod
    def reverse(xs):
        return xs[::-1]

    @staticmethod
    def init_static(cls):
        assert(getattr(cls, '_init_static'))
        cls._init_static()
        return cls

    @staticmethod
    def longest_consecutive_sequence(items)->LongestConsecutiveSequence:
        """Returns an instance of LongestConsecutiveSequence.
        In the event of multiple sequences of the same length, it returns the first one.
        """
        xs = sorted(list(set(items)))
        if len(xs) == 0:
            return LongestConsecutiveSequence(0, 0)
        elif len(xs) == 1:
            return LongestConsecutiveSequence(xs[0], 1)

        seq_min = xs[0]
        seq_length = 1
        seq_prev = xs[0]

        result_min = 1
        result_length = 1
        for val in xs[1:]:
            if val == seq_prev + 1:  # Continuing current consecutive seq
                seq_length += 1
                seq_prev = val
            else:  # Moving to next consecutive seq
                if seq_length > result_length:
                    result_min = seq_min
                    result_length = seq_length
                seq_min = val
                seq_length = 1
                seq_prev = val
        if seq_length > result_length:
            return LongestConsecutiveSequence(seq_min, seq_length)
        else:
            return LongestConsecutiveSequence(result_min, result_length)
