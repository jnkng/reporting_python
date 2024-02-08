#!/usr/bin/env python
# coding: utf-8

# # Interactive Graphics - Plotly
# 
# <span style="font-family:Apple Chancery"><font size="4"> - An interactive graph is worth a thousand static graphs -</font></span>
# 
# So far, we have introduced static plots. An extension to this are interactive plots. Interactivity means for example displaying additional information when hovering the mouse over data points, selecting single traces from the legend or being able to select a value range with a slider. To display time varying effects, animated graphics can be a suitable choice.
# 
# To build such graphics, we will use the package [**plotly**](https://plotly.com). Plotly is based on javascript and uses dictionaries when it comes to specifying style options etc., meaning that nested dictionaries are often needed in order to get to a desired option/function argument. The interactive plots produced are web-based, i.e. in the html format. Accordingly, they will by default open in a browser (like jupyter notebook does) or can be viewed inside notebooks. Note however that plotly also supports the export of static gaphics. This can be specifically interesting, as an interactive graphic may be altered by hand and subsequently exported as a static image. 
# 
# The basis of plotly is the ```plotly.graph_objects``` module (imported as ```go```). Conveniently, a higher-level API called ```plotly.express``` is availabe, sparing us "between 5 and 100 times" 
# [$^1$](https://plotly.com/python/plotly-express/) the necessary code, while still maintaining the optionality of including *graph_objects*. However, sometimes it is better to work with `go` only.
# 
# The syntax for plotly express is more similar to seaborn than to matplotlib. Meanwhile, the syntax for plotly *graphic_objects* needs more detail due to the high level of customizability.
# 
# We will now display some of the standard graphics with the default plotly interactivity, starting by importing plotly express and pandas and loading the data.

# In[1]:


import plotly.express as px
import pandas as pd


# In[2]:


dax = pd.read_excel('/users/jan/data/dax.xlsx', engine='openpyxl')
credit_cards = pd.read_csv('/users/jan/data/BankChurners.csv')


# When using the **express** API, the plot function is called as usual. The first argument is the dataframe, containing the variables for the plot. Then follow the axes with the **variables as strings** and finally some customization keywords. Note that a dataframe does not need to be specified, if calling the x (y, z) axis with a pandas Series.
# 
# We will again look at barcharts and histograms first. The respective functions are ```bar()``` and ```histogram()```, where we use the dataframe as first argument. Then we specify the axes arguments ```x=, y=```. 
# 
# In order to make a bar plot showing the counts, we need to create a dataframe with this information first. We use panda's ```groupby()``` followed by ```size()``` before resetting the index to get the counts not as index, but variable.

# In[3]:


plot_df = credit_cards.groupby(by=["Marital_Status"]).size().reset_index(name="count")
plot_df


# We now use the ```px.bar()``` function to create a Figure object in line one. The first argument takes the dataframe, ```x``` and ```y``` the variables we want to plot **as strings**. 
# 
# Additionally, we can set the size of the figure using ```width``` and ```height```.
# 
# The categories are by default ordererd alphabetically.
# 
# Finally, as we have seen for matplotlib, we use fig's ```show()``` method to display the graphic.

# In[4]:


fig = px.bar(data_frame=plot_df, x='Marital_Status', y='count', width=400, height=320)
fig.show()


# We can see that creating a standard plot in plotly already offers interactivity. Hovering the mouse over the plot shows a tool bar at the top. Clicking these symbols allows to zoom in and out or select different data points (not so helpful with histograms). The plot can also be downloaded as .png by clicking the camera symbol on the left.
# 
# Furthermore, we see the **hovering_data** when hovering the mouse over the bars. This hover data will by default show the x and y values of the displayed data. In this case the category and count. We will see shortly how to alter this information. 

# While a histogram is per definition used for numerical data, we can use the ```histogram()``` function for bar charts with the count on the y axis as above. The syntax does not change, we simply substitute ```histogram``` for ```bar```./
# The result will differ slightly, as ```histogram()``` will order the bars by descending count. To create the same graphic as before, we can use the ```update_xaxes()``` method. Note that this method can be chained to the inital call in the first line of the following cell. For better readability however, it is recommended to call the method in a new line. 
# 
# The method's argument to reorder the bars is *categoryorder*, which takes a string as input:
# - 'total de-/ascending': order bars according to their height
# 
# - 'category de-/ascending': order bars alphanumerically by their name
# 
# - 'array': ordered according to the additional *categoryarray* argument, which allows custom ordering
# 
# It has several other arguments, for example to change the axis to logarithmic.

# In[5]:


fig = px.histogram(credit_cards, x='Marital_Status', width=400, height=320)
fig.update_xaxes(categoryorder='array', categoryarray=['Single', 'Married', 'Divorced', 'Unknown'])
fig.show()


# In order to inspect your or someone's figure, you can use `print`. It will show the whole structure of the object and all nested lists, tuples and dictionaries! 

# In[6]:


print(fig)


# ## Colors and Facets
# 
# To change the color (of the bars), we use the ```update_traces()``` method. The ```marker_color``` argument takes a string as argument. This string my be a predefined color, like *black* or *green*, or an rgb code, which we would also have to pass as string: ```rgb(1,1,1)```

# In[7]:


fig = px.histogram(credit_cards, x='Marital_Status', width=400, height=320)
fig.update_traces(marker_color='rgb(12,22,170)')
fig.show()


# Another way to color the markers/bars would be according to a variable. To do so, we use the color argument inside the graphic function call and pass a variable name from the dataframe. Note that the hover information now yields information on the split data. \
# The ```barmode=``` argument specifies, how the differently coloured bars should be displayed. Stacked bars are the default option, ```'group'``` sets the bars next to one another.

# In[8]:


fig = px.histogram(credit_cards, x='Marital_Status', color='Gender', barmode='group', width=400, height=320)
fig.show()


# We can also use variables from the dataframe for splitting one graph into several subplots. The respective keyword is ```facet_col``` (```facet_row``` to split horizontally). The title of the subplots will automatically show which variable was chosen for the split and which category is shown in the plot. 
# 
# Custom colouring for different categories can be achieved by defining an according dictionary. The dictionary needs all available categories of the ```color=``` variable as keys and the desired color as value. Such a dictionary (```col_map```) is defined in the following using different values to define a colour. It is passed to the ```color_discrete_map``` argument.
# 
# Another modification aims at the order of the stack:
# 
# Assuming a platinum card is the most exclusive, followed by gold, silver and blue, we choose this order from top to bottom. We exploit the fact, that the traces are built sequentially by creating an ordered dataframe. We do so by a mapping dictionary (```card_order```) and the ```.map()``` method. 

# In[9]:


col_map = {'Blue': '#069AF3', 'Gold': 'gold', 'Platinum': 'rgb(102,102,102)', 'Silver': 'silver'}
card_order = {'Blue': 0, 'Silver': 1, 'Gold': 2, 'Platinum': 3 }
credit_card_order = credit_cards.copy()
credit_card_order['card_order'] = credit_card_order.Card_Category.map(card_order)


# In[10]:


fig = px.histogram(credit_card_order.sort_values('card_order', ascending=True), x='Education_Level', width=800, height=370, facet_col='Gender', 
                   color='Card_Category', color_discrete_map=col_map)

fig.show()


# Turning to a scatter plot, we introduce and use:
# 
# - ```hover_data``` to display more information from the dataframe in the info boxes when hovering over data points. Note two things regarding the hover information: firstly, the variables to appear have to be supplied inside a list and should be a pandas Series, not a string like for x and y. Secondly, if data point overlap (or are identical) in the displayed x-y-plane, the hover box will only show the information for the "last printed" of those data points.
# 
# - ```size``` to resize the markers according to values of a given variable. The size can also be specified inside ```update_trace``` (see below) to set a constant size of the markers 
# 
# - relabeling the axes with ```labels```: using a dict with the variable name key and the desired label as value, both as strings
# 
# - the ```update_layout()``` method which we use to modify the `hovermode` to display a highlight on the x-axis
# 
# Note the reduced dataframe for less datapoints, to get a better look at the difference in marker size.

# In[11]:


cc_sample = credit_cards.sample(200)   # less data for better visualisation
fig = px.scatter(cc_sample, x='Customer_Age', y='Months_on_book', width=800, height=500,
                 hover_name='Education_Level',
                 hover_data=[cc_sample.Credit_Limit],
                 size = 'Credit_Limit', 
                 labels={'Customer_Age':'Customer Age', 'Months_on_book':'Months on book'})
fig.update_traces(marker=dict(color = 'rgb(0,137,147)'))
fig.update_layout(hovermode='y')
fig.show()


# ## Subplots
# 
# Plotly offers a simple way to create subplots, quite similar to pyplot. With the ```make_subplots``` function, we pass as arguments how many rows and columns we want to display and then use ```add_trace()```. This functions adds a trace, i.e. what will be displayed as a new plot, to fill these allocated slots by specifying the ```row``` and ```col``` arguments with the respective indexes. Note that we use ```graph_objects``` here, which have been imported as ```go```. The syntax for ```go```s changes slightly as the function name starts with a capital letter.
# 
# Some more customization in the example below:
# 
# - `subplot_titles`: list of strings containing the titles of the subplot in row-major ordering (first row (of plots) left to right, then second row...) 
# 
# - ```legend``` inside ```update_layout```: takes a dict as argument for customization of the legend. Customization includes for example:
#     - ```x/y``` as position relative to figure 
#     - `bgcolor` asto change the legend's background colour

# In[12]:


import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = make_subplots(rows=1, cols=2, subplot_titles=['Credit Limit','Avg Open to buy'])

fig.add_trace(go.Histogram(x= credit_cards.Credit_Limit, name='Credit Limit'), row=1, col=1)

fig.add_trace(go.Bar(x=credit_cards.Education_Level.unique(),
                     y=credit_cards.groupby('Education_Level').mean().Avg_Open_To_Buy, name='Avg Open to buy',
                     marker=dict(color='rgba(50,60,110, 1)')),
              row=1, col=2)

fig.update_layout(legend={'x':.2, 'y':.85, 'bgcolor': 'rgb(180,180,181)'})
fig.show()


# Using `add_trace`, we can combine different plots in a subplot. We now use numpy's `.histogram()` function to access the bins and counts and plot them using `go.Bar`. This extra step is necessary, since plotly will not let you access the bins produced when calling the histogram function. 
# 
# We use `go.Scatter` with `mode = lines+markers` to add a **line plot** in order to emphasize the trend.
# 
# We also specify the bar `width` in the call of the bar chart to reduce the spacing.

# In[13]:


import numpy as np

fig = make_subplots(rows=1, cols=1, subplot_titles=['Credit Limit'])

counts, bins = np.histogram(credit_cards.Credit_Limit, bins=15)
fig.add_trace(go.Bar(x=bins,y= counts, name='Avg open to buy', hoverinfo='skip', width=bins[1]-bins[0]),
              row=1, col=1)
fig.add_trace(go.Scatter(x=bins,
                         y=counts,
                         mode='lines+markers',
                         name='Avg open to buy', showlegend=False,
                        marker=dict(color='rgba(204,68,0, 1)')))


fig.update_layout(height=500, width=600, legend={'x':.55, 'y':.96, 'bgcolor': 'rgb(255,255,255)'})
fig.show()


# Note that the same plot could be created outside the subplot environment: Similar to matplotlib, we could have called the functions subsequently!

# Another type of plot, specifically for finance, is the candlestick chart to display the evolution of a stock's price over time. It has a date range on it's x-axis and a 'candlestick' for every (trading) day. This candlestick is basically a boxplot:
# 
#     - the box boundaries show the open and close prices
#     - the whiskers the highest and lowest price for the day 
# 
# This whisker-box is coloured according to the following outcome:
#     
# - if close > open price: green 
# - if close < open price: red
# 
# Plotly includes the `go.Candlestick()` function which takes a date and the four respective prices as arguments.
# This function comes with an advanced tool of interactivity: a rangeslider to select the date range we would like to inspect more closely.
# 
# To disable the slider update the layout `fig.update_layout(xaxis_rangeslider_visible=False)`

# In[14]:


stock_data = pd.read_csv('https://www.dropbox.com/s/inw5s8x4pp0p0kh/historical_data.csv?dl=1')


# In[15]:


fig = go.Figure(go.Candlestick(x=stock_data.Date, open=stock_data.INTC_Open, high=stock_data.INTC_High,
                               low=stock_data.INTC_Low, close=stock_data.INTC_Close))
fig.show()

