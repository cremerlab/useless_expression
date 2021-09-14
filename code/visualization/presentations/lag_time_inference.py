#%% 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import futileprot.viz
colors, _ = futileprot.viz.matplotlib_style()

# Load the labled region data
data = pd.read_csv('../../../data/collated/collated_diauxic_shifts_labeled.csv')
data.head()
# %%
# Choose an example for the WT
wt = data[(data['date'] == '2021-09-09') & (data['replicate']==1) & (data['strain']=='WT')]
wt = wt[wt['od_600nm_subtracted'] >= 0.015]
wt['elapsed_time_hr'] -= wt['elapsed_time_hr'].min()

# %%
fig, ax = plt.subplots(1, 1, figsize=(4, 4))
ax.set_xlabel('elasped time [hr]')
ax.set_ylabel('log optical density')
ax.set_xlim([0.5, 7.5])
ax.set_ylim([-4, -1.5])
ax.plot(wt['elapsed_time_hr'], np.log(wt['od_600nm_subtracted'].values), '-k.')
plt.savefig('../../../figures/presentations/lagtime_nolabel.pdf', bbox_inches='tight')
gluc = wt[wt['phase']=='exponential_glucose']
acet = wt[wt['phase']=='exponential_acetate']
shift = wt[wt['phase']=='shift']
ax.plot(gluc['elapsed_time_hr'], np.log(gluc['od_600nm_subtracted']), '-', 
        color=colors['primary_blue'], marker='o', ms=3, label='growth on glucose')
ax.plot(acet['elapsed_time_hr'], np.log(acet['od_600nm_subtracted']), '-', 
        color=colors['primary_black'], marker='o', ms=3, label='growth on acetate')
ax.plot(shift['elapsed_time_hr'], np.log(shift['od_600nm_subtracted']), '-', 
        color=colors['primary_green'], marker='o', ms=3, label='lag phase')
ax.legend()
plt.savefig('../../../figures/presentations/lagtime_labled.pdf', bbox_inches='tight')
# ax.set_yscale('log')
# %%
fig, ax = plt.subplots(1, 1, figsize=(4,1))
ax.set_xlim([0, 7.5])

ROLLING_WINDOW = 8
NUDGE = 2
PEARSON_THRESH = 0.975

# Using the data, do a rolling correlation coefficient.
wt['log_od'] = np.log(wt['od_600nm_subtracted'])
out = wt[['elapsed_time_hr', 
            'log_od']].rolling(ROLLING_WINDOW).corr().reset_index()
out = out[out['level_1']=='elapsed_time_hr']['log_od']
out = out[ROLLING_WINDOW:]
ax.set_ylabel('pearson correlation')
ax.set_xlabel('elapsed time [hr]')
locs = out >= PEARSON_THRESH
locs = locs.astype(int)
sign_loc = np.sign(locs).diff()
min_ind = np.argmin(sign_loc) + ROLLING_WINDOW 
max_ind = np.argmax(sign_loc) + ROLLING_WINDOW 
ax.plot(wt['elapsed_time_hr'].values[ROLLING_WINDOW:], out, '.', color=colors['primary_black'])
plt.savefig('../../../figures/presentations/pearson_correlation_lagtime_nolabels.pdf', bbox_inches='tight')
ax.plot(wt['elapsed_time_hr'].values[ROLLING_WINDOW:min_ind], out[:min_ind - ROLLING_WINDOW], '.', color=colors['primary_blue'])
ax.plot(wt['elapsed_time_hr'].values[min_ind:max_ind], out[min_ind- ROLLING_WINDOW :max_ind - ROLLING_WINDOW], '.', color=colors['primary_green'])
ax.plot(wt['elapsed_time_hr'].values[max_ind:], out[max_ind - ROLLING_WINDOW:], '.', color=colors['primary_black'])
ax.hlines(PEARSON_THRESH, 0, 7.5, 'k', color=colors['primary_red'], zorder=1000)
plt.savefig('../../../figures/presentations/pearson_correlation_lagtime.pdf', bbox_inches='tight')
# %%
