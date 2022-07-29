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
from dash import dash_table
import plotly.express as px
import numpy as np
import os
import pandas as pd
from app import app
import plotly.graph_objects as go

# app = dash.Dash(__name__)
# server = app.server

dash.register_page(__name__, path='/')

df = pd.read_csv(
        'https://raw.githubusercontent.com/mcgovernplotly/DinoDashboard/main/DinoData.csv')

Period_list = list(df["Period"].unique())
Period_list.sort()
# df2 = df.groupby(['Latitude', 'Longitude','Period'], as_index=False).count()
# df2['LatLongPeriodCount']=df2['name_old']
# df3 = df.groupby(df['Period','Type'], as_index=False)
#df3['LatLongTypeCount']=df3['name_old']
Type_list = list(df["Type"].unique())
totalFossilsFounds = len(df.axes[0])

# fig = px.scatter_geo(df, lat='Latitude', lon='Longitude', color="Country",
#                      hover_name="Country",
#                      projection="mercator",
#                      )


layout = ddk.App(
        [
                ddk.Header(
                        [
                        ddk.Logo(src=app.get_asset_url('trex.png')),
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
                                        multi=True,
                                        value= Period_list,
                                        clearable=True,
                                        searchable=True,
                                        ),
                                        html.Div(id="Period-dropdown"),
                                        html.Label('Dino Type', style={'fontSize':30, 'textAlign':'center'}),
                                        dcc.Dropdown(id='display-type', options=[], multi=True, value=[]),
                                        
                                ]
                                )
                        ),
                        width=8,
                        ),

                        ddk.Card(
                        width=24,
                        children=[
                                ddk.CardHeader(title='Total Fossils Found Across All Periods'),
                                ddk.DataCard(value=totalFossilsFounds,
                                        style={'width':'fit-content'}),
                        ]
                        ),
                        # ddk.Card(
                        # width=24,
                        # children=[
                        #         ddk.CardHeader(title='Total Fossils Found'),
                        #         ddk.DataCard(
                        #                 id='total-fossils',
                        #                 value='',
                        #                 style={'width':'fit-content'}),
                        # ]
                        # ),

                        # ddk.Card(
                        # width=40,
                        # children=[
                        #         dcc.Graph(figure=px.scatter_geo(df2, lat='Latitude', lon='Longitude', color="Period", size='LatLongPeriodCount',
                        #         hover_name="Country").update_geos(projection_type="orthographic")),
                        # ],
                        # ),
                        ddk.Card(
                        width=43,
                        children=[
                                ddk.CardHeader(title='Which Country Fossils Were Found'),
                                dcc.Graph(id='display-map', figure={}),
                        ],),
                        ddk.Card(
                        width=56,
                        children=[
                                ddk.CardHeader(title='Total Found by Country'),
                                ddk.Graph(id='display-scatter', figure={}),
                        ],
                        ),
                        # px.scatter(df, x="MillionsYears", y=len(df.axes[0]), color="Period"),
                ],
                ),
                
                ]
        ),


@app.callback(
    Output('display-type', 'options'),
    [Input('period', 'value')],
)
def set_type_options(chosen_type):
        dff = df[df['Period'].isin(chosen_type)]
        #df.drop_duplicates(subset='brand')
        return [{'label':c, 'value':c} for c in dff['Type'].unique()]

@app.callback(
        Output('display-type', 'value'),
        Input('display-type', 'options'),
)
def set_type_value(available_options):
        return [x['value'] for x in available_options]
@app.callback(
        Output('display-scatter', 'figure'),
        Output('display-map', 'figure'),
        # Output('total-fossils', 'children'),
        Input('display-type', 'value'),
        Input('period', 'value')
)
def update_graph(selected_type, selected_period):
        if len(selected_type) == 0:
                return dash.no_update
        else:
                dff = df[(df.Period.isin(selected_period)) & (df.Type.isin(selected_type))]
                df3 = dff.groupby(['Latitude', 'Longitude','Period', 'Country'], as_index=False).count()
                df3['LatLongTypeCount']=df3['name_old']

                fig2 = px.scatter_geo(df3, lat='Latitude', lon='Longitude', color="Period", size='LatLongTypeCount',
                        hover_name="Country").update_geos(projection_type="orthographic")

                fig = px.bar(dff, x='Country',
                color= 'Period',
                # size='MillionsYears'
                )
        return fig,fig2
# def update_cards(selected_period):
#         dff = df[(dff.Type.isin(selected_period))]
#         fig = ddk.Card(value='Name')
#         return fig


if __name__ == "__main__":
    app.run_server(debug=True)