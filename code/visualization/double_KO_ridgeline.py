#%%
import numpy as np 
import pandas as pd 
import futileprot.viz
import sklearn.neighbors
import seaborn as sns
import tqdm
import matplotlib.pyplot as plt
colors,_  = futileprot.viz.matplotlib_style()

#%%
# Load the hyperparameter data
data = pd.read_csv('../../data/mcmc/growth_rate_inference_hyperparameter_samples.csv')
data['strain'] = [s.replace('∆', 'Δ') for s in data['strain'].values]

# %%
# For each collection of samples, compute the kernel density estimate over a wide range
mu_range = np.linspace(0.1, 1.5, 1000)
kde_dfs = []
for g, d in tqdm.tqdm(data.groupby(['strain', 'growth_medium', 'class'])):
    logprob = sklearn.neighbors.KernelDensity(
                                     kernel='gaussian',
                                     bandwidth=0.01,
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
    _df['class'] = g[2]
    kde_dfs.append(_df)
kde_df = pd.concat(kde_dfs, sort=False)
#    

#%%

# Set up the ridgeline plot
N_DIST = len(kde_df[kde_df['class'] == 'Double KO']['strain'].unique())
palette = sns.color_palette('mako', n_colors=N_DIST+1)

# Assign the indices
ax_ind = {}
indices = {}
counter = np.round(N_DIST / 2)
labels = {0:[], 1:[]} 
ax_counter = 0
switch = False
for g, d in kde_df[kde_df['class']=='Double KO'].groupby(['strain']):
    if ax_counter <= 22:
        ax_ind[g] = 0
    else:
        ax_ind[g] = 1
    if counter > 0:
        counter -= 1
    else:
        counter = int(np.round(N_DIST / 2))
    ax_counter += 1
    indices[g] = counter
    labels[ax_ind[g]].append(g)


# Instantiate the figure
fig, ax = plt.subplots(1, 2, figsize=(8, 6))

# Adjust the axis limits
ax[0].set_xlim([0.1, 0.7])
ax[1].set_xlim([0.3, 0.7])

for a in ax:
    a.set_xlabel('growth rate [hr$^{-1}$]')
    a.set_facecolor('#FFFFFF') 

# Add ytick labels
_ = ax[0].set_yticks(np.arange(0, 23))
_ = ax[1].set_yticks(np.arange(0, 22))
ax[0].set_yticklabels(reversed(sorted(labels[0])))
ax[1].set_yticklabels(reversed(sorted(labels[1])))
for g, d in kde_df[kde_df['class']=='Double KO'].groupby(['strain', 'growth_medium']):
    _ax = ax[ax_ind[g[0]]]
    ind = int(indices[g[0]])
    if g[0] == 'WT':
        _color = 'grey'
    else:
        _color = palette[ind]

    # Plot the result from the double
    _ax.plot(d['growth_rate_hr'], d['kde_norm'] + ind,
            zorder=np.abs(ind - N_DIST) +0.8, color=_color)
    _ax.plot(d['growth_rate_hr'], ind * np.ones(len(d)),
            zorder=np.abs(ind - N_DIST) +0.8, color=_color)
    _ax.fill_between(d['growth_rate_hr'], ind, d['kde_norm'] + ind, alpha=0.5,
        zorder=np.abs(ind - N_DIST) + 2, color=_color)

    # Get the individuals
    singles = g[0].split(' ')
    ls = [':', '--']
    for i, s in enumerate(singles):
        _d = kde_df[(kde_df['strain']==s) & (kde_df['growth_medium']=='acetate')]
        _ax.plot(_d['growth_rate_hr'], _d['kde_norm'] + ind,
            zorder=np.abs(ind - N_DIST) +1, color='grey', linestyle=ls[i])


plt.savefig('../../figures/growth_rates/DoubleKO_hyperparameter_ridgeline.pdf', bbox_inches='tight',
            transparent=True)
# %%
