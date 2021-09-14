#%%

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import futileprot.viz
import seaborn as sns
colors, palette = futileprot.viz.matplotlib_style()

# WT = TRUE


data = pd.read_csv('../../../data/collated/collated_diauxic_shifts_labeled.csv')
data = data[(data['od_600nm_subtracted'] >= 0.01) & (data['od_600nm_subtracted'] <= 0.15)]
data['strain'] = [s.replace('∆', 'Δ') for s in data['strain'].values]
# %%

aligned = []
for g, d in data.groupby(['strain']):
    for _g, _d in d.groupby(['date', 'run_number', 'replicate']):
        shift_init = _d[_d['phase']=='shift']['elapsed_time_hr'].min()
        shift_od = np.log(_d[_d['phase']=='shift']['od_600nm_subtracted'].median())
        _d['shifted_time'] = np.round(_d['elapsed_time_hr'].values - shift_init, decimals=2)
        _d['shifted_od'] = np.log(_d['od_600nm_subtracted'].values) - shift_od
        aligned.append(_d)
aligned = pd.concat(aligned, sort=False)
aligned = aligned[(aligned['shifted_time'] <=3) & (aligned['shifted_time'] >=-1.5)]
aligned['shifted_od'] += 1

# %%
fig, ax = plt.subplots(1, 1, figsize=(4, 4))
ax.set_xlabel('time from diauxic shift [hr]')
ax.set_ylabel('log optical density relative to shift')
palette = sns.color_palette('husl', n_colors=11)
counter = 0
for g, d in aligned.groupby(['strain']):
    if g == 'WT':
        zorder = 1000
        markerfacecolor='white'
        markeredgecolor=colors['primary_black']
        linecolor=colors['primary_black']
    else:
        zorder = 1
        markerfacecolor = palette[counter] 
        markeredgecolor='white'
        linecolor=markerfacecolor
    d = d.groupby(['shifted_time']).mean().reset_index()
    ax.plot(d['shifted_time'], d['shifted_od'], '-', marker='o', label=g,
            markeredgecolor=markeredgecolor, markerfacecolor=markerfacecolor, ms=3,
            zorder=zorder,
            color=linecolor)
    counter += 1

ax.legend()

ax.vlines(0, -1, 2, color='k', linestyle='--')
ax.set_ylim([0, 1.5])
plt.savefig('../../../figures/presentations/aligned_diauxic_shifts.pdf', index=False)
# %%


# %%
aligned.head()
# %%
