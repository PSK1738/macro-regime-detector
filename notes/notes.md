## 01/06/2026 - 05/06/2026 - Introduction

This project will build upon well-known literature on the probabilistic modelling of hidden macroeconomic regimes (Hamilton 1989 & Filardo 1994). 

Focus on simplicity and robustness i.e. Occam's Razor. Many potential regimes, such as bubbles, recessions, hawkish CBs ect. With data lags, transmission lags and decision lags (CGG 1999), it is clear complex models suffer from overfitting and provide no predictive power (as stressed by BNP Parisbas macro analyst). With only 11 recessions since WW2, giving around 50 quarters of recession data, complex models reliant on many parameters are useless. We will start considering Hamilton's simplification of 2 regimes: expansion and recession. 

- James Hamilton — concise summary: (see https://econbrowser.com/recession-index)
    The NBER's recession dates are authoritative but subjective and often delayed, raising concerns about timeliness and political independence. This motivates a purely data-driven approach to identifying recessions automatically. The key tradeoff is between using rich detailed data versus keeping the model simple and robust to economic change and data revisions.

    ---

    1. The NBER's recession-dated quarters show a wide spread of GDP growth outcomes. While recessions are associated with contraction on average, 19 of the 45 NBER recession quarters recorded positive real GDP growth — highlighting that NBER classification and raw GDP growth are far from synonymous.

    2. The same distribution for NBER expansion quarters shows growth is typically positive, though 10 expansion quarters nonetheless recorded negative real GDP growth.

    3. Observed GDP growth can be modelled as a mixture of two normal distributions. With recessions comprising roughly 20% of postwar quarters and expansions 80%, weighting each density accordingly and summing gives the unconditional distribution of GDP growth.

    4. A GDP growth reading of −6% sits almost entirely under the recession distribution, making recession highly probable. More formally, the ratio of the recession density to the mixture density (see images) at any point is exactly the posterior probability of recession given that growth rate i.e. Bayes' rule.

Forward algorithm: We use the fact that regimes are persistent: expansion continues into next quarter with ~95% probability, recession with ~75%. We use last quarter's inferred regime as an informative prior when applying bayes' rule to current quarter. This will yield a real-time probability of recession at each date given all gdp data oberved till that point.


## Backward smoothing - improve past estimates but as this is a M.C. this is irrelevant to forward prediction.

Our current recession probability at time t, uses all data up to time t. We can now work backwards. For example, if we observe −6% growth this quarter, that is strong evidence of recession now, and given that recessions persist, it raises the probability that recession had already begun last quarter.


**The decision rule**
To make a binary call Hamilton uses two asymmetric thresholds. A recession is declared when the index >= 67%, and ended when it falls below 33% (so we are very confident that we are in recession). Start and end dates are assigned as the most recent quarter where P(recession) was above or below 0.5, anchoring the dates to where the model thinks the turning point actually was rather than when you became confident enough to announce it.

**The COVID problem - CLAUDE SUMMARY**
    The 2020:Q2 reading was −28% annualised (Hamilton's original paper quotes −31%; the difference is due to subsequent BEA data revisions — FRED returns the latest revised vintage, not the real-time advance estimate Hamilton used).

    Hamilton's solution was to estimate parameters on all data from 1947:2020 Q1 as the Q2 and Q3 recordings were such outliers and would distord the MLE's. 

    The filter still runs through all quarters including Q2, Q3, and beyond — new data continues to generate recession probabilities. 

# Data
Series: A191RL1Q225SBEA (FRED) — Real GDP, percentage change from preceding period, quarterly, seasonally adjusted annual rate (SAAR). Data runs from 1947:Q1 to present, giving 316 quarters as of 2026:Q1.

## 06/06/2026 - Running the forward filter

Reminder of the algorithm:
Initial step - Our predicted expansion/recession probability row vector starts at [0.8, 0.2] (predicted prob), then we update following the observation using Bayes' rule: Prob of expansion/recession given all GDP data up to and including time t is density of GDP obs under expansion/recession times prob of expansion/recession using GDP data not including time t (predicted prob) over prob of observing y_t (i.e. the two entries summed to normalise in order to sum to 1). 

We want to compare the predictive power vs. actual NBER announcement of recessions.

Different data to use and approach:
Advance release: 1 month after quarter ends
Revised release: 2 months after quarter ends
Final release: 3 months after quarter ends

Now we will try to used unrevised, higher frequency data to improve predictions of current GDP.