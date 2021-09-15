#%%
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import futileprot.viz
colors, palette = futileprot.viz.matplotlib_style()






# Plot the theory curve

phi_O_high = 0.65
phi_O_low = 0.52
phiX_range_low = np.linspace(0, 1 - phi_O_low-0.001, 100)
phiX_range_high = np.linspace(0, 1 - phi_O_high-0.001, 100)





data = pd.read_csv('../../../data/literature/Scott2010/Scott2010_fig4.csv')


fig, ax = plt.subplots(1, 2, figsize=(6, 3))
for a in ax:
    a.set_ylabel('fitness')

ax[0].set_xlabel('useless expression (induced) $\phi_X*$ ')
ax[0].set_title('overexpression of useless protein')
ax[1].set_title('underexpression of useless protein')
ax[1].set_xlabel('useless expression (native) $\phi_X$ ')

# for a in ax:
    # a.set_yscale('log')
ax[0].set_ylim([1E-2, 1.2])
ax[0].set_xlim([-0.01, 0.5])

# Plot the theory curve

phiX_range =np.linspace(0, 1, 100)
oe_fitness_low = (1 - phi_O_low - phiX_range_low) / (1 - phi_O_low)
oe_fitness_high = (1 - phi_O_high - phiX_range_low) / (1 - phi_O_high)
ue_fitness_low = (1 - phi_O_low - phiX_range_low) / (1 - phi_O_low - phiX_range_low.max())
ue_fitness_high = (1 - phi_O_high - phiX_range_high) / (1 - phi_O_high - phiX_range_high.max())

ax[0].fill_between(phiX_range_low, oe_fitness_high, oe_fitness_low,
                 label='prediction', color='grey', alpha=0.5)
ax[1].fill_between(phiX_range_low, ue_fitness_high, ue_fitness_low,
                 label='prediction', color='grey', alpha=0.5)

# ax.set_yscale('log')
ax[0].legend()
plt.tight_layout()
plt.savefig('../../../figures/presentations/useless_expression_nodata.pdf')


for g, d in data.groupby(['source']):
    ax[0].plot(d['phi_X']/100, d['fitness'], 'o', label=g, ms=4)
ax[0].legend()
plt.tight_layout()
plt.savefig('../../../figures/presentations/useless_expression_data.pdf')

# 

# %%

