# Degen 

*pronounced "dee-gen"* as in [Degenerate Gambler](https://www.urbandictionary.com/define.php?term=Degenerate%20Gambler)

![alt text](https://github.com/jzuhusky/degen/blob/master/coverage.svg?raw=true)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### Installation

```bash
pip install degen
```

## Programming with betting odds, made simple

Easy to initialize `Odds` objects.
```python
from degen import AmericanOdds

odds = AmericanOdds(-110)
print(odds.value)
# >>> -110
```

Easily convert to and from each type of odds. `AmericanOdds` `DecimalOdds` and `ImpliedProbability` are all `Odds` types, and support `.to_american_odds()` `.to_decimal_odds()` and `.to_implied_probability()` methods for easily switching between odds types. 
```python
odds = AmericanOdds(-110)

decimal_odds: DecimalOdds = odds.to_decimal_odds()
print(decimal_odds.value)
# >>> 1.909090909090909090909090909

implied_probability: ImpliedProbability = odds.to_implied_probability()
print(implied_probability.value)
# >>> 0.5238095238095238095238095238
```

Easily compute Parlay odds
```python
odds1 = AmericanOdds(-110)
odds2 = AmericanOdds(-110)

parlay_odds: AmericanOdds = odds1 & odds2
print(parlay_odds.value)
# >>> 264.4628099173553719008264463
```

Easily compute Juice
```python

juice = AmericanOdds(-110) | AmericanOdds(-110)

# Juice can't be represented by american odds, so the type of the juice 
# variable will be "ImpliedProbability" after the computation, which is still an Odds type. 
print(type(juice))
# >>> <class 'degen.odds_models.ImpliedProbability'>

# ImpliedProb > 1.0 provides a measure of "juiced" odds, or the book "vig"
print(juice.value)
# >>> 1.047619047619047619047619048

# You can ask all odds objects if they're "juiced"
print(juice.is_juiced)
# >>> True
```

# Contributing / Developing

Install requirements
```bash
pip install -r requirements-dev.txt -r requirements.txt
```

Run tox suite:

* Run black code fmt checks
* Run unittests
* Check coverage
* Generate coverage report & badge
```
tox
```

Test coverage has a floor of 95% - this will block a PR from getting approval if this threshold isn't met. 

## Todo

Contributions from other developers are always welcome, here are some things that need to be implemented:

* Fractional Odds
* Hong Odds 

### Notes

 * Everythign done with Decimals for numerical precision
