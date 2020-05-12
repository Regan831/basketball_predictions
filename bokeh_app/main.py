
# Pandas for data management
import pandas as pd

# os methods for manipulating paths
from os.path import dirname, join

# Bokeh basics
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs
from bokeh.plotting import output_file,show


# Each tab is drawn by one script
from scripts.histogram import histogram_tab
from scripts.density import density_tab
from scripts.table import table_tab
from scripts.plot import plot_tab

# Read data into dataframes
df_avgs_w_l = pd.read_pickle('df_avgs_w_l')
df_avgs_w_l['rpi'] = pd.to_numeric(df_avgs_w_l['rpi'], errors='coerce')

# Create each of the tabs
tab1 = histogram_tab(df_avgs_w_l)
tab2 = density_tab(df_avgs_w_l)
tab3 = table_tab(df_avgs_w_l)
tab4 = plot_tab(df_avgs_w_l)
# tab5 = route_tb(flights)

# Put all the tabs into one application
tabs = Tabs(tabs = [tab1, tab2, tab3, tab4])

# Put the tabs in the current document for display
curdoc().add_root(tabs)

output_file('plots.html')

show(tabs)
