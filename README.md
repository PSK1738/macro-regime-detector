# Macro Regime Detector

Key topic I'll be studying in my MSc Statistics programme. Not trying to produce a paper here, just exploring, understanding, and modifying the approach myself.

Implementation of Hamilton's (1989) two-state Hidden Markov Model in Python, categorising US business cycles into expansion and recession using FRED API data.

## Overview

Built a forward filter from scratch based on Hamilton (1989) to pull latent economic regimes out of macro indicators. Started as a 2-regime univariate model, extended to a full multivariate version, then extended again with a Time-Varying Transition Probability (TVTP) model, where transitions between regimes depend on macro covariates instead of being fixed.

No market or asset data here, no allocation, no trading. Kept the scope to regime detection.

## Methodology

1. **Univariate Hamilton filter** — implemented the 2-regime forward filter using GDP data, checked against NBER recession dating.
2. **Multivariate extension** — 17 macro indicators from FRED, stationarised and ADF-tested.
3. **PCA** — explored correlation structure, reduced dimensionality, ran on the full sample and with COVID excluded
4. **Pure macroeconomic HMM** — multivariate Gaussian-emission HMM using 7 macro indicators, number of regimes selected using AIC/BIC and economic intuition, checked with numerical stability, comparison of empirical results to theoretical stationary distribution , and Shannon entropy.
5. **HMM-TVTP** — transition probabilities exploration, use smm, credit spread and continued claims as inputs, z-score normalise & 2 month lag, initial weightings estimated using logistic regression, omit COVID single data point for calculation

## Structure

ENSAE_paper_exploration/

├── 1-Macro_Variables_trial.ipynb

├── 2-Macro_Variables_Stationarity_Correlation.ipynb

├── 3-Full_Sample_PCA.ipynb

├── 4-PCA_excl_COVID.ipynb

├── 5-Pure_Macro_HMM.ipynb

└── 6-TVTP_Macro_HMM.ipynb

notes/

└── notes.md # working notes, kept informal

THEORY_Hamilton.md # derivation notes, forward filter

THEORY_PCA.md # PCA derivation and interpretation

THEORY_Regime_Validation.md # stability, transition significance, persistence checks

THEORY_TVTP.md # TVTP derivation and estimation

## Acknowledgements

ENSAE Paris applied statistics project by Benisti, Haddadi, Memet, and Thinot (2025-2026) on equity-bond correlation regimes for the project inspiration. 