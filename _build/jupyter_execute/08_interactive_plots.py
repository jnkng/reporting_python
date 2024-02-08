#!/usr/bin/env python
# coding: utf-8

# # Interactive Graphics - Plotly
# 
# <span style="font-family:Apple Chancery"><font size="4"> - An interactive graph is worth a thousand static graphs -</font></span>
# 
# So far, we have introduced static plots. An extension to this are interactive plots. Interactivity means for example displaying additional information when hovering the mouse over data points, selecting single traces from the legend or being able to select a value range with a slider. To display time varying effects, animated graphics can be a suitable choice.
# 
# To build such graphics, we will use the package [**plotly**](https://plotly.com). Plotly is based on javascript and uses dictionaries when it comes to specifying style options etc., meaning that nested dictionaries are often needed in order to get to a desired option/function argument. The interactive plots produced are web-based, i.e. in the html format. Accordingly, they will by default open in a browser (like jupyter notebook does) or can be viewed inside notebooks. Note however that plotly also supports the export of static graphics. This can be specifically interesting, as an interactive graphic may be altered by hand and subsequently exported as a static image. 
# 
# The basis of plotly is the ```plotly.graph_objects``` module (imported as ```go```). Conveniently, a higher-level API called ```plotly.express``` is available, sparing us "between 5 and 100 times" 
# [$^1$](https://plotly.com/python/plotly-express/) the necessary code, while still maintaining the optionality of including *graph_objects*. However, sometimes it is better to work with `go` only.
# 
# The syntax for plotly express is more similar to seaborn than to matplotlib. Meanwhile, the syntax for plotly *graphic_objects* needs more detail due to the high level of customizability.
# 
# We will now display some of the standard graphics with the default plotly interactivity, starting by importing plotly express and pandas and loading the data.

# In[1]:


import plotly.express as px
import pandas as pd


# In[2]:


dax = pd.read_excel('data/dax.xlsx', engine='openpyxl')
credit_cards = pd.read_csv('data/BankChurners.csv')


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
# The categories are by default ordered alphabetically.
# 
# Finally, as we have seen for matplotlib, we use fig's ```show()``` method to display the graphic.

# In[4]:


fig = px.bar(data_frame=plot_df, x='Marital_Status', y='count', width=400, height=320)
fig.show()


# We can see that creating a standard plot in plotly already offers interactivity. Hovering the mouse over the plot shows a tool bar at the top. Clicking these symbols allows to zoom in and out or select different data points (not so helpful with histograms). The plot can also be downloaded as .png by clicking the camera symbol on the left.
# 
# Furthermore, we see the **hovering_data** when hovering the mouse over the bars. This hover data will by default show the x and y values of the displayed data. In this case the category and count. We will see shortly how to alter this information. 

# While a histogram is per definition used for numerical data, we can use the ```histogram()``` function for bar charts with the count on the y axis as above. The syntax does not change, we simply substitute ```histogram``` for ```bar```./
# The result will differ slightly, as ```histogram()``` will order the bars by descending count. To create the same graphic as before, we can use the ```update_xaxes()``` method. Note that this method can be chained to the initial call in the first line of the following cell. For better readability however, it is recommended to call the method in a new line. 
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
# The ```barmode=``` argument specifies, how the differently colored bars should be displayed. Stacked bars are the default option, ```'group'``` sets the bars next to one another.

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
# Note the reduced dataframe for less data points, to get a better look at the difference in marker size.

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
                     y=credit_cards.groupby('Education_Level').mean(numeric_only=True).Avg_Open_To_Buy, name='Avg Open to buy',
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


# ## More interactivity - sliders and buttons
# 
# Plotly offers more interactivity than the tools that come with every plot, like hover information or the ability to zoom in. We have seen one example in the range/date slider which comes with candlestick charts. We will now have a look at some more pieces to enhance a graphs interactivity.
# 
# ### Sliders
# 
# Sliders can be used in order to limit a displayed range of values or dates. They can also be used to select different groups in a dataset, similar to a dropdown menu.
# 
# To build sliders, we just need a column with that variable, for example 'Date' from the 'stock_data' dataset.
# 
# We create a figure, add a trace with our scatter plot and then update the layout by providing a nested dictionary for the `xaxis`:
#    - `rangeslider` as key with another dict to set the visbility to True
#    - `type` as key and `'date'` as value
#    
# Note that we also select a range for the xaxis, where we provide the data range simply as string. This will create a default range for the rangeslider when creating the plot. Using the same `range` argument inside the `rangeslider` dict would limit the xaxis of the whole graph to this range.

# In[16]:


fig = go.Figure()
fig.add_trace(
    go.Scatter(x=stock_data.Date, y=stock_data.INTC_Close))

fig.update_layout(
    xaxis=dict(
        rangeslider=dict(visible=True),
        type="date",
        range=["2018-06-30", "2020-05-31"]
    )
)

fig.show()


# A slider can also be used for item/variable selection rather than selecting a range, i.e. similar to a dropdown menu. These sliders update the trace every time it is moved to a different position.
# 
# To set up this kind of slider, we subset the stock_data dataframe for the data of the respective company and add a trace each time.
# 
# Then we define a dictionary to take care of the visibility, here called [`sliders` (doc)](https://plotly.com/python/reference/layout/sliders/#layout-sliders-items-slider-steps-items-step-method), which we pass to `update_layout`. Note that we need to put out `sliders` into a list in order for plotly's `slider` argument to accept it.\
# We nest several dicts where we define how the slider will work:
# - at the first level, we select the `steps` to which we give a list of dicts
#     - the dicts of this list each define a position of the slider
#     - as value, we define `method` to `restyle`, as we need to change the visibility of the traces
#     - we provide a `label` to show on the slider
#     - the `args` keyword, to which we hand a list of dicts, containing a list of booleans as value to `'visible'`. This list corresponds to the three traces created before: display one trace per slider position
# 
# More on `args`: this argument accepts all options/dictionaries, that the plot inside `add_trace` would accept. However, the packing in dicts must be according to the requirements!
# 
# Note that we set the visibility of traces `[1]` and `[2]` to `False` after adding the traces. Otherwise, upon running the code, the initial state would show all three lines.
# 
# We also change the slider's position to appear above the graph by specifying `y` and change font size, slider color  and slider length exemplarily. See the [documentation on sliders](https://plotly.com/python/reference/layout/sliders/) for more possibilities of customization.

# In[17]:


fig = go.Figure()
opens = [el for el in stock_data.columns if '_Open' in el]

for op in opens:
    fig.add_trace(go.Scatter(
        x = stock_data.Date,
        y = stock_data[op],
        mode='lines',
        name = op.split('_')[0],
        marker = dict(color='rgb(23,120,147)')
    ))
fig.data[1].visible=False
fig.data[2].visible=False
    
sliders = [dict(steps=[
    {'method': 'restyle', 'label': 'Intel',
    'args': [{'visible': [True, False, False]}]},
    {'method': 'restyle', 'label': 'Boeing',
    'args': [{'visible': [False, True , False]}]},
    {'method': 'restyle', 'label': 'Microsoft',
    'args': [{'visible': [False, False, True]}]}
],
                y=1.4,
                bgcolor='grey',
                font=dict(size=14),
                lenmode='fraction',
                len=.3
               )]

fig.update_layout(dict(sliders=sliders))


# ### Buttons
# 
# We can include buttons in our plotly graphics to change layout options or the displayed data. In general, this will be similar to creating sliders. 
# 
# To create buttons, we call `update_layout()` and then specify `updatemenus`. To create buttons, we need to set `type="buttons"` and then define a dict with the buttons.
# Here, we create two sets of buttons:
# - to select the company, as in the example above
# - to change the style of the line to dotted and back
# 
# Some parts to which to pay attention:
# - Inside `updatemenus`, the button sets appear in separate dicts
# - `args` for the color dict needs a nested dict, from `line` to `dash`, just like what would be needed in the call of `go.Scatter`
# 
# Let's use the example above, but with buttons instead of sliders for the company and the buttons described above.

# In[18]:


fig = go.Figure()

for op in opens:
    fig.add_trace(go.Scatter(
        x = stock_data.Date,
        y = stock_data[op],
        mode='lines',
        name = op.split('_')[0],
        marker = dict(color='rgb(23,120,147)')
    ))

fig.data[1].visible=False
fig.data[2].visible=False

comp_buttons = [{'method': 'restyle', 'label': 'Intel',
    'args': [{'visible': [True, False, False]}]},
    {'method': 'restyle', 'label': 'Boeing',
    'args': [{'visible': [False, True , False]}]},
    {'method': 'restyle', 'label': 'Microsoft',
    'args': [{'visible': [False, False, True]}]}
            ]

line_buttons = [dict(args=[dict(line=dict(dash=False))],
                    label="reset",
                    method="restyle"),
                 dict(args=[dict(line=dict(dash="dot"))],
                    label="dot",
                    method="restyle")]

fig.update_layout(
    updatemenus=[dict(
                    type="buttons",
                    buttons= comp_buttons),
                dict(
                    type="buttons",
                    buttons= line_buttons,direction="right",
            showactive=True,
            x=-.23,
            xanchor="left",
            y=1.12,
            yanchor="top")
                ])


# #### Time buttons
# 
# Time buttons are of special interest when working with dates. They can be used, in order to limit the displayed data range. However, in contrast to sliders, the range is fixed per button.
# 
# The buttons are part of the *xaxis* and *rangeselector* options:
# In the definition of the dicts, we provide:
# - `count` to set how many steps a button goes back
# - `step` to set the unit of the steps
# - `stepmode` to select whether to go back
#     - exactly 1 year back from last date: `backward` 
#     - start at the beginning of the current period (e.g. back to 01/01 for YTD): `todate`
# - `label` for the text on the buttons

# In[19]:


fig = go.Figure()

for op in opens:
    fig.add_trace(go.Scatter(
        x = stock_data.Date,
        y = stock_data[op],
        mode='lines',
        name = op.split('_')[0],
        marker = dict(color='rgb(23,120,147)')
    ))
fig.data[1].visible=False
fig.data[2].visible=False

comp_buttons = [{'method': 'restyle', 'label': 'Intel',
    'args': [{'visible': [True, False, False]}]},
    {'method': 'restyle', 'label': 'Boeing',
    'args': [{'visible': [False, True , False]}]},
    {'method': 'restyle', 'label': 'Microsoft',
    'args': [{'visible': [False, False, True]}]}
            ]

line_buttons = [dict(args=[dict(line=dict(dash=False))],
                    label="reset",
                    method="restyle"),
                 dict(args=[dict(line=dict(dash="dot"))],
                    label="dot",
                    method="restyle")]

time_buttons =[dict(count= 14, step="day", stepmode= "todate", label="2WTD"),
               dict(count= 3, step="month", stepmode= "todate", label="3MTD"),
               dict(count= 1, step="year", stepmode= "todate", label="YTD"),
               dict(count= 1, step="year", stepmode= "backward", label="1Y"),
               dict(step="all", label="reset")
]
    

fig.update_layout(     
    dict(
         xaxis=dict(
             rangeselector=dict(buttons=time_buttons)
                   )
     ),
    updatemenus=[dict(
                    type="buttons",
                    buttons= comp_buttons),
                dict(
                    type="buttons",
                    buttons= line_buttons,direction="right",
            showactive=True,
            x=-.23,
            xanchor="left",
            y=1.12,
            yanchor="top")]

)


# #### Dropdowns
# 
# Dropdowns may be used when there are many options to select from, i.e. too many to place single buttons, or just instead of buttons for aesthetic reasons.
# 
# Again, the syntax is very similar to before but using `type=dropdown`. Actually, using the example above, we can just substitute the type to be `dropdown` instead of `buttons` for `comp_buttons`in `update_layout`!

# In[20]:


fig = go.Figure()

colors = ['rgb(230,10,19)', 'rgb(223,120,14)', 'rgb(23,12,240)']
for i, op in enumerate(opens):
    fig.add_trace(go.Scatter(
        x = stock_data.Date,
        y = stock_data[op],
        mode='lines',
        name = op.split('_')[0]
    ))
    
comp_buttons = [
    {'method': 'restyle', 'label': 'all',
    'args': [{'visible': [True, True, True]}]},
    {'method': 'restyle', 'label': 'Intel',
    'args': [{'visible': [True, False, False]}]},
    {'method': 'restyle', 'label': 'Boeing',
    'args': [{'visible': [False, True , False]}]},
    {'method': 'restyle', 'label': 'Microsoft',
    'args': [{'visible': [False, False, True]}]}
            ]

line_buttons = [dict(args=[dict(line=dict(dash=False))],
                    label="line",
                    method="restyle"),
                 dict(args=[dict(line=dict(dash="dot"))],
                    label="dot",
                    method="restyle")]

time_buttons =[dict(count= 14, step="day", stepmode= "todate", label="2WTD"),
               dict(count= 3, step="month", stepmode= "todate", label="3MTD"),
               dict(count= 1, step="year", stepmode= "todate", label="YTD"),
               dict(count= 1, step="year", stepmode= "backward", label="1Y"),
               dict(step="all", label="reset")]
    

fig.update_layout(     
    dict(xaxis=dict(rangeselector=dict(buttons=time_buttons))),
    updatemenus=[dict(
                    type="dropdown",
                    buttons= comp_buttons),
                dict(
                    type="buttons",
                    buttons= line_buttons,direction="right",
            showactive=True,
            x=-0.22,
            xanchor="left",
            y=1.12,
            yanchor="top")]
)


# #### Saving as html
# 
# To save a figure, call the `write_html()` method on the figure and provide the path to the desired location as path. The html file can then be viewed using your browser and will work just as in jupyter notebook.
# 

# In[21]:


fig.write_html('plotly.html')


# #### Saving as static image
# 
# Similar to saving as html, to save a static version of the figure, call the `write_image()` method on the Figure object. Again, provide the path to the file as string. Possible formats are, among others, **.pdf** and **.png**
# 
# Note that you need to have additional packages, like kaleido, installed for this export. If this is required by an error message, follow the respective instructions and use your package manager to install.

# In[22]:


fig.write_image('plotly.pdf')
fig.write_image('plotly.png')

