#%%
import numpy as np 
import pandas as pd 
import altair as alt 
import futileprot.viz
import sklearn.neighbors
import tqdm
colors, palette = futileprot.viz.altair_style()
#%%

# Load the hyperparameter data
data = pd.read_csv('../../data/mcmc/growth_rate_inference_hyperparameter_samples.csv')

# %%
# For each collection of samples, compute the kernel density estimate over a wide range
mu_range = np.linspace(0.1, 1.5, 1000)
kde_dfs = []
for g, d in tqdm.tqdm(data.groupby(['strain', 'growth_medium'])):
    logprob = sklearn.neighbors.KernelDensity(
                                    kernel='gaussian'
                                    ).fit(
                                        d['mu'].values[:, None]
                                    ).score_samples(
                                        mu_range[:, None])
    _df = pd.DataFrame([])
    _df['growth_rate_hr'] = mu_range
    _df['kde'] = np.exp(logprob)
    _df['kde_norm'] = _df['kde'].values / _df['kde'].max()
    _df['strain'] = g[0]
    _df['growth_medium'] = g[1]
kde_df = pd.concat(kde_dfs, sort=False)
#    
# %%
