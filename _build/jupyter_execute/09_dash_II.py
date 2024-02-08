#!/usr/bin/env python
# coding: utf-8

# In[2]:


from jupyter_dash import JupyterDash 
import dash_core_components as dcc
import dash_html_components as html


# # Dash - advanced interactivity
# 
# dependencies!
# 
# To provide advanced interactivity and reactivity, we need to provide the content as a function. Dash then makes use of [decorators](Decorators) and callbacks:
# 
# - decorators link the functions to the input and output of the UI
# 
# - a callback ensures that every time an input changes (the element referenced with its **id**), the respective function is run to keep the content of the UI up-to-date, e.g. for a new selection of data points, or after clicking a button, etc.  
# 
# The structure for building an advanced app is:
# - create a JupyterDash object
# 
# - define the UI by using the `.layout()` method:
#     - static elements are defined here
#     - every interactive item gets an unique **id** which will identify the element as it is given to the server/UI. For example: An info text, which will not change during the use of the app would not need an id. A button to alter something must get an id.
# 
# - define the server functions for the content and use the `app.callback` decorator (see [](Decorators))
#     - this part will do any calculations or assignments for interactive elements. The output created here also gets an **id** to address it in the UI in order to display it
#     
# - the app is run using the `.run_server()` method
# 
# 

# 
# 
# To use the decorators and link input and output for server and UI, we need to import the respective functions from `dash.dependencies`.

# In[4]:


from dash.dependencies import Input, Output

app = JupyterDash('test')

app.layout = html.Div([
    html.H6("Change the value in the text box to see callbacks in action!"),
    html.Div(children=["Input: ",
              dcc.Input(id='my-input', value='initial value', type='text')]),
    html.Br(),
    html.Div(id='my-output'),

])

@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return f'Output: {input_value}'

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




