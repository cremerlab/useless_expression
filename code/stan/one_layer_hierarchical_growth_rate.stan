data {
    // Dimensional parameters
    int<lower=1> J;
    int<lower=1> N;
    int<lower=1, upper=J> idx[N];

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
    real<lower=0> tau;

    // Level 1
    vector[J] mu_1_tilde;

    // Singular
    real<lower=0> sigma;
    vector<lower=0>[J] od_init;
}

transformed parameters { 
    vector[J] mu_1 = mu + tau * mu_1_tilde;
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
    log_optical_density ~ normal(log_od_init[idx] + mu_1[idx] .* elapsed_time, sigma);

}