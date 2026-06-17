# Macro Regime Detector

Implementation of Hamilton's (1989) two-state Hidden Markov Model in Python, 
categorising US business cycles into 2 states: expansion and recession using FRED API data.

**Status: In Progress**

## Content
- `notebooks/` — main project: forward filter, NBER data (for now...)
- `ENSAE_paper_exploration/` — exploration of equity-bond correlation regimes, to include Principal component analysis on macro indicators and ADF stationarity testing
- `notes/` — thought process throughout the project
- `theory/` — key algorithms and mathematical derivations

## Next Steps
- Time-varying transition probabilities (Filardo 1994) driven by PCA macro indicators
- End Goal: Produce a clean write up of findings and implementation of statistical, econmetric and probabilistic methods. 
