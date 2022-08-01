from decimal import Decimal
import unittest

from degen import AmericanOdds, Bet, DecimalOdds, ImpliedProbability, Parlay


class TestBetModels(unittest.TestCase):
    def test_bet_simple(self):
        bet = Bet(wager_amt=Decimal(100), odds=AmericanOdds(100))
        self.assertEqual(bet.american_odds, AmericanOdds(100))
        self.assertEqual(bet.decimal_odds, DecimalOdds(2.0))
        self.assertEqual(bet.implied_probability, ImpliedProbability(0.5))
        self.assertEqual(bet.payoff, Decimal(200))

    def test_parlay(self):

        leg1 = AmericanOdds(100)
        leg2 = AmericanOdds(100)

        parlay = Parlay(wager_amt=Decimal(100), legs=[leg1, leg2])

        self.assertEqual(parlay.american_odds, AmericanOdds(300))
        self.assertEqual(parlay.decimal_odds, DecimalOdds(4.0))
        self.assertEqual(parlay.implied_probability, ImpliedProbability(0.25))
        self.assertEqual(parlay.payoff, Decimal(400))

    def test_parlay_2(self):
        p = Parlay(
            wager_amt=Decimal(100), legs=[AmericanOdds(100), AmericanOdds(200), AmericanOdds(100)]
        )
        self.assertEqual(p.odds.value, Decimal(1100))
        self.assertEqual(p.payoff, Decimal(1200))
