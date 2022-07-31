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

    def test_ip_to_ameican_fail(self):

        juiced_odds = ImpliedProbability(1.1)

        with pytest.raises(ValueError):
            _ = juiced_odds.to_american_odds()
