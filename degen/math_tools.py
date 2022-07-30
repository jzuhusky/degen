from decimal import Decimal

from degen.utils import check_implied_probability


def implied_prob_to_odds_pos(implied_prob: Decimal) -> Decimal:
    """Compute Positive American Odds given an implied prob"""
    check_implied_probability(implied_prob)
    return (Decimal(100.0) / implied_prob) - Decimal(100.0)


def implied_prob_to_odds_neg(implied_prob: Decimal) -> Decimal:
    """Compute Negative American Odds given an implied prob"""
    check_implied_probability(implied_prob)
    return (Decimal(100.0) * implied_prob) / (implied_prob - Decimal(1.0))


def american_odds_to_implied_prob(american_odds: Decimal) -> Decimal:
    """American odds to implied probability"""

    if american_odds == Decimal("-100"):
        american_odds = Decimal("100")

    if american_odds >= Decimal(100.0):
        return Decimal(100.0) / (american_odds + Decimal(100.0))
    else:
        return abs(american_odds) / (abs(american_odds) + Decimal(100.0))


def american_odds_to_decimal_odds(american_odds: Decimal) -> Decimal:
    """American odds to decimal odds"""
    if american_odds >= Decimal(100.0):
        return Decimal(1.0) + (american_odds / Decimal(100.0))
    else:
        return Decimal(1.0) - (Decimal(100.0) / american_odds)


def decimal_odds_to_american_odds(decimal_odds: Decimal) -> Decimal:
    """Decimal odds to american odds"""
    if decimal_odds >= Decimal(2.0):
        return (decimal_odds - Decimal(1.0)) * Decimal(100.0)
    else:
        return Decimal(-100.0) / (decimal_odds - Decimal(1.0))


def decimal_odds_to_implied_prob(decimal_odds: Decimal) -> Decimal:
    """Decimal odds to implied probability"""
    return Decimal(1.0) / decimal_odds


def implied_prob_to_decimal_odds(implied_prob: Decimal) -> Decimal:
    """Implied Probability to decimal odds"""
    return Decimal(1.0) / implied_prob
