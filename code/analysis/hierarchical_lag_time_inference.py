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
    # Ignore the preshift phase 
    d = d[~d['phase'].str.contains(f"{g[1].split('-')[0]}")]

    # Get the shift parameters
    shift_od = d[d['phase']=='shift'].groupby(
                ['date', 'run_number', 'replicate'])['od_600nm_subtracted'].median().values
    shift_init = d[d['phase']=='shift'].groupby(
                                ['date', 'run_number', 'replicate']
                                )['elapsed_time_hr'].min().values
    
    # Restrict to only the exponential phase
    d = d[d['phase']==f"exponential_{g[1].split('-')[-1]}"]

    # Generate the ID vecs
    d['biol_rep'] = d.groupby(['date', 'run_number']).ngroup() + 1
    d['tech_rep'] = d.groupby(['date', 'run_number', 'replicate']).ngroup() + 1
    biol_idx = d.groupby(['tech_rep']).mean()['biol_rep'].values.astype(int)

    # Generat the data dictionary
    data_dict = {'J':d['biol_rep'].max(),
                 'K':d['tech_rep'].max(),
                 'N': len(d),
                 'biol_idx':biol_idx,
                 'tech_idx':d['tech_rep'].values.astype(int),
                 'elapsed_time':d['elapsed_time_hr'].values.astype(float),
                 'optical_density':d['od_600nm_subtracted'].values.astype(float),
                 'shift_optical_density':shift_od,
                 't_init': shift_init}
    samples = model.sample(data=data_dict, iter_warmup=1000, adapt_delta=0.99, 
                            iter_sampling=5000)
    samples = arviz.from_cmdstanpy(samples)
    bebi103.stan.check_all_diagnostics(samples)
    df = samples.posterior[['mu', 'theta', 'delta']].to_dataframe().reset_index()
    df['strain'] = g[0]
    df['growth_medium'] = g[1]
    dfs.append(df)

#%%
## Save the lag times
samples = pd.concat(dfs, sort=False)
samples.to_csv('../../data/mcmc/lag_time_inference_hyperparameter_samples.csv',
                index=False)



# %%
