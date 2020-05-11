import pandas as pd
from bokeh.sampledata.iris import flowers

from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, HoverTool, Panel, Range1d
from bokeh.layouts import column, row, WidgetBox
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider,
								  Tabs, CheckboxButtonGroup,
								  TableColumn, DataTable, Select)


def plot_tab(df_avgs_w_l):
    def make_dataset(conf_list, years=(2003,2004)):
        df = df_avgs_w_l[(df_avgs_w_l['Season'] >= years[0]) & (df_avgs_w_l['Season'] <= years[1])]
        subset = pd.DataFrame(columns=df.columns)

        for conf in conf_list:
            subset = subset.append(df[df['ConfName'] == conf])

        new_src = ColumnDataSource(subset)

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
        p = figure(title = "Wins Vs. KenPom Rating", plot_height = 600, plot_width = 800,)
        p.xaxis.axis_label = 'KenPom Rating'
        p.yaxis.axis_label = 'Wins'
        p.x_range =  Range1d(-40, 40)
        p.y_range =  Range1d(0, 35)

        # Create the hover tool
        hover = HoverTool(tooltips=[
            ("Team", "@TeamName"),
            ("Conference", "@ConfName"),
            ("Wins", "@n_wins"),
            ("KenPom", "@kp_rating"),
            ('Year', "@Season"),
            ('Seed', '@seed')
            ])

        p.circle('kp_rating', 'n_wins', color='colors',
                 fill_alpha=0.2, size=10, source=src)

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
        new_src = make_dataset(confs_to_plot, years=years)

        # Update the source used
        src.data.update(new_src.data)

    colormap = {False: 'red', True: 'green'}
    df_avgs_w_l['colors'] = [colormap[x] for x in df_avgs_w_l['made_tourn']]

    conf_selection = CheckboxGroup(labels=list(df_avgs_w_l['ConfName'].unique()),
                               active = [0])
    conf_selection.on_change('active', update)

    year_select = RangeSlider(start = 2003, end = 2019,
                         step = 1, value = [2003,2004],
                         title = 'Year')
    # Update the plot when the value is changed
    year_select.on_change('value', update)

    controls = WidgetBox(year_select, conf_selection)

    initial_confs = [conf_selection.labels[i] for i in conf_selection.active]

    src = make_dataset(initial_confs)

    p = make_plot(src)

    layout = row(controls, p)

    tab = Panel(child=layout, title = 'Plot')

    return tab
