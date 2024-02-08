#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

all_options = {
    'America': ['New York City', 'San Francisco', 'Cincinnati'],
    'Canada': [u'Montréal', 'Toronto', 'Ottawa']
}
app.layout = html.Div([
    dcc.RadioItems(
        id='countries-radio',
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        value='America'
    ),

    html.Hr(),

    dcc.RadioItems(id='cities-radio'),

    html.Hr(),

    html.Div(id='display-selected-values')
])


@app.callback(
    Output('cities-radio', 'options'),
    Input('countries-radio', 'value'))
def set_cities_options(selected_country):
    return [{'label': i, 'value': i} for i in all_options[selected_country]]


@app.callback(
    Output('cities-radio', 'value'),
    Input('cities-radio', 'options'))
def set_cities_value(available_options):
    return available_options[0]['value']


@app.callback(
    Output('display-selected-values', 'children'),
    Input('countries-radio', 'value'),
    Input('cities-radio', 'value'))
def set_display_children(selected_country, selected_city):
    return u'{} is a city in {}'.format(
        selected_city, selected_country,
    )



app.run_server(mode='inline')


# In[ ]:


import pandas as pd
import plotly.express as px


# In[ ]:


df = pd.DataFrame({
    "x": [1,2,1,2],
    "y": [1,2,3,4],
    "customdata": [1,2,3,4],
    "fruit": ["apple", "apple", "orange", "orange"]
})

fig = px.scatter(df, x="x", y="y", color="fruit", custom_data=["customdata"])

fig.update_layout(clickmode='event+select')


# In[11]:


from jupyter_dash import JupyterDash
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

# make a sample data frame with 6 columns
df = pd.DataFrame({"Col " + str(i+1): np.random.rand(30) for i in range(6)})

app.layout = html.Div([
    html.Div(
        dcc.Graph(id='g1', config={'displayModeBar': False}),
        className='four columns'
    ),
    html.Div(
        dcc.Graph(id='g2', config={'displayModeBar': False}),
        className='four columns'
        ),
    html.Div(
        dcc.Graph(id='g3', config={'displayModeBar': False}),
        className='four columns'
    )
], className='row')

def get_figure(df, x_col, y_col, selectedpoints, selectedpoints_local):

    if selectedpoints_local and selectedpoints_local['range']:
        ranges = selectedpoints_local['range']
        selection_bounds = {'x0': ranges['x'][0], 'x1': ranges['x'][1],
                            'y0': ranges['y'][0], 'y1': ranges['y'][1]}
    else:
        selection_bounds = {'x0': np.min(df[x_col]), 'x1': np.max(df[x_col]),
                            'y0': np.min(df[y_col]), 'y1': np.max(df[y_col])}

    # set which points are selected with the `selectedpoints` property
    # and style those points with the `selected` and `unselected`
    # attribute. see
    # https://medium.com/@plotlygraphs/notes-from-the-latest-plotly-js-release-b035a5b43e21
    # for an explanation
    fig = px.scatter(df, x=df[x_col], y=df[y_col], text=df.index)

    fig.update_traces(selectedpoints=selectedpoints,
                      customdata=df.index,
                      mode='markers+text', marker={ 'color': 'rgba(0, 116, 217, 0.7)', 'size': 20 }, unselected={'marker': { 'opacity': 0.3 }, 'textfont': { 'color': 'rgba(0, 0, 0, 0)' }})

    fig.update_layout(margin={'l': 20, 'r': 0, 'b': 15, 't': 5}, dragmode='select', hovermode=False)

    fig.add_shape(dict({'type': 'rect',
                        'line': { 'width': 1, 'dash': 'dot', 'color': 'darkgrey' }},
                       **selection_bounds))
    return fig

# this callback defines 3 figures
# as a function of the intersection of their 3 selections
@app.callback(
    Output('g1', 'figure'),
    Output('g2', 'figure'),
    Output('g3', 'figure'),
    Input('g1', 'selectedData'),
    Input('g2', 'selectedData'),
    Input('g3', 'selectedData')
)
def callback(selection1, selection2, selection3):
    selectedpoints = df.index
    for selected_data in [selection1, selection2, selection3]:
        if selected_data and selected_data['points']:
            selectedpoints = np.intersect1d(selectedpoints,
                [p['customdata'] for p in selected_data['points']])

    return [get_figure(df, "Col 1", "Col 2", selectedpoints, selection1),
            get_figure(df, "Col 3", "Col 4", selectedpoints, selection2),
            get_figure(df, "Col 5", "Col 6", selectedpoints, selection3)]

app.run_server(mode='inline', port=5055)


# In[5]:


dash.callback_context.triggered


# In[ ]:




