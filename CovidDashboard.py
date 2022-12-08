import numpy
import pandas as pd
import bokeh
from bokeh.io import curdoc
from bokeh.plotting import figure, show, output_file
from bokeh.models import DateRangeSlider, Select, ColumnDataSource, Button
from bokeh.layouts import column, grid, layout
from bokeh.events import ButtonClick
import json
from datetime import date, timedelta



### Define callback functions for slider and drop down menu



bokeh_doc = curdoc()

output_file('Covid_dashboard.html')

#### Date time slider
date_range_slider = DateRangeSlider(value=(date(2022, 12, 1), date(2022, 12, 3)),
                                    start=date(2022, 12, 1), end=date(2022, 12, 3))
									
									
def slider_callback(attr,old,new):
	daterange =date_range_slider.value_as_datetime
	datelist = pd.date_range(start=daterange[0],end=daterange[1]).strftime('%Y-%m-%d')
	
	
	
	
date_range_slider.on_change("value",slider_callback)



###
##### Load data from date range
f = open('Scraped_Data.json')
data = json.load(f)
f.close()

###
##### Create drop down menu for choosing country
menu = []
for i in data["2022-11-21"]:
	menu.append(i)

select = Select(title="Option:", value=menu[0], options=menu)


def select_callback(attr, old, new):
	selectedCountry = select.value

	
select.on_change('value',select_callback)

##
### BUTTON 
##

button = Button(label="Refresh plot", button_type="success")

def button_callback(event):
	x =[]
	y =[]
	daterange =date_range_slider.value_as_datetime
	datelist = pd.date_range(start=daterange[0],end=daterange[1]).strftime('%Y-%m-%d')
	selectedCountry = select.value
	
	for i in datelist:
		f = open(str(i) +'.json')
		data = json.load(f)
		f.close()
		x.append([i])
		y.append(data[selectedCountry]["Total Cases"])

	print(x)
	print(y)
	source_plot.data = dict(x_values = x, y_values = y)

button.on_event(ButtonClick,button_callback)
########################################
#### PLOTTING

plot_data = {'x_values': [],
			 'y_values': []}

source_plot = ColumnDataSource(data = plot_data)
p = figure()
p.vbar(x='x_values', top='y_values', source = source_plot, width=0.25)



# show layout
optionss = column(date_range_slider,select,button,p)
bokeh_doc.add_root(optionss)
bokeh_doc.title = "Covid Dashboard"

show(optionss)