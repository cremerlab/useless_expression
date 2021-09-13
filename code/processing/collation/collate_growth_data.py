"""
Growth Curve Collation
===========================
This script reads through all experiments within `code/processing/growth_curves/`
and `code/procssing/diauxic_shifts/` and collates all data from "accepted" experiments.

`collated_experiment_record_OD600_growth_curves.csv`:
    This is a long-form tidy CSV file with records of all experiments that were
    performed, regardless of their accpetance or rejection, and annotates 
    which were used and why. This information is based on the "status" and 
    "description" fields on the README.md file associated with each experiment.

`collated_OD600_growth_curves.csv
    This is a long-form tidy CSV file with all growth curves taken across strains 
    and conditions. Only experiments marked as "accepted" in the README.md 
    frontmatter is included in this file.

`collated_OD600_growth_curves_exponential_phase.csv`
    This is a long-form tidy CSV file with all growth measurements deemed to 
    be in the exponential phase of growth. Only experiments marked as "accepted" 
    in the README.md frontmatter is included in this file.
"""
#%%
import numpy as np 
import pandas as pd 
import futileprot.io
import glob

# Get all of the folders for growth rates
gr_folders = glob.glob('../growth_rates/*') 

# Get all of the folders for diauxic shifts
diaux_folders = glob.glob('../diauxic_shifts/*') 

# Parse the frontmatter from the README.md files.
valid_paths = [[], []]
record = pd.DataFrame([])
exp_type = ['growth curve measurement', 'diauxic shift measurement']
for i, cat in enumerate([gr_folders, diaux_folders]):
    for _, folder in enumerate(cat):
        exp_info = futileprot.io.scrape_frontmatter(folder)  
        exp_info['experiment'] = folder.split('/')[-1]
        exp_info['experiment_type'] = exp_type[i]
        record = record.append(exp_info, ignore_index=True)
        if exp_info['status'].lower() == 'accepted':
            valid_paths[i].append(folder)

# Format and store the experiment record
record = record[['experiment', 'experiment_type',  'status', 'description']]
record.sort_values(by='experiment', inplace=True)
record.to_csv('../../../data/collated/collated_experiment_record_OD600_growth_curves.csv', 
              index=False)

#%%
shift_curves = []
_exp_phase = []
for i, cat in enumerate(valid_paths): 
    for j, path in enumerate(cat):
        if i == 0:
            exp_phase = pd.read_csv(f"{path}/output/{path.split('/')[-1]}_exponential_phase.csv")
            exp_phase['experiment_type'] = exp_type[i]
            exp_phase.rename(columns={'technical_replicate':'replicate',
                                      'od_600nm':'od_600nm_subtracted'}, inplace=True)
            _exp_phase.append(exp_phase)
        elif i == 1:
            exp_phase = pd.read_csv(f"{path}/output/{path.split('/')[-1]}_labeled_regions.csv")
            shift_curves.append(exp_phase)
            exp_phase = exp_phase[exp_phase['phase'].str.contains('exponential')]
            exp_phase.loc[exp_phase['phase']=='exponential_glucose', 'growth_medium'] = 'ga_preshift'
            exp_phase.loc[exp_phase['phase']=='exponential_acetate', 'growth_medium'] = 'acetate'
            exp_phase['experiment_type'] = exp_type[i]
            _exp_phase.append(exp_phase) 
            
shift_curves = pd.concat(shift_curves, sort=False)
shift_curves = shift_curves[['date', 'run_number', 'class', 'identifier',
                             'strain', 'replicate', 'growth_medium', 'phase',
                             'elapsed_time_hr', 'od_600nm_subtracted']]
exp_phase = pd.concat(_exp_phase, sort=False)
exp_phase = exp_phase[['date', 'run_number', 'class', 'identifier', 'strain', 
                       'replicate', 'growth_medium', 'elapsed_time_hr', 
                       'od_600nm_subtracted']]
#%%
shift_curves.to_csv('../../../data/collated/collated_diauxic_shifts_labeled.csv', index=False)
exp_phase.to_csv('../../../data/collated/collated_OD600_growth_curves_exponential_phase.csv', index=False)

print('Collation of growth measurements is complete.')

# %%
