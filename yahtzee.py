#!/usr/bin/env python

import argparse
import signal
from statistics import mean
import sys

from player_human import Player_Human
from player_bot import Player_MonteCarlo_Fast
from player_bot import Player_MonteCarlo_Slow
from player_bot import Player_NoRerolls_Greedy
from player_bot import Player_NoRerolls_Random


class GameSequence:
    def __init__(self, player):
        self.game_scores = []
        self.discarded_game_count = 0
        self.player:Player = player

    def play(self, game_count=10, min_score=0):
        """Play multiple games. If game_count == 0, then game play continues forever.
        """
        while game_count > 0 and len(self.game_scores) < game_count:
            score = self.player.play()
            if score >= min_score:
                self.game_scores.append(score)

        scores_str = '  '.join(map(str, sorted(self.game_scores)))
        print(f'Scores from {game_count} games: {scores_str}')
        if self.discarded_game_count > 0:
            discarded = self.discarded_game_count
            print(f'(Number of games discarded (score < {min_score}): {discarded:,})')
        return self.game_scores


def play_greedy(game_count=2):
    games = GameSequence(Player_NoRerolls_Greedy())
    scores = games.play(game_count)
    print(f'Mean Greedy Player score = {mean(scores)}')


def play_human(game_count=2):
    games = GameSequence(Player_Human())
    scores = games.play(game_count)
    print(f'Mean Human Player score = {mean(scores)}')


def play_monte_carlo_fast(game_count=2):
    games = GameSequence(Player_MonteCarlo_Fast())
    scores = games.play(game_count)
    print(f'Mean Monte Carlo Player (fast) score = {mean(scores)}')


def play_monte_carlo_slow(game_count=2):
    games = GameSequence(Player_MonteCarlo_Slow())
    scores = games.play(game_count)
    print(f'Mean Monte Carlo Player (slow) score = {mean(scores)}')


def play_random(game_count=2):
    games = GameSequence(Player_NoRerolls_Random())
    scores = games.play(game_count)
    print(f'Mean Random Player score = {mean(scores)}')


def main():
    parser = argparse.ArgumentParser(prog = 'Yahtzee',
                 description = 'Play the game Yahtzee',
                 add_help=False)
    parser.add_argument('-n', '--number', type=int, default=2)  # Number of games

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--fast', action='store_true')      # Monte Carlo Player (fast)
    group.add_argument('-g', '--greedy', action='store_true')    # Greedy Player
    group.add_argument('-h', '--human', action='store_true')     # Interactive mode with Human Player
    group.add_argument('-r', '--random', action='store_true')    # Random Player
    group.add_argument('-s', '--slow', action='store_true')      # Monte Carlo Player (slow)

    args = parser.parse_args()

    if args.fast:
        play_monte_carlo_fast(args.number)
    elif args.greedy:
        play_greedy(args.number)
    elif args.human:
        play_human(args.number)
    elif args.slow:
        play_monte_carlo_slow(args.number)
    elif args.random:
        play_random(args.number)
    else:
        raise RuntimeError(f'Program failed to catch missing mandatory flag '
                            'specifying which Player type to use.')


if __name__ == '__main__':
    def sigint_handler(sig, frame):
        print(f'\nThanks for playing. Exiting via SIGINT. Bye!')
        sys.exit(0)

    signal.signal(signal.SIGINT, sigint_handler)
    main()
