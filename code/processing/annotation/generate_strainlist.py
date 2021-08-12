#%%
import pickle 
import pandas as pd

# Load the strain list
strains = pd.read_csv('../../../data/strain_database/strain_list.csv')
strain_dict = {}
for g, d in strains.groupby('annotation'):
    strain_dict[g] = {k:v.values[0] for k, v in d.items()}
with open('../../../futileprot/package_data/strain_database.pkl', 'wb') as file:
    pickle.dump(strain_dict, file)


# %%
