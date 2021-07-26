"""
Plate Reader Data Collation
===========================
This script reads through all experiments within `code/processing/plate_reader/`
and collates all data from "accepted" experiments.

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

# Get all of the folders 
folders = glob.glob('../growth_rates/*') 

# Parse the frontmatter from the README.md files.
valid_paths = []
record = pd.DataFrame([])
for i, folder in enumerate(folders):
   exp_info = futileprot.io.scrape_frontmatter(folder)  
   exp_info['experiment'] = folder.split('/')[-1]
   record = record.append(exp_info, ignore_index=True)
   if exp_info['status'].lower() == 'accepted':
       valid_paths.append(folder)

# Format and store the experiment record
record = record[['experiment', 'status', 'description']]
record.sort_values(by='experiment', inplace=True)
record.to_csv('../../../data/collated/collated_experiment_record_OD600_growth_curves.csv', 
              index=False)


# For each valid path, iterate through and concatenate the relevant files. 
_curves = []
_exp_phase = []
for i, path in enumerate(valid_paths): 
    _curves.append( pd.read_csv(f"{path}/output/{path.split('/')[-1]}_measurements.csv"))
    _exp_phase.append(pd.read_csv(f"{path}/output/{path.split('/')[-1]}_exponential_phase.csv"))
curves = pd.concat(_curves, sort=False)
exp_phase = pd.concat(_exp_phase, sort=False)

curves.to_csv('../../../data/collated/collated_OD600_growth_curves.csv', index=False)
exp_phase.to_csv('../../../data/collated/collated_OD600_growth_curves_exponential_phase.csv', index=False)



# %%
