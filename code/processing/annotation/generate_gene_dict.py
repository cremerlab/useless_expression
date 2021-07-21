#%%
import pickle
import tqdm
import pandas as pd

# Load the master gene list
colicogs = pd.read_csv('../../../data/escherichia_coli_gene_index.csv')

#%%
# Load the gene classification scheme from Mori 2021
classifier = pd.read_csv('../../../data/Mori2021/Mori2021_EV11_sector_assignments.csv')

#%%
# Create a map of common name to sector as defined by Balakrishnan et al 2021
colicogs['sector'] = 'Not Assigned'
for g, d in tqdm.tqdm(classifier.groupby(['gene_name']), desc='Assigning sectors...'):
    # Get the entry in the colicogs
    entry = colicogs[colicogs['name'].str.lower() == g.lower()]
    if len(entry) > 0:
        common_name = entry['common_name'].values[0]
        colicogs.loc[colicogs['common_name'] == common_name, 
                                            'sector'] = d['sector'].values[0]

# Instantiate the dictionary to save
colidict = {}

for g, d in colicogs.groupby(['strain']):
    strain_dict = {}
    for _g, _d in tqdm.tqdm(d.groupby(['name']), 
                            desc=f'Generating dict for {g}'):
        _common_name = _d['common_name'].values[0]
        _cog_class = _d['cog_class'].values[0]
        _cog_letter = _d['cog_letter'].values[0]
        _cog_desc = _d['cog_desc'].values[0]
        _sector = _d['sector'].values[0]
        _product = _d['product'].values[0]
        strain_dict[_g.lower()] = {'common_name':_common_name,
                           'cog_class':_cog_class,
                           'cog_letter':_cog_letter,
                           'cog_desc':_cog_desc,
                           'sector': _sector,
                           'product':_product}
    colidict[g.lower()] = strain_dict

# Save the dictionary to disk 
with open('../../../futileprot/package_data/coli_gene_dict.pkl', 'wb') as file:
    pickle.dump(colidict, file)
print('Finished! Dictionary saved to `package_data`!')

# %%
