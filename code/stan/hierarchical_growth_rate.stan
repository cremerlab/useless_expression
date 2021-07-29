// Hierarchical Model for Inference of Steady-State Growth Rate
// ============================================================
// Author: Griffin Chure
// License: MIT
//

data { 
    // Dimensional parameters
    int<lower=1> J; // Number of biological replicates
    int<lower=1> K; // Number of technical replicates
    int<lower=1> N; // Number of measurements

    // Identification vectors
    int<lower=1, upper=J> J_idx[K];
    int<lower=1, upper=K> K_idx[N]; 

    // Measured parameters
    vector<lower=0>[N] elapsed_time;
    vector<lower=0>[N] optical_density;
}

transformed data {
    // Compute the log transform of the optical density to transform this to a 
    // linear model
    vector[N] log_optical_density = log(optical_density);
}

parameters {
    // level-0 parameters
    real growth_rate_mu_l0;
    real<lower=0> growth_rate_sigma;

    // Level-1  (biological replicate) parameters
    vector[J] growth_rate_mu_l1_tilde;
    vector<lower=0>[K] od_init_mu;
    vector<lower=0>[K] od_init_sigma;

    // Level-2 (technical replicate) parameters
    vector[K] growth_rate_tilde;
    real<lower=0> homosced_sigma;
    vector<lower=0>[K] od_init;

}

transformed parameters {
    vector<lower=0>[J] growth_rate_mu_l1 = growth_rate_mu_l0 + growth_rate_sigma * growth_rate_mu_l1_tilde;
    vector<lower=0>[K] growth_rate = growth_rate_mu_l1[J_idx] + growth_rate_sigma * growth_rate_tilde;
}

model {
    vector[N] mu;

    // Level-0 prior
    growth_rate_mu_l0 ~ normal(0, 1);
    growth_rate_sigma ~ normal(0, 0.5);

    // Level-1 priors
    growth_rate_mu_l1_tilde ~ normal(0, 1);  
    od_init_mu ~ normal(0, 0.1);
    od_init_sigma ~ normal(0, 0.1);

    // Level-2 priors
    growth_rate ~ normal(growth_rate_mu_l1[J_idx], growth_rate_sigma);
    od_init ~ normal(od_init_mu, od_init_sigma);
    homosced_sigma ~ normal(0, 0.01); 

    // Compute the theoretical mean
    log_optical_density ~ normal(growth_rate[K_idx] .* elapsed_time + od_init[K_idx], homosced_sigma);
}