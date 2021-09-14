data {
    // Dimensional parameters
    int<lower=1> J; // Number of biological replicates
    int<lower=1> K; // Number of technical replicates 
    int<lower=1> N; // Number of measurements

    // Identification vectors
    int<lower=1, upper=J> biol_idx[K];
    int<lower=1, upper=K> tech_idx[N]; 

    // Observed parameters
    vector<lower=0>[N] elapsed_time;
    vector<lower=0>[N] optical_density;

    // Calculated parameters
    vector<lower=0>[K] shift_optical_density; // Stationary OD for each technical replicate
    vector<lower=0>[K] shift_time_init;
}

transformed data {
    vector[K] log_shift_od = log(shift_optical_density);
    vector[N] log_od_rescaled = log(optical_density) - log_shift_od[tech_idx];
    vector[N] elapesd_time_rescaled = elapsed_time - shift_time_init;

}

parameters { 
    real<lower=0> mu_preshift; // Growth rate
    real<lower=0> mu_postshift; // Growth rate
    real<lower=0> mu_tau;  // Variance for growth rate.
    real theta_preshift; // y-intercept
    real theta_postshift; // y-intercept
    real<lower=0> theta_tau; // variance for y-intercept

    // Level 1
    vector[J] mu_preshift_1_tilde; 
    vector[J] mu_postshift_1_tilde; 
    vector[J] theta_preshift_1_tilde; // Y intercept for growth on medium 1
    vector[J] theta_postshift_1_tilde; // Y intercept for growth on medium 1

    // Level 2
    vector[K] mu_preshift_2_tilde;
    vector[K] mu_postshift_2_tilde;
    vector[K] theta_preshift_2_tilde;
    vector[K] theta_postshift_2_tilde;

    // Singular
    real<lower=0> sigma;
}


transformed parameters {
    // Uncentering operations
    vector[J] mu_preshift_1 = mu_preshift + mu_tau * mu_preshift_1_tilde;
    vector[J] mu_postshift_1 = mu_postshift + mu_tau * mu_postshift_1_tilde;
    vector[K] mu_preshift_2 = mu_preshift_1[biol_idx] + mu_tau * mu_preshift_2_tilde;
    vector[K] mu_postshift_2 = mu_postshift_1[biol_idx] + mu_tau * mu_postshift_2_tilde;
    vector[J] theta_preshift_1 = theta_preshift + theta_tau * theta_preshift_1_tilde;
    vector[J] theta_postshift_1 = theta_postshift + theta_tau * theta_postshift_1_tilde;
    vector[K] theta_preshift_2 = theta_preshift_1[biol_idx] + theta_tau * theta_preshift_2_tilde;
    vector[K] theta_postshift_2 = theta_postshift_1[biol_idx] + theta_tau * theta_postshift_2_tilde;
}   


model {   

    // Growth rates priors
    mu_preshift ~ std_normal();
    mu_postshift ~ std_normal();
    mu_preshift_1_tilde ~ std_normal();
    mu_postshift_1_tilde ~ std_normal();
    mu_preshift_2_tilde ~ std_normal();
    mu_postshift_2_tilde ~ std_normal();
    mu_tau ~ normal(0, 5);

    // Init OD priors
    theta_preshift ~ std_normal();
    theta_postshift ~ std_normal();
    theta_preshift_1_tilde ~ std_normal();
    theta_postshift_1_tilde ~ std_normal();
    theta_preshift_2_tilde ~ std_normal();
    theta_postshift_2_tilde ~ std_normal();
    theta_tau ~ normal(0, 0.1);

    // Singular priors
    sigma ~ normal(0, 0.1);

    // Likelihood
    log_od_preshift_rescaled ~ normal(mu_preshift_2[tech_idx_preshift] .* elapsed_time_preshift + theta_preshift_2[tech_idx_preshift], sigma);
    log_od_postshift_rescaled ~ normal(mu_postshift_2[tech_idx_postshift] .* elapsed_time_postshift + theta_postshift_2[tech_idx_postshift], sigma);

}

generated quantities { 
    real delta = (-theta_postshift / mu_postshift) - (-theta_preshift / mu_preshift);
}