data {
    // Dimensional parameters
    int<lower=1> J; // Number of strains and conditions
    int<lower=1> K; // Number of biological replicates
    int<lower=1> N; // Number of measurements
    int<lower=1, upper=J> unique_idx[K]; // ID vector for which biological replicates are associated with which strains
    int<lower=1, upper=K> replicate_idx[N];

    // Observed parameters
    vector<lower=0>[N] elapsed_time;
    vector<lower=0>[N] optical_density;
}

transformed data {
    vector[N] log_optical_density = log(optical_density);
}

parameters {
    //Level 0
    vector<lower=0>[J] mu;
    vector<lower=0>[J] tau;

    // Level 1
    vector[K] mu_1_tilde;

    // Singular
    vector<lower=0>[K] sigma;
    vector<lower=0>[K] od_init;
}

transformed parameters { 
    vector[K] mu_1 = mu[unique_idx] + tau[unique_idx] .* mu_1_tilde[unique_idx];
    vector[J] log_od_init = log(od_init);
}


model { 

    // Priors
    mu ~ std_normal();
    tau ~ normal(0, 5);
    mu_1_tilde ~ std_normal();
    sigma ~ normal(0, 0.1); 
    od_init ~ normal(0, 0.1);

    // Likelihood
    log_optical_density ~ normal(log_od_init[replicate_idx] + mu_1[replicate_idx] .* elapsed_time, sigma[replicate_idx]);

}