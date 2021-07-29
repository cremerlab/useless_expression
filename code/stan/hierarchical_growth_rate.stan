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
    real<lower=0> theta;
    real<lower=0> tau;

    // Level 1
    // vector[J] theta_1_tilde;
    vector<lower=0> [J] theta_1;

    // Singular
    real<lower=0> sigma;
    vector<lower=0>[J] od_init;
}

// transformed parameters { 
    // vector[J] theta_1 = theta + tau * theta_1_tilde;
// }

model { 
    vector[N] mu = theta_1[idx] .* elapsed_time + od_init[idx];

    // Priors
    theta ~ normal(0, 0.5);
    tau ~ normal(0, 0.1);
    // theta_1_tilde ~ std_normal();
    theta_1 ~ normal(theta, tau);
    sigma ~ normal(0, 10); 
    od_init ~ normal(0, 0.1);

    // Likelihood
    log_optical_density ~ normal(mu, sigma);

}