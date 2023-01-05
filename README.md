<div align="center">
<h1>Yahtzee</h1>
</div>

A repo for exploring player implementations related to the game of Yahtzee.
Specifically: random, human, Monte Carlo, and (deep) reinforcement learning
players.

## How to run:
  * To play ten interactive games:
```
    % ./yahtzee.py --human -n 10
```
  * To have the Random Player play 100 games:
```
    % ./yahtzee.py --random -n 100
```

## TODO-Players:
  * Add early scoring (before 3rd roll) capabilities to Monte Carlo players.
  * Improve scores of the "fast" Monte Carlo Player. Is about 180. Should be > 200.
  * Implement one or more players using Reinforcement Learning.
  * [Low pri] Support interactive play without a pre-set number of games.
  * [Low pri] Return Move data from \_exec\_policy, for more detailed testing.
  * [Low pri] Implement multi-player play. For example, a bot aware of the scores
    of other players could choose a different risk/reward balance in the hopes
    of winning a game it had been losing.

## TODO-LongestConsecutiveSubsequence:
  * [Low pri] Either return all longest consecutive subsequences,
    or reverse the traversal order so that, in the case of ties,
    the sequence with the larger values is chosen.

## TODO-GUI:
  * [Low pri] Implement GUI.
