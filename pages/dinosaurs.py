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
Type_list = list(df['Type'].unique())
Type_list.sort()

# this should be cached
all_names_cols = [
    'Name', 'Link', 'Type', 'Diet', 'Period'
]
# all_names = pd.read_sql('SELECT {} FROM "Name" WHERE series_n > 0')
# all_names['Name']= all_names['Link'].apply(get_cover_afterwards)
# all_names['id']=all_names['Name']

# db_table = ddk.DataTable(
#     id='db-table',
#     data=all_names.to_dict('records'),
#     columns=[
#         {"name": colnames_books[i], "id": i} for i in ['title', 'author_name', 'average_rating', 'series_name', 'series_n']
#     ] + [
#         {"name": 'Rating', "id": 'average_rating', "type":'numeric',"format":Format(precision=2, scheme=Scheme.fixed)},
#         {"name": 'book_id_long', "id": 'id'},
#         {"name": 'Cover url', "id": 'cover'}
#     ],
#     hidden_columns = ['id','url'],
#     style_data={'background-color':'white', 'color':'#1a1a82'},
#     filter_action='native',
#     row_selectable='single'
#     )


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
                                        html.Label('Dinosaur Type', style={'fontSize':30, 'textAlign':'center'}),
                                        dcc.Dropdown(
                                        id='dinotype',
                                        options=[
                                                {"label": i, "value": i} for i in Type_list
                                        ],
                                        multi=True,
                                        value= Type_list,
                                        clearable=True,
                                        searchable=True,
                                        ),

                                dbc.CardHeader("Select Dino Name Here"),
                                dcc.Dropdown(
                                    id="name_dropdown",
                                    options=[
                                        {"label": i, "value": i}
                                        for i in list(df['Name'])
                                    ],
                                    clearable=True,
                                    searchable=True,
                                    value="Segisaurus",
                                ),
                                ]
                                )
                        ),
                        width=4,
                        ),
                ],

                ),
                ddk.Row([
                 ddk.Block(id='image_placeholder')
        ]),
                
                ]
        ),

# html.A(
#     href="https://www.twitter.com/username",
#     children=[
#         html.Img(
#             alt="Link to my twitter",
#             src="twitterlogo.png",
#         )
#     ]
# )

# def generate_thumbnail(image):
#     return html.Div([
#         html.A([
#             html.Img(
#                 src = app.get_asset_url(i),
#                 style = {
#                     'height': '40%',
#                     'width': '40%',
#                     'float': 'left',
#                     'position': 'relative',
#                     'padding-top': 0,
#                     'padding-right': 0
#                 }
#             )
#         ], href = 'https://www.google.com'),
#     ])

# images_div = []
# for i in images:
#     images_div.append(generate_thumbnail(i))
# app.layout = html.Div(images_div)

# @app.callback(
#     Output('image_placeholder', 'children'),
#     [Input('name_dropdown', 'value')],
#     prevent_initial_call=True
# )
# def display_cover(row_id) :
#     name_url = all_names.query('id=="{}"'.format(row_id[0])).to_dict('records')[0]['Link']
#     return html.Img(src=name_url)


# def update_output(name_value):
#         return display_image(name_value).unique()

# def display_image(name_value):
#         if len(name_value) == 0:
#                 return dash.no_update
#         else:
#                 dff = df[(df.Link(name_value))]
#                 df2 = list(df['Link'])
#                 fig = html.Div(value=df2.unique)
#                 return df2




    # filter_ = df['Name'].isin(name_value)
    # filtered_df = df[filter_]
    # return filtered_df.formatted

# def set_type_value(available_options):
#         #displays type values that go into second dropdown?
#         # new_df = df1[(df1['region'].isin(town)]
#         return [x['value'] for x in available_options]
# @app.callback(
#         Output('display-scatter', 'figure'),
#         Output('display-map', 'figure'),
#         # Output('total-fossils', 'children'),
#         Input('display-type', 'value'),
#         Input('period', 'value')
# )
# def update_graph(selected_type, selected_period):
#         if len(selected_type) == 0:
#                 return dash.no_update
#         else:
#                 dff = df[(df.Period.isin(selected_period)) & (df.Type.isin(selected_type))]
#                 df3 = dff.groupby(['Latitude', 'Longitude','Period', 'Country'], as_index=False).count()
#                 df3['LatLongTypeCount']=df3['name_old']

#                 fig2 = px.scatter_geo(df3, lat='Latitude', lon='Longitude', color="Period", size='LatLongTypeCount',
#                         hover_name="Country").update_geos(projection_type="orthographic")

#                 fig = px.bar(dff, x='Country',
#                 color= 'Period',
#                 # size='MillionsYears'
#                 )
#         return fig,fig2


if __name__ == "__main__":
    app.run_server(debug=True)