# Theory — Hamilton (1989) Two-State Markov Switching Filter

---

*The problem*

At every quarter t we observe GDP growth y_t. We never observe the regime s_t directly.
The regime is either 0 (expansion) or 1 (recession).

We want to compute, at each quarter t:

    P(s_t = k | y_1, y_2, ..., y_t)

i.e. the probability of being in regime k given all GDP data observed up to and
including quarter t.


*Distribution assumption - MLE without NBER dates*

Hamilton's key insight is that you do not need the NBER to tell you when recessions were. The GDP data itself contains that information, he finds the parameters that make the observed sequence of GDP growth most probable. Those parameters are the recession mean, expansion mean, common variance, and the two transition probabilities (while this seems like an oversimplification we elect for robustness and simplicity). When you do this blind — no NBER dates used at all — you recover parameters almost identical to those obtained by fitting to NBER-classified quarters directly. The model essentially rediscovers the business cycle from GDP alone.

GDP growth is normally distributed within each regime:

    y_t | s_t = 0  ~  N(mu_e, sigma^2)       expansion
    y_t | s_t = 1  ~  N(mu_r, sigma^2)       recession

The variance sigma^2 (= 10.1800) is common to both regimes. The means differ:

    mu_e =  3.87902    mean GDP growth in expansion
    mu_r = -1.51768    mean GDP growth in recession

*Time invariant transition probabilities using Hamilton's results*

The regime follows a Markov chain. The transition matrix P has entries:

    P[i, j] = P(s_t = j | s_{t-1} = i)

    P = | p00      1-p00 |  =  | 0.944   0.056 |    row 0: from expansion
        | 1-p11    p11   |     | 0.304   0.696 |    row 1: from recession

Where:
    p00 = 0.943698    P(stay in expansion | currently in expansion)
    p11 = 0.696427    P(stay in recession  | currently in recession)

Expansions last ~18 quarters onaverage, recessions ~3 quarters. This transition matrix captures the persistence of regimes.

*The probability vector to update given all gdp data*

Following Hamilton (1989) we use a row vector. At each quarter t:

    x_t = [ P(s_t=0 | y_1,...,y_t)   P(s_t=1 | y_1,...,y_t) ]
         = [ P(expansion)   P(recession) ]

Both entries are non-negative and sum to 1.

# The process

## Predict

BEFORE observing y_t, we predict x_t  i.e.  x_{t|t-1} = x_{t-1} @ P

Written out:

    [ P(s_t=0)   P(s_t=1) ] = [ P(s_{t-1}=0)   P(s_{t-1}=1) ] @ | p00      1-p00 |
                                                                   | 1-p11    p11   |

The first element:

    P(s_t=0) = P(s_{t-1}=0) * p00 + P(s_{t-1}=1) * (1-p11)

## Update upon observing y_t

Using the predetermined parameters we find the density of the observation under each regimes distribution. 

    w_t = [ f(y_t | s_t=0)   f(y_t | s_t=1) ]
          = [ N(y_t; mu_e, sigma^2)   N(y_t; mu_r, sigma^2) ]


We use Bayes':
    x_t = (w_t * x_{t|t-1}) / (y_t)

    Written out:

    x_t = (1/f(y_t)) * [ f(y_t|s_t=0) * P(s_t=0|y_1,...,y_{t-1})   f(y_t|s_t=1) * P(s_t=1|y_1,...,y_{t-1}) ]

    where:
        P(y_t) = f(y_t | s_t=0) * P(s_t=0 | y_1,...,y_{t-1})
           + f(y_t | s_t=1) * P(s_t=1 | y_1,...,y_{t-1})

Note that:  P(y_t) = sum(w_t * x_{t|t-1})

## Why this is exactly Bayes' rule - Claude note

Standard Bayes' rule:

    P(A | B) = P(B | A) * P(A) / P(B)

The filter update maps to this term for term:

    Posterior  P(s_t=k | y_1,...,y_t)      — regime probability after seeing y_t
    Likelihood f(y_t | s_t=k)              — how probable is this GDP reading in regime k
    Prior      P(s_t=k | y_1,...,y_{t-1}) — regime probability before seeing y_t
    P(B)       f(y_t)                      — marginal likelihood of y_t, computed via
                                             the law of total probability across both regimes

The one subtlety: in standard Bayes the prior P(A) is unconditional. Here the
prior is already conditioned on all past data y_1,...,y_{t-1} via the predict
step. Each quarter's prior is the previous quarter's posterior propagated
forward through the transition matrix. By the time Bayes' rule is applied at
quarter t, the prior already contains everything learned from 1947 up to t-1.
That is what makes the filter sequential and powerful.

## Starting values:

efore any data, use unconditional postwar frequencies (Hamilton, 1989):

    x_0 = [ 0.80   0.20 ]    (expansion, recession)

The filter then runs forward quarter by quarter from 1947:Q1 to present

## Backward smoothing

The forward filter gives filtered probabilities — conditioned only on data
up to t. The backward smoother refines these using the full sample.

If we observe -6% GDP this quarter, that is strong evidence of recession now.
Given regime persistence, it retroactively raises the probability that recession
had already begun last quarter. Information flows both ways in time.

    Forward pass:  compute P(s_t = k | y_1, ..., y_t)       for t = 1,...,T
    Backward pass: compute P(s_t = k | y_1, ..., y_T)       for t = T,...,1

The result is a smoother, sharper recession probability at each quarter,
conditioned on the entire sample rather than just the past.

---

## The decision rule

The filter output is a continuous probability at each quarter. To make a
binary recession/expansion call, Hamilton uses two asymmetric thresholds:

    Recession declared:  index rises above 0.67
    Recession ended:     index falls below 0.33

Start and end dates are assigned as the most recent quarter where P(recession)
was above or below 0.50, anchoring the dates to where the model thinks the
turning point actually was rather than when you became confident enough to
announce it.
