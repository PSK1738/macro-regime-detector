# Theory - TVTP

In standard HMM p_ij is constant. 

Now we take p_ij(Xt) where Xt is our vector of macro-economic variables at time t

β_ij is essentially the baseline tendency to transition from state i to j

ω_j is the weighting vector (same dimension as Xt) which is the effect od maco variables of wanting to move into regime j.

The formula is the same as logistic regression we've seen before:

p_ij(X_t) = exp(β_ij + ω_j^T X_t) / Σ_k exp(β_ik + ω_k^T X_t)

To find ω and β we must use numerical estimation methods:

Uses the EM algorithm: 
- given current estimate of all paramter run forward backward algorith to find posterior probability of being in each regime at each time
- L-BFGS (quais-Newton method) will iteratively adjust ω_j and β_ij to max the expected complete-data log-likelihood from expectation step. This is essentially fitting onto a wighted logistic regression model where X_t are the regressors and ω_j and β_ij take the role of the intercept/coefficients

To implement we use ssm library