#%%
import numpy as np 
import pandas as pd 
import cmdstanpy
import altair as alt
import bebi103
import arviz 

# Load the collated data
data = pd.read_csv('../../data/collated/collated_OD600_growth_curves_exponential_phase.csv')

# Average across the replicates
data = data.groupby(['growth_medium', 'date', 'run_number', 
                     'strain', 'elapsed_time_hr']).mean().reset_index()


alt.Chart(data).mark_point().encode(x='elapsed_time_hr:Q',y=alt.Y('od_600nm:Q', scale=alt.Scale(type='log')), color='strain:N', shape='growth_medium')
#%%
# Compile the model
model = cmdstanpy.CmdStanModel(stan_file='../stan/hierarchical_growth_rate.stan')

# %%
# Iterate through each strain and growth medium to perform the inference.
sample_dfs = []
count = 0
for g, d in data.groupby(['growth_medium', 'strain']):
    # Assign identifiers
    d['biol_rep'] = d.groupby(['date', 'run_number']).ngroup() + 1

    # Assemble the data dictionary. 
    data_dict = {'J':d['biol_rep'].max(),
                 'N':len(d),
                 'idx': d['biol_rep'].values,
                 'elapsed_time':d['elapsed_time_hr'].values.astype(float),
                 'optical_density':d['od_600nm'].values.astype(float)}  
    samples = model.sample(data_dict, adapt_delta=0.9)
    samples = arviz.from_cmdstanpy(samples)
    print("""Assessing Diagnostics for {g}""")
    bebi103.stan.check_all_diagnostics(samples)
    count +=1
    if count == 2:
        break
    # samples = samples.posterior.to_dataframe().reset_index()
    # samples['growth_medium'] = g[0]
    # samples['strain'] = g[1]
    # sample_dfs.append(samples)

# samples = pd.concat(sample_dfs, sort=False)    
# %%
import bokeh.io
bokeh.io.show(bebi103.viz.parcoord(samples))
# %%
bokeh.io.show(
    bebi103.viz.corner(samples, parameters=['sigma', 'theta', 'tau'])
)
# %%
