data {
    // Dimensional parameters
    int<lower=1> J; // Number of biological replicates
    int<lower=1> K; // Number of technical replicates
    int<lower=1> N; // Number of total measurements
    int<lower=1, upper=J> biol_idx[K]; // ID vector for biological replicates
    int<lower=1, upper=K> tech_idx[N]; // ID vector for technical replicates

    // Observed parameters
    vector<lower=0>[N] elapsed_time;
    vector<lower=0>[N] optical_density;
}

transformed data {
    vector[N] log_optical_density = log(optical_density);
}

parameters {
    //Level 0
    real<lower=0> mu;
    real<lower=0> mu_tau; 

    // Level 1
    vector[J] mu_1_tilde;
    vector<lower=0>[J] od_init;
    real<lower=0> od_init_tau;

    // Level 2
    vector[K] mu_2_tilde;
    vector[K] od_init_tilde;

    // Singular
    real<lower=0> sigma;
}

transformed parameters { 
    vector[J] mu_1 = mu + mu_tau * mu_1_tilde;
    vector[K] mu_2 = mu_1[biol_idx] + mu_tau * mu_2_tilde;
    vector<lower=0>[K] od_init_1 = od_init[biol_idx] + od_init_tau * od_init_tilde;
    vector[K] log_od_init = log(od_init_1);
}


model { 

    // Growth rate priors
    mu ~ std_normal();
    mu_tau ~ normal(0, 5);
    mu_1_tilde ~ std_normal();
    mu_2_tilde ~ std_normal();

    // Init OD priors
    od_init ~ normal(0, 0.1);
    od_init_tau ~ normal(0, 0.05);
    od_init_tilde ~ std_normal();

    // Singluar priors
    sigma ~ normal(0, 0.1); 

    // Likelihood
    log_optical_density ~ normal(log_od_init[tech_idx] + mu_2[tech_idx] .* elapsed_time, sigma);

}