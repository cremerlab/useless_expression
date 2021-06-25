#%%
import numpy as np 
import pandas as pd 
import altair as alt
from altair_saver import save
import futileprot as fp


colors, palette = fp.viz.altair_style()

data = pd.read_csv('../../../../data/spectrophotometry/2021-06-24_growth_curves/2021-06-24_growth_curves.csv')

tidy, params, opts = fp.growth.infer_growth_rate(data, 
                                                 groupby=['growth_medium', 'strain'],
                                                 od_bounds=[0.04, 0.4], 
                                                 print_params=False)

# %%

# Rename the strains in the data and parameter dataframes 
tidy['strain'] = [s.replace('delta_', 'Δ') for s in tidy['strain'].values]
params['strain'] = [s.replace('delta_', 'Δ') for s in params['strain'].values]

points = alt.Chart(tidy, 
                   width=200, 
                   height=200
            ).mark_line(
                    point=True, 
                    opacity=0.75
            ).encode(
                    x=alt.X('elapsed_time_hr:Q', title='elapsed time [hr]'),
                    y=alt.Y('od_600nm:Q', title='optical density', scale=alt.Scale(type='log')),
                    color=alt.Color('strain:N', 
                                    title='strain', 
                                    scale=alt.Scale(scheme='tableau10'))
            ).facet(column=alt.Column('growth_medium:N', 
                                    header=alt.Header(labelFontSize=15)),
                    row=alt.Row('strain:N', 
                                header=alt.Header(labelFontSize=15))
            ).resolve_scale(x='independent')

save(points, '2021-06-24_KO_growth_curves.pdf')
# %%
# Make a plot of the growth rates for each medium 
growth_rates = params[params['parameter']=='growth_rate']
plots = []
for g, d in growth_rates.groupby(['growth_medium']):
    min_val = 0.9 * d['map_val'].min()
    max_val = 1.1 * d['map_val'].max()
    lam_base= alt.Chart(d,
                       width=400, 
                       height=200,
                ).transform_calculate(
                    ymin='datum.map_val-datum.cred_int',
                    ymax='datum.map_val+datum.cred_int'
                ).encode(
                    x=alt.X(
                            'strain:N', 
                            title='strain'), 
                    color=alt.Color(
                            'strain:N', 
                            title='strain',
                            scale=alt.Scale(scheme='tableau10')))


    lam_points = lam_base.mark_point(size=80, 
                                 opacity=0.75
                ).encode(
                    y=alt.Y('map_val:Q', 
                            title='growth rate [inv. hr]',
                            scale=alt.Scale(domain=[min_val, max_val])), 
                )
                
    lam_lines = lam_base.mark_errorbar(
                ).encode(
                    y='ymin:Q',
                    y2='ymax:Q' 
                    )
                
 
    _plot = (lam_points + lam_lines).properties(title=g)
    plots.append(_plot) 
plot = plots[0] & plots[1]
save(plot, '2021-06-24_KO_growth_rates.pdf')

#%%
# Plot the fits
plots = 0
for g, d in params.groupby(['strain']):
    _plots = 0
    for _g, _d in d.groupby(['growth_medium']):
        # Get the data 
        _data = tidy[(tidy['growth_medium'] == _g) & 
                     (tidy['strain'] == g)]
        points = alt.Chart(
                        data=_data,
                        width=200,
                        height=200
                ).mark_point(
                        size=80, 
                        opacity=0.75
                ).encode(
                        x=alt.X('elapsed_time_hr:Q', 
                                title='elapsed time [hr]'),
                        y=alt.Y('od_600nm:Q', 
                                title='optical density [a.u.]',
                                scale=alt.Scale(type='log')),
                )
        # Compute the fit
        od_init = _d[_d['parameter']=='od_init']['map_val'].values[0]
        lam = _d[_d['parameter']=='growth_rate']['map_val'].values[0]
        time_range = np.linspace(0, _data['elapsed_time_hr'].max(), 200)
        fit = od_init * np.exp(lam * time_range)
        __df = pd.DataFrame([]) 
        __df['elapsed_time_hr'] = time_range
        __df['od_600nm'] = fit 
        
        # Plot the fit
        _fit = alt.Chart(__df).mark_line().encode(
                    x=alt.X('elapsed_time_hr:Q'),
                    y=alt.Y('od_600nm:Q')
                )
        subplot = (points + _fit).properties(title=f'{g}, {_g} growth')
        if _plots == 0:
            _plots = subplot
        else: 
            _plots |= subplot

    if plots == 0: 
        plots = _plots
    else:
        plots &= _plots


# plot = alt.layer(plots)
save(plots, '2021-06-24_KO_growth_curves_with_fit.pdf')
# %%

# Print the growth rates:
for g, d in growth_rates.groupby(['growth_medium']):
    print(f"""
{g} supported growth
==================================
""")
    for _g, _d in d.groupby(['strain']):
        print(f"{_g}: λ = {_d['map_val'].values[0]:0.3f} ± {_d['cred_int'].values[0]:0.3f} per hr.")

# %%
