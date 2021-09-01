"""
Note:
* This script drops points before 0.5 hr for the Stanford + micronutrients sample
"""
#%%
import numpy as np 
import pandas as pd 
import futileprot.io
import futileprot.viz
import altair as alt 
import altair_saver
colors, palette = futileprot.viz.altair_style()

# Define experiment parameters
DATE = '2021-08-31'
STRAINS = 'WT'
MEDIUM = 'acetate_water_comparison'
CARBON = 'acetate'
RUN_NO = 2
ROOT = '../../../..'
SKIPROWS = 36 
OD_BOUNDS = [0.03, 0.08]

# Add the well identifiers
WATER_MAP = {'UCSD + micronutrients': ['C3', 'D3', 'E3', 'F3'],
       'UCSD - micronutrients': ['C4', 'D4', 'E4', 'F4'],
       'Stanford + micronutrients': ['C5', 'D5', 'E5', 'F5']}

#%%
# Generate a list of all valid wells
wells = [f'{letter}{number}' for letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] for number in np.arange(1,13)]

# Load the data
data = pd.read_csv(f'{ROOT}/data/growth_rates/{DATE}_r{RUN_NO}_{STRAINS}_{MEDIUM}/{DATE}_r{RUN_NO}.csv', 
                skiprows=SKIPROWS)

# Melt and drop unnecessary stuff
melted = data.melt(id_vars=['Time'], var_name='well', value_name='od_600nm')
melted = melted.loc[melted['well'].isin(wells)]
melted.dropna(inplace=True)

# Add strain identifier and replicates
melted['strain'] = 'blank'
melted['water_source'] = 'blank'
for water, wells in WATER_MAP.items():
    for idx, well in enumerate(wells):
        melted.loc[melted['well']==well, 'strain'] = 'WT'
        melted.loc[melted['well']==well, 'water_source'] = water

melted['replicate'] = 0
for i in range(3, 11):
    for l in ['C', 'D', 'E', 'F']:
        ind = i - 2
        melted.loc[melted['well'] == f'{l}{i}', 'replicate'] = ind


#%%
# Add information regarding date and growth medium
melted['growth_medium'] = CARBON
melted['date'] = DATE
melted['run_number'] = RUN_NO

# Convert time to elapsed time
melted['time_sec'] = pd.to_timedelta(melted['Time'].values)
melted['time_sec'] = melted['time_sec'].dt.total_seconds()
melted['elapsed_time_hr'] = (melted['time_sec'] - melted['time_sec'].min())/3600
#%%
# Drop unnecessary Time columns
melted.drop(columns=['Time', 'time_sec'], inplace=True)


# Reformat blank value as average entry per time
measurement = []
for g, d in melted.groupby(['elapsed_time_hr']):
    d = d.copy()
    avg_blank = d[d['strain']=='blank']
    meas = d[d['strain']!='blank']
    meas['avg_blank_value'] = avg_blank['od_600nm'].mean()
    measurement.append(meas)
measurement = pd.concat(measurement, sort=False)

# Save to disk
measurement.to_csv(f'./output/{DATE}_r{RUN_NO}_{STRAINS}_{MEDIUM}_measurements.csv', index=False)

#%%
# Perform the blank subtraction
measurement['od_600nm_subtracted'] = measurement['od_600nm'].values - measurement['avg_blank_value'].values

# Given truncation, recalculated elapsed time and save truncated data
trunc = []
for g, d in measurement.groupby(['water_source', 'replicate']):
    d = d.copy()
    d = d[(d['od_600nm_subtracted'] >= OD_BOUNDS[0]) & 
          (d['od_600nm_subtracted'] <= OD_BOUNDS[1])]
    d['elapsed_time_hr'] -= d['elapsed_time_hr'].min()
    trunc.append(d)
trunc = pd.concat(trunc, sort=False)
trunc = trunc[['strain', 'water_source', 'elapsed_time_hr', 
             'od_600nm_subtracted', 'growth_medium',  'replicate',
             'date', 'run_number']]
trunc.rename(columns={'od_600nm_subtracted':'od_600nm',
                      'replicate':'technical_replicate'}, inplace=True)

dfs = []
for g, d in trunc.groupby(['water_source']):
    if g == 'Stanford + micronutrients':
        dfs.append(d[d['elapsed_time_hr'] > 0.5])
    else:
        dfs.append(d)
trunc = pd.concat(dfs, sort=False)


trunc.to_csv(f'./output/{DATE}_r{RUN_NO}_{STRAINS}_{MEDIUM}_exponential_phase.csv', index=False)

# %%
# Generate a figure of all of the raw traces
raw_traces = alt.Chart(
                    data=measurement, 
                    width=400, 
                    height=200
                ).mark_line(
                    point=True,
                    opacity=0.75
                ).encode(
                    x=alt.X('elapsed_time_hr:Q', title='elapsed time [hr]'),
                    y=alt.Y('od_600nm:Q', title='optical density [a.u.]'), 
                    color=alt.Color('replicate:N', title='technical replicate'),
                ).facet(
                    row='water_source:N',
                    column='micronutrients:N'
                )
altair_saver.save(raw_traces, f'output/{DATE}_r{RUN_NO}_{STRAINS}_{MEDIUM}_raw_traces.png',
                 scale_factor=2)


# %%
