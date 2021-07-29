// Hierarchical Model for Inference of Steady-State Growth Rate
// ============================================================
// Author: Griffin Chure
// License: MIT
//

data { 
    // Dimensional parameters
    int<lower=1> J_1; // Number of biological replicates
    int<lower=1> J_2; // Number of technical replicates
    int<lower=1> N; // Number of measurements

    // Identification vectors
    int<lower=1, upper=J_1> J_1_idx[J_2];
    int<lower=1, upper=J_2> J_2_idx[N]; 

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

    //Level-0 parameters
    real theta; // Growth rate location parameter
    real<lower=0> tau; // Growth rate scale parameter

    // level-0 parameters
    vector[J_1] theta_1_tilde;
    vector[J_2] theta_2_tilde;

    // Level-2 (technical replicate) parameters
    real<lower=0> homosced_sigma;
    vector<lower=0>[J_1] od_init;
    vector<lower=0>[J_2] od_init_1_tilde;
    real<lower=0> od_init_tau;

}

transformed parameters {
    vector<lower=0>[J_1] theta_1 = theta + tau * theta_1_tilde;
    vector<lower=0>[J_2] theta_2 = theta_1[J_1_idx] + tau * theta_2_tilde;
    vector<lower=0>[J_2] od_init_1 = od_init[J_1_idx] + od_init_tau * od_init_1_tilde;
}

model {
    // Level-0 prior
    theta_1 ~ normal(0, 1);
    tau ~ normal(0, 1);
    od_init ~ normal(0, 0.1);

    // Level-1 priors
    theta_1_tilde ~ normal(0, 1);
    theta_2_tilde ~ normal(0, 1);
    od_init_1_tilde ~ normal(0, 1);

    // Homoscedastic error
    homosced_sigma ~ normal(0, 0.1);
    log_optical_density ~ normal(theta_2[J_2_idx] .* elapsed_time + od_init_1[J_2_idx], homosced_sigma);
}
