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
data.head()
#%%
data = data[(data['class']=='WT' ) | (data['class']=='Single KO')]
# %%
# For each collection of samples, compute the kernel density estimate over a wide range
mu_range = np.linspace(0.1, 1.5, 1000)
kde_dfs = []
for g, d in tqdm.tqdm(data.groupby(['strain', 'growth_medium'])):
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
    kde_dfs.append(_df)
kde_df = pd.concat(kde_dfs, sort=False)
#    

#%%
# Set up the ridgeline plot
N_DIST = len(kde_df['strain'].unique())
palette = sns.color_palette('mako', n_colors=N_DIST+1)

# Assign the indices
indices = {'WT':N_DIST}
counter = N_DIST
for g, d in kde_df[kde_df['strain']!='WT'].groupby(['strain']):
    counter -= 1
    indices[g] = counter

# Instantiate the figure
fig, ax = plt.subplots(1, 2, figsize=(6, 4), sharey=True)

# Add a label of what the height means
ax[0].arrow(0.42, 0.5 * N_DIST, 0, 0.8, color='grey', 
            width=0.001, head_length=0.05, head_width=0.01)
ax[0].text(0.4, 0.51 * N_DIST, '$\propto$ probability', fontsize=5, 
          rotation='vertical', fontstyle='italic')
# ax[0].text(0.5 * N_DIST, 0.05, 'growth in acetate', 
        #  color=colors['primary_black'], fontweight='bold')
# Add labels
ax[0].set_title('growth in acetate', loc='right', y=0.82)
ax[1].set_title('growth in glucose', loc='right', y=0.82)

# Adjust the axis limits
ax[0].set_xlim([0.4, 0.75])
ax[1].set_xlim([0.72, 1.35])

for a in ax:
    a.set_xlabel('growth rate [hr$^{-1}$]')
    a.set_facecolor('#FFFFFF') 

# Add ytick labels
_ = ax[0].set_yticks((np.arange(N_DIST) + 1) * 0.5)
ax[0].set_yticklabels(reversed(sorted(indices.keys())))
axes = {'acetate':ax[0], 'glucose':ax[1]}
for g, d in kde_df.groupby(['strain', 'growth_medium']):
    _ax = axes[g[1]]
    ind = indices[g[0]]

    if g[0] == 'WT':
        _color = 'grey'
    else:
        _color = palette[ind]
    _ax.plot(d['growth_rate_hr'], d['kde_norm'] + 0.5 * ind,
            zorder=np.abs(ind - N_DIST) +1, color=_color)
    _ax.fill_between(d['growth_rate_hr'], 0.5 * ind, d['kde_norm'] + 0.5 *ind, alpha=0.5,
        zorder=np.abs(ind - N_DIST) + 2, color=_color)
plt.savefig('../../figures/growth_rates/singleKO_hyperparameter_ridgeline.pdf', bbox_inches='tight')
# %%

# %%
