import numpy as np
import pandas as pd
import bokeh
from bokeh.io import curdoc
from bokeh.plotting import figure, show, output_file
from bokeh.models import DateRangeSlider, Select, ColumnDataSource, Button
from bokeh.layouts import column, grid, layout, row
from bokeh.events import ButtonClick
import json
from datetime import date, timedelta

### Initialize variables

#plot_data = {'x_values': [],
#			 'y_values': []}
			 

plot_data = {'x_values': ['2022-12-01', '2022-12-02', '2022-12-03'], 'y_values': [0,0,0]}
source_plot = ColumnDataSource(data = plot_data)

### Define callback functions for slider and drop down menu

bokeh_doc = curdoc()

#output_file('Covid_dashboard.html')

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

##### Create drop down menu for choosing country
menu = []
for i in data["2022-11-21"]:
	menu.append(i)

select = Select(title="Country:", value=menu[0], options=menu)

def select_callback(attr, old, new):
	selectedCountry = select.value

	

	
select.on_change('value',select_callback)

##
### BUTTON 
##
button = Button(label="Refresh plot", button_type="success")

def button_callback():
	x =[]
	y =[]
	x2 = []
	y2 = []
	daterange =date_range_slider.value_as_datetime
	datelist = pd.date_range(start=daterange[0],end=daterange[1]).strftime('%Y-%m-%d')
	selectedCountry = select.value
	
	for i in datelist:
		f = open(str(i) +'.json')
		data = json.load(f)
		f.close()
		x.append(i)
		y.append(data[selectedCountry]["New Deaths /1M"])	
		x2.append(i)
		y2.append(data[selectedCountry]["Total Deaths /1M"])
		
		
	source_plot.data = dict(x_values = x, y_values = y)
	p.x_range.factors = x
	source_plot2.data = dict(x_values = x2, y_values = y2)
	p2.x_range.factors = x2
	
	



button.on_click(button_callback)

########################################
#### PLOTTING

p = figure(x_range=plot_data['x_values'],title = "New Deaths /1M")
p.vbar(x='x_values', top='y_values', source = source_plot, width=0.25)
p.y_range.start = 0


plot_data2 = {'x_values': ['2022-12-01', '2022-12-02', '2022-12-03'], 'y_values': [0,0,0]}
source_plot2 = ColumnDataSource(data = plot_data)

p2 = figure(x_range=plot_data2['x_values'],title = "Total Deaths /1M")
p2.vbar(x='x_values', top='y_values', source = source_plot2, width=0.25)
p2.y_range.start = 0











# show layout


plots = row(p,p2)
optionss = column(date_range_slider,select,button,plots)
bokeh_doc.add_root(optionss)
bokeh_doc.title = "Covid Dashboard"

#show(optionss)