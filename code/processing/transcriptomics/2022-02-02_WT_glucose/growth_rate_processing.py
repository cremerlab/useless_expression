#%%
import numpy as np 
import pandas as pd 
import altair as alt
import altair_saver
import futileprot.viz
import futileprot.growth
colors, palette = futileprot.viz.altair_style()

DATE = '2022-02-02'
STRAIN = 'WT'
MEDIUM = 'glucose'

# Load the growth curve data 
data = pd.read_csv(f'../../../../data/transcriptomics/{DATE}_{STRAIN}_{MEDIUM}/{DATE}_{STRAIN}_{MEDIUM}_growth_curve.csv')

# Infer the growth rate
data_df, param_df, opts = futileprot.growth.infer_growth_rate(od_bounds=[0.04, 0.4], data=data,groupby='date')

# Compute the fit for display.
time_range = np.linspace(0, 2, 100)
fit = opts[0]['popt'][1] * np.exp(time_range * opts[0]['popt'][0])
fit_df = pd.DataFrame([])
fit_df['elapsed_time_hr'] = time_range
fit_df['od_600nm'] = fit

# Set up the plot
points = alt.Chart(
        data=data_df
        ).mark_point(
            size=100,
            opacity=0.75
        ).encode(
            x=alt.X('elapsed_time_hr:Q', title='elapsed time [hr]'),
            y=alt.Y('od_600nm:Q', title='optical density [a.u.]',
                    scale=alt.Scale(type='log'))
        )
fit = alt.Chart(
        data=fit_df
        ).mark_line(
            size=1
        ).encode(
            x='elapsed_time_hr:Q',
            y='od_600nm:Q'
        ).properties(
            title=f"{DATE} {STRAIN} {MEDIUM}, λ = {opts[0]['popt'][0]:0.3f} ± {opts[0]['popt'][-1]:0.3f} per hr"
        )

layer = (points + fit)
altair_saver.save(layer, f'./output/{DATE}_{STRAIN}_{MEDIUM}_growth_curve.pdf')

# %%
