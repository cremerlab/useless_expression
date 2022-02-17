#%%
import numpy as np 
import pandas as pd 
import tqdm
import scipy.integrate
import futileprot.viz
import futileprot.model
import panel as pn 
import bokeh.io 
import bokeh.plotting
import bokeh.models
bokeh.io.output_notebook()
colors, palette = futileprot.viz.bokeh_style()
const = futileprot.model.load_constants()

# %%
# Set some parameters
n_muts = 20
gamma_max = const['gamma_max']
nu_max = np.random.normal(4.5, 1, n_muts)
phi_O = const['phi_O']
Kd_TAA = const['Kd_TAA']
Kd_TAA_star = const['Kd_TAA_star']
tau = const['tau']
kappa_max = const['kappa_max']
Kd_cnt = const['Kd_cnt']
c_nt = 0.010
Y = const['Y']

# Set the initial conditions
M_tot = 0.01 * const['OD_conv']
M0 = (1 / n_muts) * np.ones(n_muts) * M_tot
phi_Rb = 0.02
phi_O = const['phi_O']
phi_Mb = 1 - phi_Rb - phi_O
MRb = phi_Rb * M0
MMb = phi_Mb * M0
TAA = np.ones(n_muts) * 1E-5
TAA_star = np.ones(n_muts) * 1E-5

# Pack the arguments
params = []
for i in range(n_muts): 
    params.append(M0[i])
    params.append(MRb[i])
    params.append(MMb[i])
    params.append(TAA[i])
    params.append(TAA_star[i])
params.append(c_nt) 

# Pack the parameters
args = {'gamma_max': gamma_max,
        'nu_max': np.array(nu_max),
        'Kd_TAA': Kd_TAA,
        'Kd_TAA_star': Kd_TAA_star,
        'tau': tau,
        'kappa_max':kappa_max,
        'phi_O': phi_O,
        'nutrients': {'Kd_cnt': Kd_cnt,
                    'Y': Y}}

# %%
dt = 0.001
time_range = np.arange(0, 7.5, dt)
out = scipy.integrate.odeint(futileprot.model.self_replicator_FPM,
                            params, time_range, args=(args,))
out = out.T
dfs = []
cols = ['M', 'MRb', 'MMb', 'TAA', 'TAA_star']

idx = 0
for j in range(0, n_muts * 5, 5):
    _df = pd.DataFrame([])
    _out = out[j:j+5] 
    for i, c in enumerate(cols):
        _df[c] = _out[i]
    _df['time'] = time_range
    _df['c_nt'] = out[-1] 
    _df['idx'] = (j + 5) / 5
    _df['nu_max'] = nu_max[int((j+5)/5) - 1]
    dfs.append(_df)
    idx += 1
df = pd.concat(dfs, sort=False)

