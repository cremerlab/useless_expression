#%%
import numpy as np 
import pandas as pd 
import tqdm
import cmdstanpy
import arviz 
import bebi103.stan

# Load the collated data 
data = pd.read_csv('../../data/collated/collated_diauxic_shifts_labeled.csv')


# %%
# Load the inferential model
model = cmdstanpy.CmdStanModel(stan_file='../stan/two_layer_hierarchical_diauxie.stan')

# %%
dfs = []
for g, d in tqdm.tqdm(data.groupby(['strain', 'growth_medium'])):

    # Get the shift parameters
    shift_od = d[d['phase']=='shift'].groupby(
                ['date', 'run_number', 'replicate'])['od_600nm_subtracted'].median().values

    # Generate the ID vecs
    d['biol_rep'] = d.groupby(['date', 'run_number']).ngroup() + 1
    d['tech_rep'] = d.groupby(['date', 'run_number', 'replicate']).ngroup() + 1
    biol_idx = d.groupby(['tech_rep']).mean()['biol_rep'].values.astype(int)

    # Separate by the different phases
    m1, m2 = g[-1].split('-')
    m1_exp = d[d['phase']==f'exponential_{m1}']
    m2_exp = d[d['phase']==f'exponential_{m2}']

    # Generate the data dictionary
    data_dict = {'J':d['biol_rep'].max(),
                 'K':d['tech_rep'].max(),
                 'N_preshift': len(m1_exp),
                 'N_postshift': len(m2_exp),
                 'biol_idx':biol_idx,
                 'tech_idx_preshift':m1_exp['tech_rep'].values.astype(int),
                 'tech_idx_postshift':m2_exp['tech_rep'].values.astype(int),
                 'elapsed_time_preshift':m1_exp['elapsed_time_hr'].values.astype(float),
                 'elapsed_time_postshift':m2_exp['elapsed_time_hr'].values.astype(float),
                 'optical_density_preshift':m1_exp['od_600nm_subtracted'].values.astype(float),
                 'optical_density_postshift':m2_exp['od_600nm_subtracted'].values.astype(float),
                 'shift_optical_density':shift_od}
    samples = model.sample(data=data_dict)#, iter_warmup=1000, iter_sampling=5000, adapt_delta=0.99)

    samples = arviz.from_cmdstanpy(samples)
    bebi103.stan.check_all_diagnostics(samples)
    df = samples.posterior[['mu_preshift', 'mu_postshift', 
                            'theta_preshift', 'theta_postshift',
                            'delta']].to_dataframe().reset_index()
    df['strain'] = g[0]
    df['growth_medium'] = g[1]
    dfs.append(df)


#%%
## Save the lag times
samples = pd.concat(dfs, sort=False)
samples.to_csv('../../data/mcmc/lag_time_inference_hyperparameter_samples.csv',
                index=False)



# %%
