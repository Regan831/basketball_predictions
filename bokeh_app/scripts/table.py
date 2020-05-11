import pandas as pd
import numpy as np

from bokeh.models import ColumnDataSource, Panel
from bokeh.models.widgets import TableColumn, DataTable

def table_tab(df):

	# Calculate summary stats for table
	conf_stats = df.groupby('ConfName')['rpi'].describe()
	conf_stats = conf_stats.reset_index().rename(
		columns={'ConfName': 'conference', 'count': 'rpi', '50%':'median'})

	# Round statistics for display
	conf_stats['mean'] = conf_stats['mean'].round(2)
	conf_src = ColumnDataSource(conf_stats)

	# Columns of table
	table_columns = [TableColumn(field='conference', title='Conference'),
					 TableColumn(field='rpi', title='Number of Teams'),
					 TableColumn(field='min', title='Lowest RPI'),
					 TableColumn(field='mean', title='Mean RPI'),
					 TableColumn(field='median', title='Median RPI'),
					 TableColumn(field='max', title='Highest RPI')]

	conf_table = DataTable(source=conf_src,
							  columns=table_columns, width=1000)

	tab = Panel(child = conf_table, title = 'Summary Table')

	return tab
