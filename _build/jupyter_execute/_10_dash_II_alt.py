#!/usr/bin/env python
# coding: utf-8

# In[1]:


from jupyter_dash import JupyterDash 
import dash_core_components as dcc
import dash_html_components as html


# # Dash - advanced interactivity
# 
# 
# To provide advanced interactivity and reactivity, that is to let new input trigger modified output, we need to provide the content as the result of a function.
# We can have several functions, each modifying one specific element of the UI. To reference elements in the UI and the server part, we give a unique **id** to each element. This id is handed to the respective function to tell it that this is the **input** to be used. The same applies in the reversed direction: by specifying the id of the desired UI element as a function's **output**, the created result is passed to the right address to be displayed. 
# The declaration of what is input and output is done using [decorators](Decorators) and callbacks. This decorator takes the input and output ids as arguments.
# 
# The structure for building an advanced reactive app becomes:
# 
# - create a JupyterDash object
# 
# - define the UI by using the `.layout()` method:
#     - static elements are defined here
#     - every interactive item gets an unique **id** which will identify the element as it is given to the server/UI. For example: An info text, which will not change during the use of the app would not need an id. A button to alter the content must get an id.
# 
# - define the server functions for the content and use the `app.callback()` decorator.
#     - this part will do any calculations or assignments for interactive elements. The output created here also gets an **id** to address it in the UI in order to display it at the desired location. The definition as callback ensures that every time an input changes, the respective function (having this element as input) is run to keep the content of the UI up-to-date, e.g. after clicking a button  
#     
# - the app is run using the `.run_server()` method
# 
#  Note that expensive operations like (down)loading a file should be placed outside the reactive environment, if possible. Else, the operation is triggered and run every time the input changes. For example when working with APIs: Place the request and loading of the data once upfront, before starting the app. Otherwise, the request will be sent unnecessarily for every change in input and soon the limit of requests per day is reached. In general, don't change global variables inside the reactive environment.

# To use the decorators and link input and output between server and UI, we need to import the functions `Input` and `Output` from `dash.dependencies`. We call these functions (imported from `dash.dependencies`) as arguments of `app.callback()`.
# 
# Then, as arguments to `Input` and `Output` we need to specify the `component_id` and the `component_property`. The respective ids must be identical to the ones used in the UI. The properties vary, dependent on what the output of the function is:
# 
# <ins>Output</ins>:
# - `'children'`: to return text to the `'children'` argument of html elements
# 
# - `'figure'`: to return a plotly graphic to `dcc.Graph()` 
# 
# - `'value'`: to return a standard value to an interactive element
# 
# - (`'options'`: to create options for interactive elements like dropdowns, dependent on earlier selection)
# 
# <ins>Input</ins>:
# 
# - `'value'`: use the value of an element as argument, e.g. an entered number
# 
# - `'n_clicks'`: returns the number a `html.Button` has been clicked 
# 
# - (`'options'`: use options from an interactive element)

# Let's look at a first example.
# 

# In[2]:


from dash.dependencies import Input, Output

app = JupyterDash('myFirstReactive')

app.layout = html.Div([
    html.P(children="Input: "),
    dcc.Input(id='inum', value='', type='number'),
    html.P(id='outext')
])

@app.callback(
    Output(component_id='outext', component_property='children'),
    Input(component_id='inum', component_property='value')
)
def div_outext(num):
    return f'times two: {num*2}'

app.run_server(mode='inline')


# First, we instantiate the JupyterDash object.
# 
# Then, we modify the <ins>layout</ins> to contain the following elements inside the main `Div`:
# 
# - a `P` element saying 'Input:' $\rightarrow$ static, no need for an **id**
# 
# - a `dcc.Input()` with a unique id, a default value (empty string, otherwise it would say 'None') and the `type` of the input to create the according field type in the UI
# 
# - another `P` element with *only* an **id** and no children
# 
# Then, we define the <ins>server</ins> function to create the output: the function per se takes one argument and creates a string containing it after being multiplied by two.
# 
# This function, however, gets decorated with `app.callback()`. This is where the linking between the function and the UI happens. 
# `app.callback()` gets `Output()` and `Input()` as arguments. Each of which have arguments `component_id=` and `component_property=`:
# 
# - to `Output`, we pass the id of the second `P` element, which in the definition of the layout did not have a `children` argument. This omission becomes clearer when we see that we now pass `component_property='children'`. In prose, this means: Take the result of the decorated function and supply it to the UI element with `component_id='outext'` as a `children` element.
# 
# - to `Input` we pass the `component_id='inum'` and `component_property='value'`. This means, that the value of the input variable 'inum', defined by the input field `dcc.Input()` should be taken as the input to the decorated function, where it can be processed.
# 
# Every time we change the input by entering a number or clicking the arrows in the input field, the function gets called and the output is updated.
# 
# Note that when starting an app, dash will run all available callbacks. This is why we omitted the `children` in the definition of the second `P` element when defining the layout: Any value we would enter here, would instantly be overwritten by the callback.

# We will slightly alter this first example to demonstrate, that several inputs and outputs can be used by one function. 

# In[3]:


from dash.dependencies import Input, Output

app = JupyterDash()

app.layout = html.Div([
    html.Div(["Enter first and last name: ",
    dcc.Input(id='fname_i', value='otto', type='text'),
    dcc.Input(id='lname_i', value='renner', type='text')]),
    html.Br(),
    html.Div([html.P(id='fname_o', style={'float': 'left'}),
    html.P(id='lname_o', style={'float': 'left','marginLeft': 4})] )
])
    
@app.callback(
    Output(component_id='fname_o', component_property='children'),
    Output(component_id='lname_o', component_property='children'),
    Input(component_id='fname_i', component_property='value'),
    Input(component_id='lname_i', component_property='value')
)
def div_outext(fname, lname):
    if fname:
        return fname[::-1], lname[::-1]
    
app.run_server(mode='inline')


# To use several Inputs, we need to look at the order of the `Input`s in the callback. It must match the order of the arguments in the decorated function, i.e. the first `Input` will be passed as the first argument to the function. In the example above, `fname_i` is passed to the function as the `fname` argument.
# 
# For several Outputs, the same applies: the order of `Output`s in the callback must match the order after `return`.

# Dash includes elements knwon from plotly, like sliders and buttons. They are implemented in `dcc`. Some are also part of `html` like `html.Button` (having the `n_clicks` attribute).
# 
# To use interactive elements, we must take their input and pass it to a function by the callback decorator. There, we can use the value to return updated content of an element. 
# 
# In the following example, we will use a slider input to filter and return the copy(!) of a global dataframe. 

# In[53]:


import pandas as pd
import datetime as dt
import plotly.express as px
df = pd.read_csv('data/dji_100_days.csv', index_col=0)
df.date = pd.to_datetime(df.date)
df = df[df.date.dt.year == 2021]
df['month'] = [el.month for el in df.date]


# In[87]:


pd.to_datetime(6).strftime("%b")


# In[86]:


{n+1: pd.to_datetime(n).strftime("%b") for n in range(max(df.month))}


# In[81]:


from dash.dependencies import Input, Output

app = JupyterDash()

months = {}
app.layout = html.Div([
    dcc.Slider(
        id='comp_slider',
        min= min(df.month),
        max= max(df.month),
        marks= {n: str(n) for n in range(max(df.month))},
        value=1
        ),
    dcc.Dropdown(id='company_dd',
                options = [{'label': i, 'value': i} for i in df.symbol.unique()], value=df.symbol.unique()[0]),
    dcc.Graph(id='outgraph')
])

@app.callback(
    Output('outgraph', 'figure'),
    Input('comp_slider', 'value'),
    Input('company_dd', 'value')
)
def make_outgraph(month, sym):
    dftemp = df[df.symbol == sym]
    dftemp = dftemp[dftemp.month == month]
    fig = px.line(dftemp, x='date', y='open')
    return fig

app.run_server(mode='inline', port=8051)


# In[63]:


df[df.month==4]


# In[ ]:


@app.callback(
    Output(component_id='fname_o', component_property='children'),
    Output(component_id='lname_o', component_property='children'),
    Input(component_id='fname_i', component_property='value'),
    Input(component_id='lname_i', component_property='value')
)
def div_outext(fname, lname):
    if fname:
        return fname[::-1], lname[::-1]
    
app.run_server(mode='inline')


# In[ ]:


app.callback_map


# (Decorators)=
# ## Decorators
# 
# Functions which expand the functionality of another function are called decorators (or wrappers). However, these decorators do not change the underlying function, i.e. the one that *gets decorated*. 
# 
# This is possible since functions, just like anything in python, are objects and can get passed as arguments to other functions (we have seen this in the context of callbacks). Furthermore, functions may be defined inside other functions, using the the same syntax as usual.
# 
# Let's look at a simple example of a function and a wrapper/decorator.
# The initial function `text_to_wrap` simply prints a string. The decorator returns the `wrapper()` function, which adds a line above and below the text, when printing.

# In[ ]:


def text_to_wrap():
    print('my text')
    
text_to_wrap()


# In[ ]:


def emphasize_decorator(func):
    def wrapper():
        print('##################')
        func()
        print('!!!!!!!!!!!!!!!!!!')
    return wrapper


# To decorate `text_to_wrap`, we can assign the decorator with '`text_to_wrap`' as argument to the initial function name. Note that we pass the function name without parentheses.

# In[ ]:


text_to_wrap = emphasize_decorator(text_to_wrap)


# In[ ]:


text_to_wrap()


# To shorten this procedure, python includes a special syntax for decorators. With `@emphasize_decorator` (no parentheses!) before the definition of the inner function, we can achieve the same behaviour.

# In[ ]:


# emphasize_decorator is being treated as already defined

@emphasize_decorator
def print_greeting():
    print('Hello')


# In[ ]:


print_greeting()


# We see, that `print_greeting()` has initially been defined to print 'Hello'. With the decorator call using `@`, however, we have decorated it on the fly to add the emphasis lines around the text from `emphasize_decorator()`. Furthermore, decorators may be chained by subsequent calls of the decorator functions with the same `@`-syntax before the definition of the inner function.  

# To pass arguments through the decorator, we can use `*args` and `**kwargs` as placeholder for an arbitrary number of positional arguments and keyword arguments. Note that this is not unique for decorators, but can be used for the definition of any function! We will now update the first two examples from above:
#     - `text_to_wrap` will get two arguments to print
#     - `wrapper` inside `emphasize_decorator` will get the placeholders in it's definition 

# In[ ]:


def emphasize_decorator(func):
    def wrapper(*args, **kwargs):
        print('##################')
        func(*args, **kwargs)
        print('!!!!!!!!!!!!!!!!!!')
    return wrapper


# In[ ]:


@emphasize_decorator
def text_to_wrap(w1, w2):
    print(f"{w1}\n{w2}")


# In[ ]:


text_to_wrap('line1', 'line2')


# This is what dash does with the functions defined in the server part: These functions get wrapped to be linked automatically to the UI and to get called every time, the respective input changes.

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


import dash
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State

cars_df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/imports-85.csv')
# Build parcats dimensions
categorical_dimensions = ['body-style', 'drive-wheels', 'fuel-type']
dimensions = [dict(values=cars_df[label], label=label) for label in categorical_dimensions]
# Build colorscale.
color = np.zeros(len(cars_df), dtype='uint8')
colorscale = [[0, '#167b7e'], [1, '#4b3268']]


def build_figure():
    fig = go.Figure(
        data=[
            go.Scatter(x=cars_df.horsepower, y=cars_df['highway-mpg'],
                       marker={'color': 'gray'}, mode='markers', selected={'marker': {'color': 'firebrick'}},
                       unselected={'marker': {'opacity': 0.4}}),
            go.Parcats(
                domain={'y': [0, 0.4]}, dimensions=dimensions,
                line={'colorscale': colorscale, 'cmin': 0,
                      'cmax': 1, 'color': color, 'shape': 'hspline'})
        ])
    fig.update_layout(
        height=800,
        xaxis={'title': 'Horsepower'},
        yaxis={'title': 'MPG', 'domain': [0.6, 1]},
        dragmode='lasso',
        hovermode='closest',
        # plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        autosize=False,
        bargap=0.35,
        font={"family": "Questrial", "size": 10})
    return fig


app =JupyterDash(prevent_initial_callbacks=True)
app.layout = html.Div([dcc.Graph(figure=build_figure(), id="graph")])


@app.callback(Output("graph", "figure"), [Input("graph", "selectedData"), Input("graph", "clickData")],
              [State("graph", "figure")])
def update_color(selectedData, clickData, fig):
    selection = None
    # Update selection based on which event triggered the update.
    trigger = dash.callback_context.triggered[0]["prop_id"]
    if trigger == 'graph.clickData':
        selection = [point["pointNumber"] for point in clickData["points"]]
    if trigger == 'graph.selectedData':
        selection = [point["pointIndex"] for point in selectedData["points"]]
    # Update scatter selection
    fig["data"][0]["selectedpoints"] = selection
    # Update parcats colors
    new_color = np.zeros(len(cars_df), dtype='uint8')
    new_color[selection] = 1
    fig["data"][1]["line"]["color"] = new_color
    return fig



app.run_server()


# In[ ]:


say_whee()


# In[ ]:




