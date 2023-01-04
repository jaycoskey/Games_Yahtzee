#!/usr/bin/env python

import numpy as np
import numpy.typing as npt


class OptimalPlay:
    # The following data is from Wikipedia's page on Yahtzee.
    AVG_BOX_SCORES:npt.NDArray = np.array(
        [1.88, 5.28, 8.57, 12.16, 15.69, 19.19,
        21.66, 13.10, 22.59, 29.46, 32.71, 16.87, 22.01])
    ZERO_BOX_SCORE_PROB:npt.NDArray = np.array([
        0.1084, 0.0180, 0.0095, 0.0060, 0.0050, 0.0053,
        0.0326, 0.3634, 0.0963, 0.0180, 0.1822, 0.6626, 0.0])

    UPPER_BONUS:float   = 23.84
    YAHTZEE_BONUS:float = 9.58

    ZERO_UPPER_BONUS_PROB:float   = 0.3188
    ZERO_YAHTZEE_BONUS_PROB:float = 0.9176
