# Degen 

*pronounced "dee-gen"*

### A clean approach to programming with betting odds

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



### Features

 * Everythign done with Decimals for numerical precision
