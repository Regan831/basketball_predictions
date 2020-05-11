import pandas as pd
import numpy as np

from scipy.stats import gaussian_kde

from bokeh.plotting import figure
from bokeh.models import (CategoricalColorMapper, HoverTool,
						  ColumnDataSource, Panel,
						  FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider,
								  Tabs, CheckboxButtonGroup,
								  TableColumn, DataTable, Select)
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16


def density_tab(df_avgs_w_l):
    def make_dataset(conf_list, range_start, range_end, bandwidth=1, years=(2003,2003)):
        df = df_avgs_w_l[(df_avgs_w_l['Season'] >= years[0]) & (df_avgs_w_l['Season'] <= years[1])]

        xs = []
        ys = []
        colors = []
        labels = []

        for i, conf in enumerate(conf_list):
            subset = df[df['ConfName'] == conf]

            kde = gaussian_kde(subset['rpi'], bw_method=bandwidth)

    		# Evenly space x values
            x = np.linspace(range_start, range_end, 100)
    		# Evaluate pdf at every value of x
            y = kde.pdf(x)

    		# Append the values to plot
            xs.append(list(x))
            ys.append(list(y))

    		# Append the colors and label
            colors.append(Category20_16[i])
            labels.append(conf)

        new_src = ColumnDataSource(data={'x': xs, 'y': ys,
    							   'color': colors, 'label': labels})

        return new_src

    def style(p):
        # Title
        p.title.align = 'center'
        p.title.text_font_size = '20pt'
        p.title.text_font = 'serif'

        # Axis titles
        p.xaxis.axis_label_text_font_size = '14pt'
        p.xaxis.axis_label_text_font_style = 'bold'
        p.yaxis.axis_label_text_font_size = '14pt'
        p.yaxis.axis_label_text_font_style = 'bold'

        # Tick labels
        p.xaxis.major_label_text_font_size = '12pt'
        p.yaxis.major_label_text_font_size = '12pt'

        return p

    def make_plot(src):
        # Create the figure
        p = figure(plot_height = 600, plot_width = 800, title = 'Histogram of RPI by Conference',
                  x_axis_label = 'RPI', y_axis_label = 'Count')

        # Add the quad glpyh with the source by conference
        p.multi_line('x', 'y', color = 'color', legend = 'label',
					 line_width = 3,
					 source = src)

        # Create the hover tool
        hover = HoverTool(tooltips=[('Conference', '@label'),
            ('RPI', '$x'),
            ('Density', '$y')],
            line_policy = 'next')

        # Add styling and hover tool
        p.add_tools(hover)

        p.legend.click_policy = 'hide'

        # Styling
        p = style(p)

        return p

    def update(attr, old, new):
        # Get the list of carriers for the graph
        confs_to_plot = [conf_selection.labels[i] for i in
                            conf_selection.active]

        years = (year_select.value[0], year_select.value[1])
        # Make a new dataset based on the selected carriers and the
        # make_dataset function defined earlier
        new_src = make_dataset(confs_to_plot,
                               range_start = .3,
                               range_end = .75,
                               bandwidth = 1,
                               years=years)


        # Update the source used the quad glpyhs
        src.data.update(new_src.data)

    conf_selection = CheckboxGroup(labels=list(df_avgs_w_l['ConfName'].unique()),
                                  active = [0])
    conf_selection.on_change('active', update)


    # Slider to select the binwidth, value is selected number
    year_select = RangeSlider(start = 2003, end = 2019,
                         step = 1, value = [2003,2004],
                         title = 'Year')
    # Update the plot when the value is changed
    year_select.on_change('value', update)

    controls = WidgetBox(year_select, conf_selection)

    initial_confs = [conf_selection.labels[i] for i in conf_selection.active]

    src = make_dataset(initial_confs, range_start = .3, range_end = .75, bandwidth=1, years=(2003,2003))

    p = make_plot(src)

    layout = row(controls, p)

    tab = Panel(child=layout, title = 'Density')

    return tab
