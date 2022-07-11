import json
import requests
#from turtle import home
import plotly
import dash_design_kit as ddk
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import plotly.graph_objs as go
import dash_table
import plotly.express as px
import numpy as np
import os
import pandas as pd

app = dash.Dash(__name__)
server = app.server

df = pd.read_csv(
        'https://raw.githubusercontent.com/mcgovernplotly/DinoDashboard/main/DinoData.csv')

Period_list = list(df["Period"].unique())
Period_list.sort()

app.layout = ddk.App(
        [
                ddk.Header(
                        [
                        html.Img(src=app.get_asset_url('trex.png')),
                        ddk.Title("Dino Fossil Data"),
                        ]
                ),
                dbc.Row(
                children=[
                        dbc.Col(
                        dbc.Card(
                                dbc.CardBody(
                                children=[
                                        html.Label('Period', style={'fontSize':30, 'textAlign':'center'}),
                                        dcc.Dropdown(
                                        id='period',
                                        options=[
                                                {"label": i, "value": i} for i in Period_list
                                        ],
                                        value='Late Triassic',
                                        clearable=True,
                                        searchable=True,
                                        ),
                                        html.Div(id="Period-dropdown"),
                                        html.Label('Dino Type', style={'fontSize':30, 'textAlign':'center'}),
                                        dcc.Dropdown(id='display-type', options=[], multi=True, value=[]),
                                ]
                                )
                        ),
                        width=4,
                        ),

                        dcc.Graph(id='display-map', figure={}),
                ],
                ),
        ]
    )



@app.callback(
    Output('display-type', 'options'),
    [Input('period', 'value')],
)
def set_type_options(chosen_type):
        dff = df[df.Period==chosen_type]
        return [{'label':c, 'value':c} for c in sorted(dff.Type.unique())]

@app.callback(
        Output('display-type', 'value'),
        Input('display-type', 'options'),
)
def set_type_value(available_options):
        #displays type values that go into second dropdown?
        return [x['value'] for x in available_options]
@app.callback(
        Output('display-map', 'figure'),
        Input('display-type', 'value'),
        Input('period', 'value')
)
def update_graph(selected_type, selected_period):
        if len(selected_type) == 0:
                return dash.no_update
        else:
                dff = df[(df.Period==selected_period) & (df.Type.isin(selected_type))]

                fig = px.scatter(dff, x='Species', y='Type',
                color= 'Diet',
                size='MillionsYears',
                )
        return fig

if __name__ == "__main__":
    app.run_server(debug=True)