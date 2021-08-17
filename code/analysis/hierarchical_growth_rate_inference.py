#%%
import numpy as np 
import pandas as pd 
import cmdstanpy
import futileprot.bayes
import tqdm
import bebi103
import arviz 

# Load the collated data
data = pd.read_csv('../../data/collated/collated_OD600_growth_curves_exponential_phase.csv')

# Average across the replicates
data = data.groupby(['growth_medium', 'date', 'run_number', 
                     'strain', 'elapsed_time_hr']).mean().reset_index()

#%%

# Compile the model
model = cmdstanpy.CmdStanModel(stan_file='../stan/hierarchical_growth_rate.stan')


#%%

# Assign the various identifiers
data['unique_idx'] = data.groupby(['strain', 'growth_medium']).ngroup() + 1 
data['replicate_idx'] = data.groupby(['strain', 'growth_medium', 
                                      'date', 'run_number']).ngroup() + 1
unique_idx = data.groupby(['strain', 'growth_medium', 
                            'date', 'run_number']
                        ).mean().reset_index()['unique_idx'].values.astype(int)
replicate_idx = data['replicate_idx'].values.astype(int)
#%%
# Set up the data dictionary
data_dict = {'J':data['unique_idx'].max(),
             'K': data['replicate_idx'].max(),
             'N': len(data),
             'unique_idx': unique_idx,
             'replicate_idx': replicate_idx,
             'elapsed_time': data['elapsed_time_hr'].values.astype(float),
             'optical_density': data['od_600nm'].values.astype(float)}

# Sample the model all at once
samples = model.sample(data=data_dict, adapt_delta=0.99) 
                    #, iter_warmup=500, 
                    #    threads_per_chain=48, chains=10, parallel_chains=10,
                    #    adapt_delta=0.9)

#%%
samples = arviz.from_cmdstanpy(samples)
bebi103.stan.check_all_diagnostics(samples) 


# %%
# Iterate through each strain and growth medium to perform the inference.
sample_dfs = []
for g, d in tqdm.tqdm(data.groupby(['growth_medium', 'strain']), desc='performing inference'):

    # Assign identifiers
    d['biol_rep'] = d.groupby(['date', 'run_number']).ngroup() + 1

    # Assemble the data dictionary. 
    data_dict = {'J':d['biol_rep'].max(),
                 'N':len(d),
                 'idx': d['biol_rep'].values,
                 'elapsed_time':d['elapsed_time_hr'].values.astype(float),
                 'optical_density':d['od_600nm'].values.astype(float)}  
    samples = model.sample(data_dict, adapt_delta=0.999)
    samples = arviz.from_cmdstanpy(samples)
    bebi103.stan.check_all_diagnostics(samples) 
    samples = samples.posterior.to_dataframe().reset_index()
    samples['growth_medium'] = g[0]
    samples['strain'] = g[1]
    sample_dfs.append(samples)
#%%
samples = pd.concat(sample_dfs, sort=False)    
# #%%
# samples.to_csv('../../data/mcmc/growth_rate_inference_samples_total.csv', index=False)
# %%
#  Save just the growth rate parameters
mu_dfs = []
for g, d in tqdm.tqdm(samples.groupby(['growth_medium', 'strain']), 
                     desc='Saving hyperparameter samples'):
    melted = d.melt('draw')
    mu_df = pd.DataFrame(melted[melted['variable']=='mu']['value'].values.T, 
                         columns=['mu'])
    mu_df['growth_medium'] = g[0]
    mu_df['strain'] = g[1]
    mu_dfs.append(mu_df)

#%%
mu_df = pd.concat(mu_dfs, sort=False)
mu_df.to_csv('../../data/mcmc/growth_rate_inference_hyperparameter_samples.csv')

#%%
# Summarize the parameters for the various percentiles. 
summary_df = pd.DataFrame([])
for g, d in tqdm.tqdm(samples.groupby(['growth_medium', 'strain']),
                    desc='Saving growth rate summaries'):
    
    # Parse the hyper parameters  
    melted = d.melt('draw')
    mu = melted[melted['variable']=='mu']['value'].values
    percs = futileprot.bayes.compute_percentiles(mu) 
    for k, v in percs.items():
        summary_df = summary_df.append({'low':v[0], 
                                        'high':v[1], 
                                        'percentile':k, 
                                        'growth_medium':g[0],
                                        'strain':g[1],
                                        'replicate':'hyperparameter'},
                                        ignore_index=True)
    # Parse the low-level parameters 
    for _g, _d in d.groupby(['mu_1_dim_0']):
        melted = _d.melt('draw')
        mu = melted[melted['variable']=='mu_1']['value'].values
        for k, v in percs.items():
            summary_df = summary_df.append({'low':v[0], 
                                        'high':v[1], 
                                        'percentile':k, 
                                        'growth_medium':g[0],
                                        'strain':g[1],
                                        'replicate':_g},
                                        ignore_index=True)
summary_df.to_csv('../../data/mcmc/growth_rate_inference_summaries.csv',
                    index=False) 
# %%
