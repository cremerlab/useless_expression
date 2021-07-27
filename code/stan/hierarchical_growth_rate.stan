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
    int<lower=1, upper=J> biol_rep_idx[K];
    int<lower=1, upper=K> tech_rep_idx[N]; 

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
    real<lower=0> growth_rate_mu_mu_l0;
    real<lower=0> growth_rate_mu_sigma_l0;
    real<lower=0> growth_rate_sigma_mu_l0;
    real<lower=0> growth_rate_sigma_sigma_l0;

    // Level-1  (biological replicate) parameters
    vector<lower=0>[J] growth_rate_mu_l1;
    vector<lower=0>[J] growth_rate_sigma_l1;
    vector<lower=0>[J] homosced_sigma_mu_l1;
    vector<lower=0>[J] homosced_sigma_sigma_l1;
    vector<lower=0>[K] od_init_mu;
    vector<lower=0>[K] od_init_sigma;

    // Level-2 (technical replicate) parameters
    vector<lower=0>[K] growth_rate;
    vector<lower=0>[K] homosced_sigma;
    vector<lower=0>[K] od_init;

}

model {
    vector[N] mu;

    // Level-0 prior
    growth_rate_mu_mu_l0 ~ normal(0, 1);
    growth_rate_mu_sigma_l0 ~ normal(0, .1);
    growth_rate_sigma_mu_l0 ~ normal(0, .1);
    growth_rate_sigma_sigma_l0 ~ normal(0, .1);

    // Level-1 priors
    growth_rate_mu_l1 ~ normal(growth_rate_mu_mu_l0, growth_rate_mu_sigma_l0);
    growth_rate_sigma_l1 ~ normal(growth_rate_sigma_mu_l0, growth_rate_sigma_sigma_l0); 
    homosced_sigma_mu_l1 ~ normal(0, 1);
    homosced_sigma_sigma_l1 ~ normal(0, 1);
    od_init_mu ~ normal(0, 0.1);
    od_init_sigma ~ normal(0, 0.1);

    // Level-2 priors
    growth_rate ~ normal(growth_rate_mu_l1[biol_rep_idx], growth_rate_sigma_l1[biol_rep_idx]);
    homosced_sigma ~ normal(homosced_sigma_mu_l1[biol_rep_idx], homosced_sigma_sigma_l1[biol_rep_idx]);
    od_init ~ normal(od_init_mu, od_init_sigma);
    
    // Compute the theoretical mean
    mu = growth_rate[tech_rep_idx] .* elapsed_time + od_init[tech_rep_idx];
    log_optical_density ~ normal(mu, homosced_sigma[tech_rep_idx]);
}
