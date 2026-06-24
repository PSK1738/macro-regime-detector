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


### Backward smoothing - improve past estimates but as this is a M.C. this is irrelevant to forward prediction.

Our current recession probability at time t, uses all data up to time t. We can now work backwards. For example, if we observe −6% growth this quarter, that is strong evidence of recession now, and given that recessions persist, it raises the probability that recession had already begun last quarter.


**The decision rule**
To make a binary call Hamilton uses two asymmetric thresholds. A recession is declared when the index >= 67%, and ended when it falls below 33% (so we are very confident that we are in recession). Start and end dates are assigned as the most recent quarter where P(recession) was above or below 0.5, anchoring the dates to where the model thinks the turning point actually was rather than when you became confident enough to announce it.

**The COVID problem - CLAUDE SUMMARY**
    The 2020:Q2 reading was −28% annualised (Hamilton's original paper quotes −31%; the difference is due to subsequent BEA data revisions — FRED returns the latest revised vintage, not the real-time advance estimate Hamilton used).

    Hamilton's solution was to estimate parameters on all data from 1947:2020 Q1 as the Q2 and Q3 recordings were such outliers and would distord the MLE's. 

    The filter still runs through all quarters including Q2, Q3, and beyond — new data continues to generate recession probabilities. 

### Data
Series: A191RL1Q225SBEA (FRED) — Real GDP, percentage change from preceding period, quarterly, seasonally adjusted annual rate (SAAR). Data runs from 1947:Q1 to present, giving 316 quarters as of 2026:Q1.

## 06/06/2026 - Running the forward filter

Reminder of the algorithm:
Initial step - Our predicted expansion/recession probability row vector starts at [0.8, 0.2] (predicted prob), then we update following the observation using Bayes' rule: Prob of expansion/recession given all GDP data up to and including time t is density of GDP obs under expansion/recession times prob of expansion/recession using GDP data not including time t (predicted prob) over prob of observing y_t (i.e. the two entries summed to normalise in order to sum to 1). 

We want to compare the predictive power vs. actual NBER announcement of recessions.

Different data to use and approach:
Advance release: 1 month after quarter ends
Revised release: 2 months after quarter ends
Final release: 3 months after quarter ends

Potentially aim to use unrevised, higher frequency data to improve predictions of current GDP. 

## 07/06/2026 - Dating Business cycle turning points Hamilton (2005)

Atlanta Fed's GDPNow / Alternatives

For live trading we will use Atlanta Fed's dynamic factor model to obtain the best live estimates for real GDP growth.
Problem: only the most revised historical estimates are available, look for new approach

We will read the paper to understand a potential approach to estimate proabilities live.

- Paper key notes/quotes:   
    Our recommendation is that one should wait until one extra quarter of GDP growth is reported or one extra month of the monthly indicators released before making a call of a business cycle turning point. (we will implement a probabilistic model to trade, not formal announcement)
    We introduce two new measures for dating business cycle turning points, which we call the “quarterly real-time GDP-based recession probability index” and the “monthly real-time multiple-indicator recession probability index” that incorporate these principles. Both indexes perform quite well in simulation with real-time data bases. We also discuss some of the potential complicating factors one might want to consider for such an analysis, such as the reduced volatility of output growth rates since 1984 and the changing cyclical behavior of employment. Although such re…nements can improve the inference, we nevertheless recommend the simpler speci…cations which perform very well historically and may be more robust for recognizing future business cycle turning points of unknown character.

### SHIFT: We aim to form a Ranked-Asset-Allocation-model based on performance of different assets in each regime. To begin we will simply look at S&P500 and 10-Year Treasury yield

First need to find better data to estimate recession probability.
We will now make a new forawrd filter using a regularly updated piece of data correlated to expansion/recession.


The main indicators we will consider (to then implement all 5 in a multivariate HMM) based on:
https://www.forbes.com/sites/bill_stone/2025/03/23/five-critical-indicators-to-gauge-recession-risk/
1) Jobs - Initial claims for unemployement benefits (weekly) & ongoing claims.
2)Credit spread 
3)Financial conditions - "The Chicago Fed produces the National Financial Conditions Index weekly. It looks at 105 measures across three categories, risk, credit, and leverage, to create a measure of financial conditions. According to the Chicago Fed, “Positive values of the NFCI have been historically associated with tighter-than-average financial conditions, while negative values have been historically associated with looser-than-average financial conditions.” The chart shows that these periods of tighter-than-normal financial conditions have often been associated with recession." 
4)Cyclical stock performance
5)The yield curve - "The 10-year Treasury minus 2-year yield is probably the most well-known predictor of recession. Historically, when the yield on the U.S. 10-year Treasury falls below the 2-year yield, also called yield curve inverting, a recession is coming. Since the 1970s, a yield curve inversion has occurred before every recession. The only blemishes on its record are the 1998 and mid-2022 inversions, which produced no subsequent economic recessions. The U.S. economy did see a significant slowdown in the first half of 2022 but rebounded in the second half. Unfortunately, even when the signal is correct, it has variable lead and lag times. The yield curve still has a better prediction track record than the economists and is used in about every Federal Reserve model, so it is worth watching despite its warts."

TASK: Read ENSAE paper to understand how to classify regimes and parameters with different data.

https://media.licdn.com/dms/document/media/v2/D4E1FAQH8cU3hFbrFXg/feedshare-document-pdf-analyzed/B4EZ6HB1KgLAAY-/0/1780381867618?e=1781136000&v=beta&t=pBtTNe3vn14uvyIFOX1L3R1CKGKMbfLN2t8ZhyUYPZ8

## 08/06/2026 - ENSAE paper notes (aim to understand the paper and all code in order to build on it and experiment)

"Correlation between equities and bond is non-stationary - positive during the stagflation of the 1970s, durably negative after the year 2000, and positive once again during the post-COVID inflationary cycle of 2022–2024." 

We can't just look at the correlation but also the volatility, the negative correlation during 2000 is very different to the negative correlation observed in 2008. Aim to find latent states to capture the non-stationarity

### KEY IDEAS (Introduction):

Use market data to identify regimes (S&P 500 and 10 Year Treasury Yield data), use macro data to identify regimes, check if they agree. The macro variables are used to update transition matrix (TVTP) rather than used to estimate probability of being in a certain regime. 

### 4 "scores" considered to check validity of regimes:

#### Separability:
 are the regimes actually different. Check if volatilities significantly differet (Levene test) and is the equity bond correlation significantly different (Fisher-Z tests).

#### Numerical stability:
Hessian must be negative definite - all eigenvalues negative. We are maximising likelihood function using EM algorithm. We must compare the difference between the largest and the smallest eigenvalue. The difference must be sufficienty small. We have that max eigenvalue is curvature in steepest direction and min is curvature in flattest. If curvature is almost flat w.r.t. a parameter, our estimate is meaningless.

#### Persistence:
Regimes must last suffiently long to be economically meaningful (e.g. months/years)

#### Model conviction:
They measure this via Shannon entropy — low entropy means the model is decisive, high entropy means it's constantly uncertain. They normalise this into a confidence index between 0 and 1.

----------------------------------------------------------------------------------------------------------------------------------

They use an expanding window so when backtesting, no future data is used

### Key Ideas (Section 2 - Literaure review)

#### 2.1 Instability of the equity-bond correlation and macroeconomic drivers

"The non-stationarity of the equity–bond correlation is well documented. Historically,
this correlation remained predominantly positive between the 1970s and the 1990s, in an environment
marked by supply shocks and high inflation. It subsequently turned negative from the bursting of the
dot-com bubble onwards, with bonds increasingly playing the role of a safe-haven asset. This negative
regime, which long supported diversification strategies, was nonetheless called into question during the
inflationary cycle of 2022–2024, a period in which equities and bonds declined simultaneously"

## 12/06/2026 - Continued

Czasonis et al. (2021) -

    Measuring the equity-bond correlation tells us nothing when we use long horizon data. The correlation depends heavily on the monthly data chosen, we need to remove distortion of the autocorrelation of the returns of equities and bonds as trending will show as correlation. Spurious regression. Use single-period correlation.

    Four main determinants of correlation:
    1) economic growth - strong growth = buy equity, sell bonds
    2) high unexpected infaltion - both go down (bonds price down as yield up and equities down as fear increases and discount rate increases)
    3) relative return of equities vs. bonds - if one has outperformed recently investors rebalance which turns corrlation negative
    4) relative volatility - e.g. uncertainty over rates can make bonds riskier so correlation turns positive

Brach (2025) - rolling windows (e.g. 30 months) are reactive and only gradually determine a change in regime, we want a clear break.

Burghardt and Liu (2012): annual vol = daily vol × √252 and Sharpe ratio use our standard calculated variance which assumed i.i.d returns. As returns are autocorrelated the true variance is potentially larger or smaller. 

Claude clean summary: 
    expansion regime  → mean reversion dominates
                    → negative autocorrelation in spread
                    → √T overstates risk
                    → negative equity-bond correlation stable

    crisis regime     → momentum/panic dominates  
                    → positive autocorrelation
                    → √T understates risk
                    → correlation flips positive

One can argue the flips between a mean-reverting spread between equities and bonds (i.e. negatively autocorrelated returns) combined with divergence in the spread through positively autocorreleated returns as equities are higher risk balance out our variance measures. The biases are regime-dependent and flip sign at the worst possible time — underestimating risk in crises when you most need accuracy.

#### 2.2 - Probabilistic modelling of financial regimes

Based on Hamilton (1989) each regime is accociated with a specific regime of return, volatility and correlation
Extension from time-invariance transition probabilities: 

"The extension to time-varying transition probabilities (Time-Varying Transition Probabilities, TVTP),
developed notably by Filardo (1994) and Diebold et al. (1994), introduces a dependence of these probabilities on observable macroeconomic variables, such as inflation, interest rates, or credit spreads. This extension is particularly relevant to the present work, since it makes it possible to test explicitly whether 2
transitions between market regimes are influenced by the macroeconomic environment. It thus paves the
way for a dynamic allocation conditioned on the available macroeconomic information."

#### 2.3 - Inflationary regimes and asset behaviour

Long-term average correlations between assets and inflation mask substantial heterogeneity across
the regimes. Dependent on the source of inflation different assets provide better hedges. 

### Key Ideas - Section 3 (Empirical evidence of non-stationarity and regimes)

The student-t distribution fits the returns better (as shown by small degress of freedom accounting for fatter tails), but we will use the normal in order to get the closed-form solution and "Mean-variance portfolio optimisation (Markowitz) is built entirely on normality — if returns are normal, variance fully describes risk and you get clean analytical solutions for optimal weights. Switch to Student-t and the optimisation becomes much messier."

We transform macro variables to become stationary and use ADF to check there is no unit root.

## 15/06/2026 - cont.

interesting correlation matrix between macro variables in appendix i.e. negative correlation between credit spead and yield curve slope. This matrix ensures we consider potential multicollinearity issues and redundancy.

## 17/06/2026

understanding correlation-based PCA and how we will use it to identify the key macro variable.

First using the Forbes article we will use:

Jobs - Continued Claims (Insured Unemployment) (CCSA) & Initial claims (ICSA) (BOTH WEEKLY)

Credit Spread - Moody's Seasoned Baa Corporate Bond Yield Relative to Yield on 10-Year Treasury Constant Maturity (BAA10Y) (DAILY)

Financial conditions - Chicago Fed National Financial Conditions Index (NFCI) (WEEKLY)

Cyclical stock performance - UNCERTAIN

Yield curve - 10-Year Treasury Constant Maturity Minus 2-Year Treasury Constant Maturity (T10Y2Y)

(while PCA isn't really justified for a small number of variable we will add more)
we must stationarise variables and note that aggregrating data to comparable timeframes is simple but advanced econometric methods exist to smoothen this e.g. Mixed data sampling (MIDAS).

We use a correlation matrix to not concern ourselves with scaling the variables.

for each we need - to first stationarise our variable to get a meaningful correlation (otherwise spurious), then we need to aggregate to monthly.

### Stionarising and aggregating 

- Continued Claims (Insured Unemployment) (CCSA) - people currently recieving unemployment benefits, we will use the monthly average, and is already statistically stationary
- Initial claims (ICSA) - new filings for unemployment benefits in a week, use monthly avg, is stationary
- Moody's Seasoned Baa Corporate Bond Yield Relative to Yield on 10-Year Treasury Constant Maturity (BAA10Y)  - take end of month end of month value, already stationary
- Chicago Fed National Financial Conditions Index (NFCI) - take end of month, already stationary

## 19/06/2026

Create a loop to pull data for different macro variables (adding variables included in the paper)
We will include macro variables:

Continued Claims (Insured Unemployment) (CCSA) (weekly)
Initial Claims (ICSA) (weekly)
Moody's Seasoned Baa Corporate Bond Yield Relative to Yield on 10-Year Treasury Constant Maturity (BAA10Y) (daily)
Chicago Fed National Financial Conditions Index (NFCI) (weekly)
10-Year Treasury Constant Maturity Minus 2-Year Treasury Constant Maturity (T10Y2Y) (daily)

Consumer Price Index for All Urban Consumers: All Items in U.S. City Average (CPIAUCSL) (monthly, infaltion)
Industrial Production: Total Index (INDPRO) (monthly, real output)
3-Month Treasury Bill Secondary Market Rate, Discount Basis (TB3MS) (monthly, eflection of current baseline interest rate)
Crude Oil Prices: West Texas Intermediate (WTI) - Cushing, Oklahoma (DCOILWTICO) (daily, track global energy markets)
Capacity Utilization: Total Index (TCU) (monthly, percent of availiable indistrial capacity being used)
Unemployment Rate (UNRATE)(monthly)
University of Michigan: Consumer Sentiment (UMCSENT) (monthly)
Commercial and Industrial Loans, All Commercial Banks (BUSLOANS) (monthly) 
Capacity Utilization: Manufacturing (SIC) (CUMFNS) (monthly, capacity utilisation for manufacturing sector)
M2 (M2SL) (monthly, how much cash and highly liquid funds circulating economy)
All Employees, Total Nonfarm (PAYEMS) (monthly)
Producer Price Index by Commodity: All Commodities (PPIACO) (monthly)


KEY: Common sample starts 1986-02 due to WTI/BAA10Y FRED history; this still spans 5 major macro-financial regime episodes.

## 22/06/2026 - PCA + Key correlations

Now we have completed the correlation matrix of macro variables, understand PCA.

For reference ENSAE PCs following PCA (Gemini Summary):

    🛠️ PC1: Industrial Activity Indicators
    Log_INDPRO_diff (Industrial Production): High Positive
    TCU_diff (Capacity Utilization): High Positive
    Log_PAYEMS_diff (Total Nonfarm Payroll Employment): High Positive
    UNRATE_diff (Unemployment Rate): High Negative


    🎈 PC2: Inflation Dynamics

    Log_CPI_diff (Consumer Price Index): High Positive
    Log_PPIACO_diff (Producer Price Index): High Positive
    WTI_Returns (Crude Oil Prices): High Positive


    🏦 PC3: Monetary & Financial Conditions

    NFCI (National Financial Conditions Index): High Positive
    Credit_spread: High Positive
    Slope (Yield Curve Slope): Moderate Negative
    TB3MS_diff (3-Month Treasury Bill Rate): Moderate Positive


    💸 PC4: Supply Shocks & Liquidity Contraction

    Log_PPIACO_diff (Producer Price Index): +0.55
    Log_M2SL_diff (M2 Money Supply): -0.55
    Log_BUSLOANS_diff (Commercial & Industrial Loans): -0.31


    🎭 PC5: Consumer Confidence & Short-Term Policy Shocks
    
    UMCSENT_diff (University of Michigan Consumer Sentiment): +0.68
    TB3MS_diff (3-Month Treasury Bill Rate): +0.53


    📈 PC6: Yield Curve Steepening & Market Sentiment
    
    UMCSENT_diff (University of Michigan Consumer Sentiment): +0.50
    Log_PPIACO_diff (Producer Price Index): +0.43
    Slope (Yield Curve Slope): +0.41
    TB3MS_diff (3-Month Treasury Bill Rate): -0.40


    📉 PC7: Corporate Profit Margin Compression
    Log_PPIACO_diff (Producer Price Index): +0.54
    Log_CPI_diff (Consumer Price Index): -0.47
    Slope (Yield Curve Slope): -0.31
    Log_PAYEMS_diff (Total Nonfarm Payroll Employment): -0.28

Made good progress, see Macro_variables_stationarity_correlation notebook.

Next: Go through PCA theory and run PCA if possible

## 24/06/2026

Including COVID 
Conduct the PCA and determine what each componenet signifies. We observe under Kaiser's rule (taking PC's with e-values larger than 1) we would use PC1 - PC5. However PC1 - PC6 captures 80.01% of the variance.

Before deciding I will analyse the PC's to determine if each represent an "economic story". See findings of notebook for analysis of componenets.


