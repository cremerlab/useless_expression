#%%
import numpy as np 
import pandas as pd 
import futileprot.io
import futileprot.viz
import altair as alt 
import altair_saver
colors, palette = futileprot.viz.altair_style()

# Define experiment parameters
DATE = '2021-08-06'
STRAINS = 'WT'
MEDIUM = 'acetate_water_comparison'
CARBON = 'acetate'
RUN_NO = 1
ROOT = '../../../..'
SKIPROWS = 28
OD_BOUNDS = [0.03, 0.1]

# Add the well identifiers
WATER_MAP = {'CCSR': ['C3', 'C4', 'C5', 'C6', 'D3', 'D4', 'D5', 'D6'],
       'MQ+': ['E3', 'E4', 'E5', 'E6', 'F3', 'F4', 'F5', 'F6'],
       'MQ-': ['C7', 'C8', 'C9', 'C10', 'D7', 'D8', 'D9', 'D10'],
       'Carboy': ['E7', 'E8', 'E9', 'E10','F7', 'F8','F9', 'F10' ]}

MICRONUTRIENT_MAP = {True: ['C3', 'C4', 'C5', 'C6','C7', 'C8', 'C9', 'C10',
                            'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10'],
                    False: ['D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10',
                            'F3', 'F4', 'F5', 'F6', 'F7', 'F8','F9', 'F10']}

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

melted['micronutrients'] = 'blank'
for micro, wells in MICRONUTRIENT_MAP.items():
    for idx, well in enumerate(wells):
        melted.loc[melted['well']==well, 'micronutrients'] = micro


melted['replicate'] = 0
for i in range(3, 11):
    for l in ['C', 'D', 'E', 'F']:
        if  i <= 6:
            ind = i-2
        else:
            ind = i - 6
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
for g, d in measurement.groupby(['water_source', 'micronutrients', 'replicate']):
    d = d.copy()
    d = d[(d['od_600nm_subtracted'] >= OD_BOUNDS[0]) & 
          (d['od_600nm_subtracted'] <= OD_BOUNDS[1])]
    d['elapsed_time_hr'] -= d['elapsed_time_hr'].min()
    trunc.append(d)
trunc = pd.concat(trunc, sort=False)
trunc = trunc[['strain', 'water_source', 'micronutrients', 'elapsed_time_hr', 
             'od_600nm_subtracted', 'growth_medium',  'replicate',
             'date', 'run_number']]
trunc.rename(columns={'od_600nm_subtracted':'od_600nm',
                      'replicate':'technical_replicate'}, inplace=True)
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
