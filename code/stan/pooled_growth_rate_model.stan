data {
    int<lower=1> N; // Number of measurements
    vector<lower=0>[N] elapsed_time;
    vector<lower=0>[N] od;
}

transformed data {
    vector[N] log_od = log(od);
}

parameters {
    real<lower=0> mu; // Growth rate
    real<lower=0> od_init; // Initial OD
    real<lower=0> sigma; // Homoscedastic error    
}

transformed parameters { 
    real log_od_init = log(od_init);
}

model {
    mu ~ std_normal();
    od_init ~ std_normal();
    sigma ~ std_normal();

    log_od ~ normal(log_od_init + mu * elapsed_time, sigma);
}