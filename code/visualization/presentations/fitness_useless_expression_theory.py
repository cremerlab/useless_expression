#%%
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import futileprot.viz
colors, palette = futileprot.viz.matplotlib_style()



fig, ax = plt.subplots(1, 1, figsize=(6, 4))
ax.set_xlabel('useless expression $\phi_X$ ')
ax.set_ylabel('fitness')


# Plot the theory curve
phiX_range =np.linspace(0, 0.4, 100)
fitness = 1/(1 - phiX_range)


#%%

data = pd.read_csv('../../../data/literature/Scott2010/Scott2010_Fig4B.csv')
data.head()
# %%
fig, ax = plt.subplots(1, 1, figsize=(6, 4))
ax.set_xlabel('useless expression $\phi_X$ ')
ax.set_ylabel('fitness')


# Plot the theory curve
phiX_range =np.linspace(0, 1, 100)
fitness = (1 - phiX_range)

ax.plot(phiX_range, fitness, 'k-', label='prediction')
for g, d in data.groupby(['medium_id']):
    d['fitness'] = d['growth_rate_hr'] / d[d['phi_X']==d['phi_X'].min()]['growth_rate_hr'].values 
    ax.plot(d['phi_X']/100, d['fitness'], 'o', label=g)
# ax.set_yscale('log')

# %%
