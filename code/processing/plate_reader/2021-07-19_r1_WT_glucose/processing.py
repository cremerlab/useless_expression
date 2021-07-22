#%%
import numpy as np 
import pandas as pd 

# Define experiment parameters
DATE = '2021-07-19'
STRAINS = 'WT'
MEDIUM = 'glucose'
ROOT = '../../../..'
SKIPROWS = 28

# Add the well identifiers
MAP = {'WT':['C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10',
               'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10',
               'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10',
               'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10'
               ]}

# Generate a list of all valid wells
wells = [f'{letter}{number}' for letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] for number in np.arange(1,13)]
# Load the data
data = pd.read_csv(f'{ROOT}/data/plate_reader/{DATE}_{STRAINS}_{MEDIUM}/{DATE}.csv', 
                skiprows=SKIPROWS)

# Melt and drop unnecessary stuff
melted = data.melt(id_vars=['Time'], var_name='well', value_name='od_600nm')
melted = melted.loc[melted['well'].isin(wells)]
melted.dropna(inplace=True)

# Add strain identifier and replicates
melted['strain'] = 'blank'
melted['replicate'] = 0
for strain, wells in MAP.items():
    for idx, well in enumerate(wells):
        melted.loc[melted['well']==well, 'strain'] = strain
        melted.loc[melted['well']==well, 'replicate'] = idx + 1

# Add information regarding date and growth medium
melted['growth_medium'] = MEDIUM
melted['date'] = DATE

# Convert time to elapsed time
melted['time_sec'] = pd.to_timedelta(melted['Time'].values)
melted['time_sec'] = melted['time_sec'].dt.total_seconds()
melted['elapsed_time_hr'] = (melted['time_sec'] - melted['time_sec'].min())/3600

# Drop unnecessary Time columns
melted.drop(columns=['Time', 'time_sec'], inplace=True)


# Reformat blank value as average eentry per time
measurement = []
for g, d in melted.groupby(['elapsed_time_hr']):
    d = d.copy()
    avg_blank = d[d['strain']=='blank']
    meas = d[d['strain']!='blank']
    meas['avg_blank_value'] = d['od_600nm'].mean()
    measurement.append(meas)
measurement = pd.concat(measurement, sort=False)


# Save to disk
measurement.to_csv(f'./output/{DATE}_{STRAINS}_{MEDIUM}_measurements.csv', index=False)
