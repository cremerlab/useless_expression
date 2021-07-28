#%%
import numpy as np 
import pandas as pd 
import cmdstanpy
import bebi103
import arviz 

# Load the collated data
data = pd.read_csv('../../data/collated/collated_OD600_growth_curves_exponential_phase.csv')

#%%
# Compile the model
model = cmdstanpy.CmdStanModel(stan_file='../stan/hierarchical_growth_rate.stan')

# %%
# Iterate through each strain and growth medium to perform the inference.
for g, d in data.groupby(['growth_medium', 'strain']):
    # Assign identifiers
    d['biol_rep'] = d.groupby(['date', 'run_number']).ngroup() + 1
    d['tech_rep'] = d.groupby(['date', 'run_number', 'technical_replicate']).ngroup() + 1

    _d = d.groupby(['date', 'run_number', 'technical_replicate']).mean().reset_index()

    # Assemble the data dictionary. 
    data_dict = {'J':d['biol_rep'].max(),
                 'K':d['tech_rep'].max(),
                 'N':len(d),
                 'J_idx':_d['biol_rep'].values,
                 'K_idx':d['tech_rep'].values.astype(int),
                 'elapsed_time':d['elapsed_time_hr'].values.astype(float),
                 'optical_density':d['od_600nm'].values.astype(float)}
    # Perform the sampling
# %%
samples = model.sample(data_dict, iter_sampling=5000, adapt_delta=0.9)
samples = arviz.from_cmdstanpy(samples)
bebi103.stan.check_all_diagnostics(samples)
# %%
