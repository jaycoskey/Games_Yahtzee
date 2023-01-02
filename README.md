<div align="center">
<h1>Yahtzee</h1>
</div>

A repo for exploring player implementations related to the game of Yahtzee.
Specifically: random, human, Monte Carlo, and (deep) reinforcement learning
players.

## How to run:
  * To have the Random Player play 100 games: 
```
    % ./yahtzee.py --random -n 100
```

## TODO-Players:
  * Implement human player.
  * Implement greedy player, without re-rolls.
  * Implement heuristics to implement fairly high-scoring, efficient player.
  * Implement one or more Monte Carlo players.
    * At least one "slow" MC Player that simulates all dice rolls.
    * At least one "fast" MC Player that uses cached statistical data.
  * Implement one or more reinforcement learning players, with training.
  * Implement multi-player play. For example, a bot aware of the scores
    of other players could choose a different risk/reward balance in the hopes
    of winning a game it had been losing.

## TODO-LongestConsecutiveSubsequence:
  * Either return all longest consecutive subsequences, or reverse the traversal order
    so that, in the case of ties, the sequence with the larger values is chosen.

## TODO-GUI:
  * Possibly implement GUI.
