data {
    // Dimensional parameters
    int<lower=1> J; // Number of biological replicates
    int<lower=1> K; // Number of technical replicates 
    int<lower=1> N; // Number of measurements for postshift growth

    // Identification vectors
    int<lower=1, upper=J> biol_idx[K];
    int<lower=1, upper=K> tech_idx[N]; 

    // Observed parameters
    vector<lower=0>[N] elapsed_time;
    vector<lower=0>[N] optical_density;

    // Calculated parameters
    vector<lower=0>[K] shift_optical_density; // Stationary OD for each technical replicate
    vector<lower=0>[K] t_init; // Time for the beginning of the shift for each replicate.
}

transformed data {
    vector[K] log_shift_od = log(shift_optical_density);
    vector[N] log_od_rescaled = log(optical_density) - log_shift_od[tech_idx];
    vector[N] time_shifted = elapsed_time - t_init[tech_idx];
}

parameters { 
    real<lower=0> mu; // Growth rate
    real<lower=0> mu_tau;  // Variance for growth rate.
    real theta; // y-intercept
    real<lower=0> theta_tau; // variance for y-intercept

    // Level 1
    vector<lower=0>[J] mu_1_tilde; 
    vector[J] theta_1_tilde; // Y intercept for growth on medium 1

    // Level 2
    vector[K] mu_2_tilde;
    vector[K] theta_2_tilde;

    // Singular
    real<lower=0> sigma;
}


transformed parameters {
    // Uncentering operations
    vector[J] mu_1 = mu + mu_tau * mu_1_tilde;
    vector[J] mu_2 = mu_1[biol_idx] + mu_tau * mu_2_tilde;
    vector[J] theta_1 = theta + theta_tau * theta_1_tilde;
    vector[J] theta_2 = theta_1[biol_idx] + theta_tau * theta_2_tilde;
}   


model {   
    
    // Growth rates priors
    mu ~ std_normal();
    mu_1_tilde ~ std_normal();
    mu_2_tilde ~ std_normal();
    mu_tau ~ normal(0, 5);

    // Init OD priors
    theta ~ std_normal();
    theta_1_tilde ~ std_normal();
    theta_2_tilde ~ std_normal();
    theta_tau ~ normal(0, 0.1);

    // Singular priors
    sigma ~ normal(0, 0.1);

    // Likelihood
    log_od_rescaled ~ normal(mu_2[tech_idx] .* time_shifted + theta_2[tech_idx], sigma);
}

generated quantities { 
    real delta = -theta / mu;
}