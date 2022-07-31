from decimal import Decimal
from typing import List

from degen.odds_models import Odds


class Bet(object):
    """Class representing a generic Bet"""

    def __init__(self, wager_amt: Decimal, odds: Odds):
        self.wager_amt = wager_amt
        self._odds = odds

    @property
    def american_odds(self):
        return self._odds.to_american_odds()

    @property
    def implied_probability(self):
        return self._odds.to_implied_probability()

    @property
    def decimal_odds(self):
        return self._odds.to_decimal_odds()

    @property
    def payoff(self):
        dec_odds = self.decimal_odds.value
        return self.wager_amt * dec_odds


class Parlay(Bet):
    def __init__(self, wager_amt: Decimal, legs: List[Odds]):
        self.legs = legs
        self.odds: Odds = legs[0]

        for odds in legs[1:]:
            self.odds &= odds

        super().__init__(wager_amt, self.odds)
