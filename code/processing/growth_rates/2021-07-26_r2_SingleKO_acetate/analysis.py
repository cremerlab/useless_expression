#%%
import numpy as np 
import pandas as pd 
import futileprot.viz
import altair as alt
import altair_saver
import scipy.stats
colors, palette = futileprot.viz.altair_style()

# Add metadata
DATE = '2021-07-26'
RUN_NO = 2
STRAINS = 'SingleKO'
MEDIUM = 'acetate'

# Load the measurement data
data = pd.read_csv(f'./output/{DATE}_r{RUN_NO}_{STRAINS}_{MEDIUM}_exponential_phase.csv')

# Perform a simplistic inference of the growth rate to get a sense of what
# the result is.
data = data[['strain', 'elapsed_time_hr', 'od_600nm']]

# For each strain, infer the growth rate and compute the fit
layout = False
for g, d in data.groupby(['strain']):
    time_range = np.linspace(0, 1.25 * d['elapsed_time_hr'].max(), 10)

    # Perform the regression
    popt = scipy.stats.linregress(d['elapsed_time_hr'], np.log(d['od_600nm']))
    slope, intercept, err = popt[0], popt[1], popt[-1]
    print(f'{g}, {MEDIUM}: µ = {slope:0.3f} ± {err:0.3f} per hr.')
    # Compute the fit
    fit = np.exp(intercept + slope * time_range)
    fit_df = pd.DataFrame([])
    fit_df['elapsed_time_hr'] = time_range
    fit_df['od_600nm'] = fit

    # Generate the plot
    points = alt.Chart(
                        data=d, 
                        width=300,  
                        height=150
                    ).mark_point(
                        color=colors['primary_blue']
                    ).encode(
                        x=alt.X('elapsed_time_hr:Q', title='elapsed time [hr]'),
                        y=alt.Y('od_600nm:Q', title='optical density [a.u]',
                                scale=alt.Scale(type='log'))
                    )

    fit = alt.Chart(data=fit_df,
                    title=f'{g}, {MEDIUM}: µ = {slope:0.3f} ± {err:0.3f} per hr.'
                    ).mark_line(   
                        color=colors['primary_blue']
                    ).encode(
                        x='elapsed_time_hr:Q',
                        y='od_600nm:Q'
                    )
    merge = points + fit
    if layout == False:
        layout = merge
    else: 
        layout &= merge

altair_saver.save(layout, f'output/{DATE}_r{RUN_NO}_{STRAINS}_{MEDIUM}_fits.png',
                scale_factor=2)
# %%
