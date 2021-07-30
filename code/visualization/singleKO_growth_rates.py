#%%
import numpy as np 
import pandas as pd 
import altair as alt 
import altair_saver
import futileprot.viz 
colors, palette = futileprot.viz.altair_style()

# Load the percentiles
data = pd.read_csv('../../data/mcmc/growth_rate_inference_summaries.csv')
data.head()
# %%

# Look first at only the hyper parameters
hyper = data[data['replicate']=='hyperparameter']

bar_chart = alt.Chart(hyper).mark_bar().encode(
        x=alt.X('low:Q', title='growth rate [per hr]'),
        x2=alt.X2('high:Q'),
        y=alt.Y('strain:N', title='strain'),
        color=alt.Color('growth_medium:N', title='growth medium'),
        opacity=alt.Opacity('percentile:N', title='credible interval [%]',  
                            sort='descending')
)

altair_saver.save(bar_chart, './output/SingleKO_glucose_acetate_growth_rates.pdf')
# %%
