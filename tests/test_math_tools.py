from decimal import Decimal
import unittest

import pytest

from degen.math_tools import (
    implied_prob_to_odds_pos,
    implied_prob_to_odds_neg,
    implied_prob_to_decimal_odds,
    american_odds_to_implied_prob,
    american_odds_to_decimal_odds,
    decimal_odds_to_implied_prob,
    decimal_odds_to_american_odds,
)


class TestMathTools(unittest.TestCase):
    def test_implied_odds_american_odds_pos(self):
        cases = [
            (Decimal("0.5"), Decimal("100")),
            (Decimal("0.25"), Decimal("300")),
            (Decimal("0.20"), Decimal("400")),
        ]

        for implied_prob, american_odds in cases:
            american_odds_computed = implied_prob_to_odds_pos(implied_prob)
            self.assertEqual(american_odds_computed, american_odds)

            implied_prob_computed = american_odds_to_implied_prob(american_odds)
            self.assertEqual(implied_prob_computed, implied_prob)

        with pytest.raises(ValueError):
            _ = implied_prob_to_odds_pos(Decimal(1.1))

        with pytest.raises(ValueError):
            _ = implied_prob_to_odds_neg(Decimal(-0.1))

    def test_implied_odds_american_odds_neg(self):

        # (implied prob, american odds)
        cases = [
            (Decimal("0.5"), Decimal("-100")),
            (Decimal("0.75"), Decimal("-300")),
            (Decimal("0.80"), Decimal("-400")),
        ]

        for implied_prob, american_odds in cases:
            american_odds_computed = implied_prob_to_odds_neg(implied_prob)
            self.assertEqual(american_odds_computed, american_odds)

            implied_prob_computed = american_odds_to_implied_prob(american_odds)
            self.assertEqual(implied_prob_computed, implied_prob)

    def test_implied_prob_decimal(self):

        cases = [
            (Decimal("0.5"), Decimal("2.0")),
            (Decimal("0.625"), Decimal("1.6")),
        ]

        for implied_prob, decimal_odds in cases:
            decimal_odds_computed = implied_prob_to_decimal_odds(implied_prob)
            self.assertEqual(decimal_odds_computed, decimal_odds)

            # and vice versa
            implied_prob_computed = decimal_odds_to_implied_prob(decimal_odds)
            self.assertEqual(implied_prob_computed, implied_prob)

    def test_american_odds_decimal(self):
        cases = [
            (Decimal("2.0"), Decimal("100")),
            (Decimal("3.0"), Decimal("200")),
            (Decimal("1.5"), Decimal("-200")),
            (Decimal("3.5"), Decimal("250")),
        ]

        for decimal_odds, american_odds in cases:
            decimal_odds_computed = american_odds_to_decimal_odds(american_odds)
            self.assertEqual(decimal_odds_computed, decimal_odds)

            american_odds_computed = decimal_odds_to_american_odds(decimal_odds)
            self.assertEqual(american_odds_computed, american_odds)
