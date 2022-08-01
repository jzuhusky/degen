import abc
from decimal import Decimal

from pydantic import BaseModel, validator

from degen.math_tools import (
    american_odds_to_implied_prob as aotip,
    american_odds_to_decimal_odds as aotdo,
    implied_prob_to_odds_neg as ipton,
    implied_prob_to_odds_pos as iptop,
    implied_prob_to_decimal_odds as iptdo,
    decimal_odds_to_american_odds as dotao,
    decimal_odds_to_implied_prob as dotip,
)


class Odds(BaseModel, abc.ABC):

    value: Decimal

    @abc.abstractmethod
    def to_american_odds(self):
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def to_implied_probability(self):
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def to_decimal_odds(self):
        raise NotImplementedError  # pragma: no cover

    @property
    def is_juiced(self):
        return False

    def __eq__(self, other):
        return self.value == other.value

    def __or__(self, other):
        """Compute sum of implied odds and return new odds"""
        implied_odds_value = self.to_implied_probability().value
        other_implied_odds_value = other.to_implied_probability().value
        new_odds = ImpliedProbability(implied_odds_value + other_implied_odds_value)

        if new_odds.value >= Decimal(1.0):
            # only return implied prob - as these are juiced odds
            return new_odds

        if isinstance(self, AmericanOdds):
            return new_odds.to_american_odds()
        elif isinstance(self, DecimalOdds):
            return new_odds.to_decimal_odds()
        elif isinstance(self, ImpliedProbability):
            return new_odds
        raise TypeError()

    def __and__(self, other):
        """Compute product of implied odds and return new odds"""
        implied_odds_value = self.to_implied_probability().value
        other_implied_odds_value = other.to_implied_probability().value
        new_odds = ImpliedProbability(implied_odds_value * other_implied_odds_value)
        if isinstance(self, AmericanOdds):
            return new_odds.to_american_odds()
        elif isinstance(self, DecimalOdds):
            return new_odds.to_decimal_odds()
        elif isinstance(self, ImpliedProbability):
            return new_odds
        raise TypeError()


class AmericanOdds(Odds):

    # American odds are generally represented by integers >= 100 (+100)
    # or <= -100. But there is no reason why they *must* be integers, for this
    # reason, we allow them to be Decimals.
    # value: Decimal

    def __init__(self, value, **kwargs):
        super().__init__(value=value, **kwargs)

    @validator("value")
    def valid_american_odds(cls, v):
        if -100 < v < 100:
            raise ValueError("Invalid american odds. Odds must be >= +100 or <= -100")
        return v

    def to_american_odds(self):
        return self

    def to_decimal_odds(self):
        return DecimalOdds(value=aotdo(self.value))

    def to_implied_probability(self):
        return ImpliedProbability(value=aotip(self.value))


class DecimalOdds(Odds):
    def __init__(self, value, **kwargs):
        super().__init__(value=value, **kwargs)

    @validator("value")
    def valid_decimal_odds(cls, v):
        if v <= Decimal(0.0):
            raise ValueError("Decimal odds must be greater than 0.0")
        return v

    def to_american_odds(self):
        if self.is_juiced:
            raise ValueError("Cannot convert to juiced odds to american odds")
        return AmericanOdds(value=dotao(self.value))

    def to_decimal_odds(self):
        return self

    def to_implied_probability(self):
        return ImpliedProbability(value=dotip(self.value))

    @property
    def is_juiced(self):
        return self.value < Decimal(1.0)


class ImpliedProbability(Odds):
    def __init__(self, value, **kwargs):
        super().__init__(value=value, **kwargs)

    @validator("value")
    def valid_implied_odds(cls, v):
        if v < Decimal(0.0):
            # for betting purposes, it's sometimes useful to see implied
            # odds greater than 1.0. This is the "juice".
            raise ValueError("Implied odds must be greater than 0.0")
        return v

    def to_american_odds(self):
        if self.is_juiced:
            raise ValueError("Cannot convert to juiced odds to american odds")
        if self.value > Decimal(0.5):
            return AmericanOdds(value=ipton(self.value))
        return AmericanOdds(value=iptop(self.value))

    def to_decimal_odds(self):
        return DecimalOdds(value=iptdo(self.value))

    def to_implied_probability(self):
        return self

    @property
    def is_juiced(self):
        return self.value > Decimal(1.0)
