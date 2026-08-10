# Theory - PCA: reducing dimensions of our data

We currently have 17 macro indicators. We will use PCA to compress these into a limited number of components, with each component taking a certain weighting (loading) of a specific macro indicator.

PC1​=w1​⋅Continued_claims+w2​⋅Initial_claims+⋯+w17​⋅Log_PPIACO_diff

We use our correlation matrix (which yields the same results as Z-score standardising to form a variance-covariance matrix) for the PCA. 

PCA is the eigendecomposition of the correlation matrix. 

Recall: 

Solve Rv=λv , v is the unit eigenvector containing our 17 weights.

Labelling our 17 indicators x1,...,x17
We wish to find the e-vector v, where v=(w1​,…,w17​)^T , s.t. we form z with the largest possible  variance (as we wish to capture as much of the variance in our data as possible)
 z = w1​x1 ​+ ⋯ + w17​x17 subject to w1^2 ​+ w2^2 ​+ ⋯ + w17^2​ = 1

 Derivation:
x is our vector of macro variables, R is our cov matrix (which is equal to the correlation matrix as we would standardise)
 Variance of z= v^T x  ==> Var(z) =  v^T R v

 Therefore we max v^T R v subject to vT v = 1

 The maximum var direction is our e-vector and langrange multiplier is the e-value:
  L=vT R v − λ(vTv−1) ==>(derivative) 2Rv−2λv=0 ==> Rv=λv
  Var(z) = v^T R v   = v^T (λv)   =λ(vTv)    =λ⋅1    =λ (e-value is equal to the var)

We call PC1 = v^T x (using the normalised e-vector with the largest corresponding eigen-value as we wish to capture the most variance)

To determine the variance captured by each PC one can just calculate 
$$\text{Explained Variance Ratio for } PC_i = \frac{\lambda_i}{\sum_{j=1}^{d} \lambda_j}$$
