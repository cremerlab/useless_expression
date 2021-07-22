"""
Plate Reader Data Collation
===========================
This script reads through all experiments within `code/processing/plate_reader/`
and collates all data from "accepted" experiments. It saves three files. All 
end with the suffix "PR" which corresponds to "plate reader" and differentiates
between other types of OD600 growth curves (such as manual spectrophotometry).

`collated_experiment_record_OD600_PR.csv`:
    This is a long-form tidy CSV file with records of all experiments that were
    performed, regardless of their accpetance or rejection, and annotates 
    which were used and why. This information is based on the "status" and 
    "description" fields on the README.md file associated with each experiment.

`collated_growth_curves_OD600_PR.csv` 
    This is a long-form tidy CSV file with all growth curves taken across strains 
    and conditions. Only experiments marked as "accepted" in the README.md 
    frontmatter is included in this file.

`collated_exponential_phase_growth_OD600_PR.csv`
    This is a long-form tidy CSV file with all growth measurements deemed to 
    be in the exponential phase of growth. Only experiments marked as "accepted" 
    in the README.md frontmatter is included in this file.
"""
#%%
import numpy as np 
import pandas as pd 
import futileprot.io

