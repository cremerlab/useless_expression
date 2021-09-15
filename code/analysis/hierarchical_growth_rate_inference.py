#%%
import numpy as np 
import pandas as pd 
import cmdstanpy
import futileprot.bayes
import futileprot.io
import tqdm
import bebi103
import arviz 

# Load the collated data
data = pd.read_csv('../../data/collated/collated_OD600_growth_curves_exponential_phase.csv')

# Average across the replicates
data = data.groupby(['growth_medium', 'date', 'run_number', 
                     'strain', 'identifier', 'elapsed_time_hr']).mean().reset_index()
_, _, classes = futileprot.io.standardize_strains(data['identifier'].values)
data['class'] = classes
#%%

# Compile the model
# model = cmdstanpy.CmdStanModel(stan_file='../stan/one_layer_hierarchical_growth_rate.stan')
model = cmdstanpy.CmdStanModel(stan_file='../stan/two_layer_hierarchical_growth_rate.stan')

# %%
# Iterate through each strain and growth medium to perform the inference.
sample_dfs = []
mu_sample_dfs = []
for g, d in tqdm.tqdm(data.groupby(['growth_medium', 'strain', 'class']), 
                    desc='performing inference'):
    d['elapsed_time_hr'] -= d['elapsed_time_hr'].min()

    # Assign identifiers
    d['biol_rep'] = d.groupby(['date', 'run_number']).ngroup() + 1
    d['tech_rep'] = d.groupby(['date', 'run_number', 'replicate']).ngroup() + 1
    biol_idx = d.groupby(['tech_rep']).mean()['biol_rep'].values.astype(int)

    # Assemble the data dictionary. 
    data_dict = {'J':d['biol_rep'].max(),
                 'K': d['tech_rep'].max(),
                 'N':len(d),
                 'biol_idx':biol_idx,
                 'tech_idx': d['tech_rep'].values.astype(int),
                 'elapsed_time':d['elapsed_time_hr'].values.astype(float),
                 'optical_density':d['od_600nm_subtracted'].values.astype(float)} 
    samples = model.sample(data=data_dict, iter_warmup=1000, adapt_delta=0.99)
    samples = arviz.from_cmdstanpy(samples)
    bebi103.stan.check_all_diagnostics(samples) 
    samples = samples.posterior['mu'].to_dataframe().reset_index()
    samples['growth_medium'] = g[0]
    samples['strain'] = g[1]
    samples['class'] = g[-1]
    sample_dfs.append(samples)

#%%
samples = pd.concat(sample_dfs, sort=False)    
samples.to_csv('../../data/mcmc/growth_rate_inference_hyperparameter_samples.csv',
                index=False)
# %%
# #  Save just the growth rate parameters
# mu_dfs = []
# for g, d in tqdm.tqdm(samples.groupby(['growth_medium', 'strain', 'class']), 
#                      desc='Saving hyperparameter samples'):
#     melted = d.melt(['draw', 'chain'])
#     melted.drop_duplicates(subset=['draw', 'chain', 'variable', 'value'], 
#                            inplace=True)
#     mu_df = pd.DataFrame(melted[melted['variable']=='mu']['value'].values.T, 
#                          columns=['mu'])
#     mu_df['growth_medium'] = g[0]
#     mu_df['strain'] = g[1]
#     mu_df['class'] = g[-1]
#     mu_dfs.append(mu_df)

# #%%
# mu_df = pd.concat(mu_dfs, sort=False)

# #%%
# mu_df.to_csv('../../data/mcmc/growth_rate_inference_hyperparameter_samples.csv')

# #%%
# Summarize the parameters for the various percentiles. 
summary_df = pd.DataFrame([])
for g, d in tqdm.tqdm(samples.groupby(['growth_medium', 'strain']),
                    desc='Saving growth rate summaries'):
    
    # Parse the hyper parameters  
    # melted = d.melt('draw')
    # mu = melted[melted['variable']=='mu']['value'].values
    percs = futileprot.bayes.compute_percentiles(d['mu'].values) 
    for k, v in percs.items():
        summary_df = summary_df.append({'low':v[0], 
                                        'high':v[1], 
                                        'percentile':k, 
                                        'growth_medium':g[0],
                                        'strain':g[1],
                                        'replicate':'hyperparameter'},
                                        ignore_index=True)
    # # Parse the low-level parameters 
    # for _g, _d in d.groupby(['mu_1_dim_0']):
    #     melted = _d.melt('draw')
    #     mu = melted[melted['variable']=='mu_1']['value'].values
    #     for k, v in percs.items():
    #         summary_df = summary_df.append({'low':v[0], 
    #                                     'high':v[1], 
    #                                     'percentile':k, 
    #                                     'growth_medium':g[0],
    #                                     'strain':g[1],
    #                                     'replicate':_g},
    #                                     ignore_index=True)
summary_df.to_csv('../../data/mcmc/growth_rate_inference_summaries.csv',
                    index=False) 


# %%
