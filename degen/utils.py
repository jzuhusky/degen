from decimal import Decimal


def check_implied_probability(implied_probability: Decimal):
    if implied_probability > 1.0 or implied_probability < 0:
        raise ValueError("Implied probability must be between 0.0 and 1.0")
