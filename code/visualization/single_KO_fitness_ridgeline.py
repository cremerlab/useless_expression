#%%
import numpy as np 
import pandas as pd 
import futileprot.viz
import sklearn.neighbors
import seaborn as sns
import tqdm
import matplotlib.pyplot as plt
colors, _  = futileprot.viz.matplotlib_style()

#%%
# Load the hyperparameter data
data = pd.read_csv('../../data/mcmc/growth_rate_inference_hyperparameter_samples.csv')

# Separate the wt and the singles
wt_data = data[data['strain']=='WT']
singles = data[data['class']=='Single KO']

# Perform the random sampling to compute the fitness for the sinlge KOs
fit_range = np.linspace(0.5, 1.5, 1000)
fit_dfs = []
fit_kde_dfs = []
N_DRAWS = int(1E4)
for g, d in singles.groupby(['growth_medium', 'strain']):

    # Perform the sampling
    wt = wt_data[wt_data['growth_medium']==g[0]]
    wt_draws = np.random.choice(wt['mu'].values, size=N_DRAWS, replace=True)
    ko_draws = np.random.choice(d['mu'].values, size=N_DRAWS, replace=True)
    fitness = ko_draws / wt_draws

    # Assemble the dataframe 
    _df = pd.DataFrame([])
    _df['fitness'] = fitness
    _df['wt_draws'] = wt_draws
    _df['ko_draws'] = ko_draws
    _df['strain'] = g[1]
    _df['growth_medium'] = g[0]
    fit_dfs.append(_df)

    # Compute the KDE
    logprob = sklearn.neighbors.KernelDensity(
                                     kernel='gaussian',
                                     bandwidth=0.01,
                                     ).fit(
                                         fitness[:, None]
                                     ).score_samples(
                                         fit_range[:, None])
    _df = pd.DataFrame([])
    _df['fitness'] = fit_range
    _df['kde'] = np.exp(logprob)
    _df['strain'] = g[1]
    _df['growth_medium'] = g[0]
    fit_kde_dfs.append(_df)


fit_df = pd.concat(fit_dfs, sort=False)
fit_kde_df = pd.concat(fit_kde_dfs, sort=False)
fit_kde_df['kde_norm'] = fit_kde_df['kde'].values / fit_kde_df['kde'].max()
   
# Perform the random sampling to coompute the resolution on fitness.
err_dfs = []
err_kde_dfs = []
for g, d in wt_data.groupby(['growth_medium']):
    wt_draws_1 = np.random.choice(d['mu'].values, size=N_DRAWS, replace=True)
    wt_draws_2 = np.random.choice(d['mu'].values, size=N_DRAWS, replace=True)
    fitness = wt_draws_1 / wt_draws_2

    # Assemble the err df
    _df = pd.DataFrame([])
    _df['fitness'] = fitness
    _df['growth_medium'] = g
    _df['wt_draws_1'] = wt_draws_1
    _df['wt_draws_2'] = wt_draws_2
    err_dfs.append(_df)

    # Compute the KDE
    logprob = sklearn.neighbors.KernelDensity(
                                     kernel='gaussian',
                                     bandwidth=0.01,
                                     ).fit(
                                         fitness[:, None]
                                     ).score_samples(
                                         fit_range[:, None])
    _df = pd.DataFrame([])
    _df['fitness'] = fit_range
    _df['kde'] = np.exp(logprob) 
    _df['growth_medium'] = g
    err_kde_dfs.append(_df)

err_df = pd.concat(err_dfs, sort=False)
err_kde_df = pd.concat(err_kde_dfs, sort=False)
err_kde_df['kde_norm'] = err_kde_df['kde'].values / err_kde_df['kde'].max()
 
# %%


# Set up the ridgeline plot
N_DIST = len(fit_kde_df['strain'].unique())
palette = sns.color_palette('mako', n_colors=N_DIST+1)

# Assign the indices
indices = {}
counter = N_DIST
OVERLAP = 1 
for g, d in fit_kde_df.groupby(['strain']):
    counter -= 1
    indices[g] = counter

# Instantiate the figure
fig, ax = plt.subplots(1, 3, figsize=(6, 6), sharey=True)

# Add a label of what the dashed distribution means
ax[0].text(0.7, (N_DIST - 1) * OVERLAP + 0.18, '          error\ndistribution', fontsize=5)

# Add labels
ax[0].set_title('30 mM acetate', loc='left', y=0.97)
ax[1].set_title('0.6 mM glucose + 30 mM acetate', loc='left', y=0.97)
ax[2].set_title('10 mM glucose', loc='left', y=0.97)

# Adjust the axis limits
for a in ax:
    a.set_xlim([0.5, 1.5])

for a in ax:
    a.set_xlabel('fitness')
    a.set_facecolor('#FFFFFF') 

# Add ytick labels
_ = ax[0].set_yticks((np.arange(N_DIST)) * OVERLAP)

ax[0].set_yticklabels(reversed(sorted(indices.keys())))
axes = {'acetate':ax[0], 'ga_preshift': ax[1], 'glucose':ax[2]}
for g, d in fit_kde_df.groupby(['strain', 'growth_medium']):
    _ax = axes[g[1]]
    ind = indices[g[0]]

    _color = palette[ind]
    
    _ax.plot(d['fitness'], d['kde_norm'] + OVERLAP *ind,
            zorder=np.abs(ind - N_DIST) +1, color=_color)
    _ax.plot(d['fitness'],  OVERLAP * ind * np.ones(len(d)),
            zorder=np.abs(ind - N_DIST) +1, color=_color)
    _ax.fill_between(d['fitness'], OVERLAP * ind, d['kde_norm'] + OVERLAP *ind, 
            alpha=0.5,  zorder=np.abs(ind - N_DIST) + 2, color=_color)


# Plot the error distributions
for g, d in err_kde_df.groupby(['growth_medium']):
    _ax = axes[g]
    _color = 'grey'
    for i in indices.values():
        if i < (N_DIST ):
            _ax.plot(d['fitness'], d['kde_norm'] + OVERLAP * i,
            '--', zorder=np.abs(i - N_DIST) +1, color=_color) 
plt.tight_layout()
plt.savefig('../../figures/SingleKO_fitness_ridgeline.pdf')
# %%
