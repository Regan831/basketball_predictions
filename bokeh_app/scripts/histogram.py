import pandas as pd
import numpy as np

from bokeh.plotting import figure
from bokeh.models import (CategoricalColorMapper, HoverTool,
						  ColumnDataSource, Panel,
						  FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider,
								  Tabs, CheckboxButtonGroup,
								  TableColumn, DataTable, Select)
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16


def histogram_tab(df_avgs_w_l):
    def make_dataset(conf_list, range_start = 0, range_end = 1, bin_width = 1/20, years=(2003,2004)):
        by_conf = pd.DataFrame(columns=['left', 'right', 'f_interval',
                                           'count', 'year',
                                           'name', 'color'])


        df = df_avgs_w_l[(df_avgs_w_l['Season'] >= years[0]) & (df_avgs_w_l['Season'] <= years[1])]
        # Iterate through all the conferences
        for i, conf_name in enumerate(conf_list):

            # Subset to the conference
            subset = df[df['ConfName'] == conf_name]

            # Create a histogram with 5 minute bins
            arr_hist, edges = np.histogram(subset['rpi'], bins = int(20), range = [.3, .75])

            # Divide the counts by the total to get a proportion
        #     arr_df = pd.DataFrame({'proportion': arr_hist / np.sum(arr_hist), 'left': edges[:-1], 'right': edges[1:] })
            arr_df = pd.DataFrame({'count': arr_hist, 'left': edges[:-1], 'right': edges[1:] })

            # Format the proportion
        #     arr_df['f_proportion'] = ['%0.5f' % proportion for proportion in arr_df['proportion']]

            # Format the interval
            arr_df['f_interval'] = ['%0.3f to %0.3f Rating' % (left, right) for left, right in zip(arr_df['left'], arr_df['right'])]

            # Assign the carrier for labels
            arr_df['name'] = conf_name

            # Color each carrier differently
            arr_df['color'] = Category20_16[i]

            # Add to the overall dataframe
            by_conf = by_conf.append(arr_df)

        # Overall dataframe
        by_conf = by_conf.sort_values(['name', 'left'])

        return ColumnDataSource(by_conf)

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
        p.quad(bottom = 0, left = 'left', right = 'right', top = 'count',
               color = 'color',  legend = 'name', source = src,
              fill_alpha = 0.8, hover_fill_alpha = 1.0, hover_fill_color = 'color', line_color = 'black')

        # Create the hover tool
        hover = HoverTool(tooltips = [('Conference', '@name'),
                                      ('Number of Teams', '@count'),
                                      ('RPI', '@f_interval')],
                         mode = 'vline')

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
                               bin_width = 1/20,
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

    src = make_dataset(initial_confs, range_start = .3, range_end = .75, bin_width = 1/20)

    p = make_plot(src)

    layout = row(controls, p)

    tab = Panel(child=layout, title = 'Histogram')

    return tab
