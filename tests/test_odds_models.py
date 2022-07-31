from decimal import Decimal
import unittest

import pytest

from degen import (
    AmericanOdds,
    DecimalOdds,
    ImpliedProbability,
)
from degen.odds_models import Odds


class TestMathTools(unittest.TestCase):
    def test_american_odds_exception(self):
        """Test invalid american odds"""
        with pytest.raises(ValueError):
            _ = AmericanOdds(50)

        with pytest.raises(ValueError):
            _ = AmericanOdds(-42)

    def test_decimal_exception(self):
        """Test invalid decimal odds"""

        with pytest.raises(ValueError):
            _ = DecimalOdds(-0.9)

    def test_implied_prob_exception(self):
        """Test invalid implied probability"""

        with pytest.raises(ValueError):
            _ = ImpliedProbability(-0.1)

    def test_juice(self):
        """Test juice can exist - but can't convert"""

        not_juiced = AmericanOdds(-110)
        self.assertFalse(not_juiced.is_juiced)

        # implied prob > 1
        juiced_ip = ImpliedProbability(1.05)
        self.assertTrue(juiced_ip.is_juiced)
        with pytest.raises(ValueError):
            _ = juiced_ip.to_american_odds()

        juiced_decimal_odds = juiced_ip.to_decimal_odds()
        self.assertTrue(juiced_decimal_odds.is_juiced)
        with pytest.raises(ValueError):
            _ = juiced_decimal_odds.to_american_odds()

    def test_compute_juice(self):

        odds1 = AmericanOdds(-110)
        odds2 = AmericanOdds(-110)

        juiced_odds: Odds = odds1 | odds2

        self.assertTrue(juiced_odds.is_juiced)
        self.assertEqual(type(juiced_odds), ImpliedProbability)

        decimal_juiced_odds = juiced_odds.to_decimal_odds()
        self.assertLess(decimal_juiced_odds.value, Decimal(1.0))
        self.assertTrue(decimal_juiced_odds.is_juiced)

        odds1 = AmericanOdds(110)
        odds2 = AmericanOdds(110)

        self.assertFalse((odds1 & odds2).is_juiced)

    def test_ip_to_american_fail(self):

        juiced_odds = ImpliedProbability(1.1)

        with pytest.raises(ValueError):
            _ = juiced_odds.to_american_odds()

    def test_implied_prob_model(self):

        ip = ImpliedProbability(0.25)
        american = ip.to_american_odds()
        self.assertEqual(american.value, 300)

        ip = ImpliedProbability(0.75)
        american = ip.to_american_odds()
        self.assertEqual(american.value, -300)

    def test_decimal_model(self):
        odds = DecimalOdds(Decimal(3.0))
        american = odds.to_american_odds()
        self.assertEqual(american.value, Decimal(200))

        american = AmericanOdds(Decimal(-200))
        dec = american.to_decimal_odds()
        self.assertEqual(dec.value, Decimal(1.5))

        dec = DecimalOdds(Decimal(2.0))
        ip = dec.to_implied_probability()
        self.assertEqual(ip.value, Decimal(0.5))

    def test_bitwise_ops(self):
        odds = AmericanOdds(100) & DecimalOdds(2.0)
        self.assertEqual(type(odds), AmericanOdds)
        self.assertEqual(odds.value, Decimal(300))

        odds = DecimalOdds(2.0) & AmericanOdds(100)
        self.assertEqual(type(odds), DecimalOdds)
        self.assertEqual(odds.value, Decimal(4.0))

        odds = ImpliedProbability(0.25) | AmericanOdds(300)
        self.assertEqual(type(odds), ImpliedProbability)
        self.assertEqual(odds.value, Decimal(0.5))

        odds = AmericanOdds(300) | ImpliedProbability(0.25)
        self.assertEqual(type(odds), AmericanOdds)
        self.assertEqual(odds.value, Decimal(100))

        odds = DecimalOdds(2.0) & ImpliedProbability(0.5)
        self.assertEqual(type(odds), DecimalOdds)
        self.assertEqual(odds.value, Decimal(4.0))

        odds = DecimalOdds(2.5) | AmericanOdds(150)
        self.assertEqual(type(odds), DecimalOdds)
        self.assertEqual(odds.value, Decimal(1.25))

        odds = ImpliedProbability(0.5) & ImpliedProbability(0.5)
        self.assertEqual(type(odds), ImpliedProbability)
        self.assertEqual(odds.value, Decimal(0.25))
