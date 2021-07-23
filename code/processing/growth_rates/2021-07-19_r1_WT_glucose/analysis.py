#%%
import numpy as np 
import pandas as pd 
import altair as alt 
from altair_saver import save as alt_save
import scipy.stats
import futileprot as fp
import glob
colors, palette = fp.viz.altair_style()

DATE = '2021-07-19'
STRAIN = 'WT'
MEDIUM = 'glucose'

# %%
# Get the measurement file
data = pd.read_csv(f'./output/{DATE}_{STRAIN}_{MEDIUM}_measurements.csv')

# Compute the background subtraction
data['od_600nm_sub'] = data['od_600nm'].values - data['avg_blank_value'].values
data = data[data['od_600nm_sub'] > 0]

# %%

# Plot all of the traces and the "average" trace among replicates
base = alt.Chart(data=data,
                    width=300, 
                    height=300
                    ).encode(
                        x=alt.X('elapsed_time_hr:Q', title='elapsed time [hr]'),
                        y=alt.Y('od_600nm_sub:Q', title='optical density [a.u.]',
                            scale=alt.Scale(type='log')))


traces = base.mark_line(color=colors['black'], opacity=0.5, size=0.5).encode(
            detail='replicate'
)
avg = base.mark_line(color=colors['primary_blue'], size=5).encode(
            y='mean(od_600nm_sub):Q',
)
alt_save(traces + avg, f'output/{DATE}_{STRAIN}_{MEDIUM}_raw_traces.png')
# %%
# Considering only the averages, restrict to the range of 0.01 to 0.1 and 
# compute the growth rate
avg_data = data.groupby('elapsed_time_hr').mean().reset_index()
avg_data = avg_data[(avg_data['od_600nm_sub'] >= 0.01) & (avg_data['od_600nm_sub'] <= 0.1)]
avg_data['elapsed_time_hr'] -= avg_data['elapsed_time_hr'].min()

# Do the regression
popt  = scipy.stats.linregress(avg_data['elapsed_time_hr'].values, 
                               np.log(avg_data['od_600nm_sub'].values))

# comptue and plot the fit. 
time_range = np.linspace(0, 2.2, 20)
_fit = np.exp(popt[1] + popt[0] * time_range)
fit_df = pd.DataFrame([])
fit_df['elapsed_time_hr'] = time_range
fit_df['od_600nm_sub'] = _fit

data_plot = alt.Chart(avg_data).mark_point( 
                ).encode(
                    x=alt.X('elapsed_time_hr:Q', title='elapsed time [hr]'), 
                    y=alt.Y('od_600nm_sub:Q', 
                            scale=alt.Scale(type='log')))

fit_plot = alt.Chart(fit_df, title=f'NCM3722 in glucose; μ = {popt[0]:0.2f} ± {popt[-1]:0.2f} per hr').mark_line().encode(
                x=alt.X('elapsed_time_hr:Q', title='elapsed time [hr]'),
                y=alt.Y('od_600nm_sub:Q', title='optical density [a.u.]')

)

layout = data_plot + fit_plot
layout.properties(title=f'NCM3722 in glucose; μ = {popt[0]:0.2f} ± {popt[-1]:0.2f} per hr')
alt_save(layout, f'output/{DATE}_{STRAIN}_{MEDIUM}_fit.png')


