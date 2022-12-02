import numpy
import bokeh
from bokeh.io import curdoc
from bokeh.plotting import figure, show, output_file
from bokeh.models import DateRangeSlider, Select, ColumnDataSource
from bokeh.layouts import column, grid, layout
import json
from datetime import date



### Define callback functions for slider and drop down menu


	


bokeh_doc = curdoc()

output_file('Covid_dashboard.html')

#### Date time slider
#date_range_slider = DateRangeSlider(value=(date(2022, 11, 21), date(2022, 11, 28)),
#                                    start=date(2022, 11, 21), end=date(2022, 11, 28))
									
									
#def slider_callback(attr,old,new):
#	daterange =date_range_slider.value
	
#date_range_slider.on_change("value",slider_callback)



###
##### Load data from date range
f = open('2022-11-21.json')
data = json.load(f)
f.close()

f = open('2022-11-22.json')
data2 = json.load(f)
f.close()



###
##### Create drop down menu for choosing country
menu = []
for i in data:
	menu.append(i)

select = Select(title="Option:", value=menu[0], options=menu)

plot_data = {'x_values': [],
			 'y_values': []}

source_plot = ColumnDataSource(data = plot_data)

def select_callback(attr, old, new):
	source_plot.data = dict(x_values = [0,1], y_values = [data[select.value]["Total Cases"], data2[select.value]["Total Cases"]])
	print(source_plot.data)
	#source_plot.data = {
		#'x_values':[1,2],
		#'y_values':[data[select.value]["Total Cases"], data2[select.value]["Total Cases"]]}

	
select.on_change('value',select_callback)




########################################
#### PLOTTING
# prepare some data
#x = [1,2]
#y = [data[Country]["Total Cases"], data2[Country]["New Deaths"]]

			 

p = figure()
p.vbar(x='x_values', top='y_values', source = source_plot, width=0.5)


# show layout
#optionss = column(date_range_slider,select)
optionss = column(select)
layouts = grid([optionss,p],sizing_mode='stretch_both')

bokeh_doc.add_root(layouts)
bokeh_doc.title = "Covid Dashboard"

show(layouts)