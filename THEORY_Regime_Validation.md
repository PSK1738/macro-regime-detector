# Regime Validation Theory


As we aren't assessing the correlation between assets at the moment we will exclude:

- Levene test
- Fisher-Z test
- Bonferroni correction 

We consider:

## (1) Numerical Stability Score (𝑠_𝑆𝑇) - Needs to be 1

  Need to ensure when maximising the log-likelihood we are at a genuine peak, not saddle point. We need a negative definite Hessian of the log-likelihood with our optimal parameters θ* =  ((ω_j if TVTP), β_ij).

  We obtain the fisher information,  I_T(θ*) = -H_T(θ*) which we expect to be positive here. This will give us positive eigenvalues

  Our output is κ* = λ_max / λ_min (largest e-val / smallest e-val) i.e. high number implies steep curvature

  The equation to use: s_ST = (1 - 0.9 · 1_{λ_max ≥ 0}) · max(0, 1 - κ*/12) (this checks the Hessian's largest eigenvalue of the log-likelihood, more as just a check)

## (2) Persistance score (𝑠_𝑃)

### Time-invariant trainsition probabilites:

    Trivially the probability of remaining in a regime i is p_ii. So the duration in a given regime follows geometric distribution. We have 

    E[D_i] = 1/(1 - p_ii)

    We can find the stationary distribution solving: 

    π^T P = π^T,  Σ π_i = 1

    After fitting the HMM which gives us the transition matrix, we compare to the oberved proportion of time spent in regime i

    f_i = (1/T) Σ_t 1{ẑ_t = i}

    These should converge. We have limited data so there is some leeway

### TVTP
    Now p_ii varies with time. We use:

    E[D_i | X_1,...,X_T] ≈ (1/T_i) Σ_t [1/(1-p_ii(X_t))] · 1{ẑ_t=i}     where T_i is the number of periods in regime i

    We are averaging the instantaneous expected duration formula from before over each time we are in regime i. 
    Similarly, we use an average transition matric to calculate the stationary distribution

    The score is calculated using:

    s_P = (1/2)[min(1, D_min/D_seuil) + min(1, f_min/f_seuil)]

    Where f_min is the proporiton of time spent in our rarest regime and f_seuil is the minumum threshold for frequency 

    D_min is the minimum duration is a regime and D_seuil is the threshhold

    May be sensible to not use the score and just record the frequency and average duration of each regime and compare to stationary distribution


## (3) Conviction Score (𝑠_𝐶I)

    We have at a given time γ_t,k = P(z_t = k | Y_{1:t}, θ) from the forward-backward algorithm when fitting the HMM

    We want to quantify how sure the model is at a given time rather than just selecting the regime with the highest probability

    Use Shannon entropy (more entropy, more uncertainty)

    H_t = -Σ_k γ_t,k log(γ_t,k) 

    this ranges from 0 (no uncertainty i.e probability 1 of being in a regime) to ln(K) (uniform probability over all regime, where K is number of regimes)

    Use to normalise:

    CI_t = 1 - H_t/ln(K)

    To obtain the score we average over the whole sample 

    s_CI = (1/T) Σ_t CI_t


These are combined to produce the global score:

𝑠𝐺 = 𝑤_𝑆𝑇 · 𝑠_𝑆𝑇 + 𝑤_𝑃 · 𝑠_𝑃 + 𝑤_𝐶𝐼 · 𝑠_𝐶I 

We will use the weights in the paper as a template. Will evenly distribute the separability weight among others
𝑤_𝑆𝑇 = 0.3   𝑤_𝑃 = 0.3  𝑤_𝐶𝐼 - 0.4

However consider not using the score at all at just looking at each individually