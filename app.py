# In[]:
# Import required libraries

import os
import pickle
import copy
import datetime as dt

import pandas as pd
from flask import Flask
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

# Multi-dropdown options
from controls import COUNTIES, WELL_STATUSES, WELL_TYPES, WELL_COLORS


# In[]:
# Create app

server = Flask(__name__)
server.secret_key = os.environ.get('secret_key', 'secret')
app = dash.Dash(__name__, server=server)
app.css.append_css({'external_url': 'https://rawgit.com/chriddyp/0247653a7c52feb4c48437e1c1837f75/raw/a68333b876edaf62df2efa7bac0e9b3613258851/dash.css'})  # noqa: E501

# Create controls
county_options = [{'label': str(COUNTIES[county]), 'value': str(county)}
                  for county in COUNTIES]

well_status_options = [{'label': str(WELL_STATUSES[well_status]),
                        'value': str(well_status)}
                       for well_status in WELL_STATUSES]

well_type_options = [{'label': str(WELL_TYPES[well_type]),
                      'value': str(well_type)}
                     for well_type in WELL_TYPES]

# Load data
df = pd.read_csv('data/wellspublic.csv')
df['Date_Well_Completed'] = pd.to_datetime(df['Date_Well_Completed'])
df = df[df['Date_Well_Completed'] > dt.datetime(1960, 1, 1)]

trim = df[['API_WellNo', 'Well_Type', 'Well_Name']]
trim.index = trim['API_WellNo']
dataset = trim.to_dict(orient='index')

points = pickle.load(open("data/points.pkl", "rb"))

# Create global chart template
mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w'  # noqa: E501

layout = dict(
    autosize=True,
    height=500,
    font=dict(family="Overpass", color='#CCCCCC'),
    titlefont=dict(color='#CCCCCC', size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor="#191A1A",
    paper_bgcolor="#020202",
    legend=dict(font=dict(size=11), orientation='h'),
    title='Satellite Overview',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="dark",
        center=dict(
            lon=-78.05,
            lat=42.54
        ),
        zoom=7,
    )
)


# In[]:
# Create app layout
app.layout = html.Div(
    [
        html.Img(
            src='https://raw.githubusercontent.com/plotly/oil-and-gas/master/data/dash-logo%20copy.png?token=AK-nZOdj_s00FsenSnDL00XCBQkubgljks5ZTYlzwA%3D%3D',  # noqa: E501
            style={'width': '4%', 'float': 'left'}
        ),
        html.H2(
            'New York Oil and Gas | Production Overview',
            style={'width': '96%', 'text-align': 'left', 'float': 'left'}
        ),
        html.H5(
            '',
            id='well_text',
            style={'width': '20%', 'float': 'left'}
        ),
        html.H5(
            '',
            id='production_text',
            style={'width': '60%', 'text-align': 'center', 'float': 'left'}
        ),
        html.H5(
            '',
            id='year_text',
            style={'width': '20%', 'text-align': 'right', 'float': 'left'}
        ),
        html.Div(
            [
                html.P('Filter by construction date (or select range in histogram):'),  # noqa: E501
                dcc.RangeSlider(
                    id='year_slider',
                    min=1960,
                    max=2017,
                    value=[1990, 2010]
                ),
            ],
            style={'margin-top': '20'}
        ),
        html.Div(
            [
                html.P('Filter by well status:'),
                dcc.RadioItems(
                    id='well_status_selector',
                    options=[
                        {'label': 'All ', 'value': 'all'},
                        {'label': 'Active only ', 'value': 'active'},
                        {'label': 'Customize ', 'value': 'custom'}
                    ],
                    value='active',
                    labelStyle={'display': 'inline-block'}
                ),
                dcc.Dropdown(
                    id='well_statuses',
                    options=well_status_options,
                    multi=True,
                    value=[]
                ),
            ],
            style={'width': '49%', 'display': 'inline-block',
                   'margin-bottom': '20'}
        ),
        html.Div(
            [
                html.P('Filter by well type:'),
                dcc.RadioItems(
                    id='well_type_selector',
                    options=[
                        {'label': 'All ', 'value': 'all'},
                        {'label': 'Productive only ', 'value': 'productive'},
                        {'label': 'Customize ', 'value': 'custom'}
                    ],
                    value='productive',
                    labelStyle={'display': 'inline-block'}
                ),
                dcc.Dropdown(
                    id='well_types',
                    options=well_type_options,
                    multi=True,
                    value=list(WELL_TYPES.keys()),
                ),
            ],
            style={'width': '49%', 'float': 'right',
                   'display': 'inline-block', 'margin-bottom': '20'}
        ),
        html.Div([
            html.Div(
                [
                    dcc.Graph(id='main_graph')
                ],
                style={'width': '66.5%', 'display': 'inline-block'}
            ),
            html.Div(
                [
                    dcc.Graph(id='individual_graph')
                ],
                style={'width': '33%', 'float': 'right',
                       'display': 'inline-block'}
            ),
        ]),
        html.Div([
            html.Div(
                [
                    dcc.Graph(id='count_graph')
                ],
                style={'width': '33%', 'display': 'inline-block'}
            ),
            html.Div(
                [
                    dcc.Graph(id='pie_graph')
                ],
                style={'width': '33%', 'display': 'inline-block',
                       'margin-left': '0.5%'}
            ),
            html.Div(
                [
                    dcc.Graph(id='aggregate_graph')
                ],
                style={'width': '33%', 'float': 'right',
                       'display': 'inline-block'}
            ),
            dcc.Checklist(
                id='lock_selector',
                options=[
                    {'label': 'Lock camera', 'value': 'locked'}
                ],
                values=[],
                labelStyle={'position': 'relative', 'z-index': '2',
                            'top': '-1000px', 'left': '35px',
                            'color': '#CCCCCC'}
            )
        ]),
    ],
    className='ten columns offset-by-one'
)


# In[]:
# Helper functions

def filter_dataframe(df, well_statuses, well_types, year_slider):
    dff = df[df['Well_Status'].isin(well_statuses)
             & df['Well_Type'].isin(well_types)
             & (df['Date_Well_Completed'] > dt.datetime(year_slider[0], 1, 1))
             & (df['Date_Well_Completed'] < dt.datetime(year_slider[1], 1, 1))]
    return dff


def fetch_individual(api):
    try:
        points[api]
    except:
        return None, None, None, None

    index = list(range(min(points[api].keys()), max(points[api].keys()) + 1))
    gas = []
    oil = []
    water = []

    for year in index:
        try:
            gas.append(points[api][year]['Gas Produced, MCF'])
        except:
            gas.append(0)
        try:
            oil.append(points[api][year]['Oil Produced, bbl'])
        except:
            oil.append(0)
        try:
            water.append(points[api][year]['Water Produced, bbl'])
        except:
            water.append(0)

    return index, gas, oil, water


def fetch_aggregate(selected, year_slider):

    index = list(range(max(year_slider[0], 1985), 2016))
    gas = []
    oil = []
    water = []

    for year in index:
        count_gas = 0
        count_oil = 0
        count_water = 0
        for api in selected:
            try:
                count_gas += points[api][year]['Gas Produced, MCF']
            except:
                pass
            try:
                count_oil += points[api][year]['Oil Produced, bbl']
            except:
                pass
            try:
                count_water += points[api][year]['Water Produced, bbl']
            except:
                pass
        gas.append(count_gas)
        oil.append(count_oil)
        water.append(count_water)

    return index, gas, oil, water


# In[]:
# Create callbacks

# Radio -> multi
@app.callback(Output('well_statuses', 'value'),
              [Input('well_status_selector', 'value')])
def display_status(selector):
    if selector == 'all':
        return list(WELL_STATUSES.keys())
    elif selector == 'active':
        return ['AC']
    else:
        return []


# Radio -> multi
@app.callback(Output('well_types', 'value'),
              [Input('well_type_selector', 'value')])
def display_type(selector):
    if selector == 'all':
        return list(WELL_TYPES.keys())
    elif selector == 'productive':
        return ['GD', 'GE', 'GW', 'IG', 'IW', 'OD', 'OE', 'OW']
    else:
        return []


# Slider -> count graph
@app.callback(Output('year_slider', 'value'),
              [Input('count_graph', 'selectedData')])
def update_year_slider(count_graph_selected):

    if count_graph_selected is None:
        return [1990, 2010]
    else:
        nums = []
        for point in count_graph_selected['points']:
            nums.append(int(point['pointNumber']))

        return [min(nums) + 1960, max(nums) + 1961]


# Selectors -> well text
@app.callback(Output('well_text', 'children'),
              [Input('well_statuses', 'value'),
               Input('well_types', 'value'),
               Input('year_slider', 'value')])
def update_well_text(well_statuses, well_types, year_slider):

    dff = filter_dataframe(df, well_statuses, well_types, year_slider)
    return "No of Wells: {}".format(dff.shape[0])


# Selectors -> production text
@app.callback(Output('production_text', 'children'),
              [Input('well_statuses', 'value'),
               Input('well_types', 'value'),
               Input('year_slider', 'value')])
def update_production_text(well_statuses, well_types, year_slider):

    dff = filter_dataframe(df, well_statuses, well_types, year_slider)
    selected = dff['API_WellNo'].values
    index, gas, oil, water = fetch_aggregate(selected, year_slider)

    def human_format(num):
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        # add more suffixes if you need them
        return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

    return "Gas: {} mcf | Oil: {} bbl | Water: {} bbl".format(
        human_format(sum(gas)),
        human_format(sum(oil)),
        human_format(sum(water))
    )


# Slider -> year text
@app.callback(Output('year_text', 'children'),
              [Input('year_slider', 'value')])
def update_year_text(year_slider):
    return "{} | {}".format(year_slider[0], year_slider[1])


# Selectors -> main graph
@app.callback(Output('main_graph', 'figure'),
              [Input('well_statuses', 'value'),
               Input('well_types', 'value'),
               Input('year_slider', 'value')],
              [State('lock_selector', 'values'),
               State('main_graph', 'relayoutData')])
def make_main_figure(well_statuses, well_types, year_slider,
                     selector, main_graph_layout):

    dff = filter_dataframe(df, well_statuses, well_types, year_slider)

    traces = []
    for well_type, dfff in dff.groupby('Well_Type'):
        trace = dict(
            type='scattermapbox',
            lon=dfff['Surface_Longitude'],
            lat=dfff['Surface_latitude'],
            text=dfff['Well_Name'],
            customdata=dfff['API_WellNo'],
            name=WELL_TYPES[well_type],
            marker=dict(
                size=4,
                opacity=0.6,
                color=WELL_COLORS[well_type]
            )
        )
        traces.append(trace)

    if (main_graph_layout is not None and 'locked' in selector):

        lon = float(main_graph_layout['mapbox']['center']['lon'])
        lat = float(main_graph_layout['mapbox']['center']['lat'])
        zoom = float(main_graph_layout['mapbox']['zoom'])
        layout['mapbox']['center']['lon'] = lon
        layout['mapbox']['center']['lat'] = lat
        layout['mapbox']['zoom'] = zoom
    else:
        lon = -78.05
        lat = 42.54
        zoom = 7

    figure = dict(data=traces, layout=layout)
    return figure


# Main graph -> individual graph
@app.callback(Output('individual_graph', 'figure'),
              [Input('main_graph', 'hoverData')])
def make_individual_figure(main_graph_hover):

    layout_individual = copy.deepcopy(layout)

    if main_graph_hover is None:
        main_graph_hover = {'points': [{'curveNumber': 4,
                                        'pointNumber': 569,
                                        'customdata': 31101173130000}]}

    chosen = [point['customdata'] for point in main_graph_hover['points']]
    index, gas, oil, water = fetch_individual(chosen[0])

    if index is None:
        annotation = dict(
            text='No data available',
            x=0.5,
            y=0.5,
            align="center",
            showarrow=False,
            xref="paper",
            yref="paper"
        )
        layout_individual['annotations'] = [annotation]
        data = []
    else:
        data = [
            dict(
                type='scatter',
                mode='lines+markers',
                name='Gas Produced (mcf)',
                x=index,
                y=gas,
                line=dict(
                    shape="spline",
                    smoothing=2,
                    width=1,
                    color='#fac1b7'
                ),
                marker=dict(symbol='diamond-open')
            ),
            dict(
                type='scatter',
                mode='lines+markers',
                name='Oil Produced (bbl)',
                x=index,
                y=oil,
                line=dict(
                    shape="spline",
                    smoothing=2,
                    width=1,
                    color='#a9bb95'
                ),
                marker=dict(symbol='diamond-open')
            ),
            dict(
                type='scatter',
                mode='lines+markers',
                name='Water Produced (bbl)',
                x=index,
                y=water,
                line=dict(
                    shape="spline",
                    smoothing=2,
                    width=1,
                    color='#92d8d8'
                ),
                marker=dict(symbol='diamond-open')
            )
        ]
        layout_individual['title'] = 'Individual Production: ' + dataset[chosen[0]]['Well_Name']  # noqa: E501

    figure = dict(data=data, layout=layout_individual)
    return figure


# Selectors, main graph -> aggregate graph
@app.callback(Output('aggregate_graph', 'figure'),
              [Input('well_statuses', 'value'),
               Input('well_types', 'value'),
               Input('year_slider', 'value'),
               Input('main_graph', 'hoverData')])
def make_aggregate_figure(well_statuses, well_types, year_slider,
                          main_graph_hover):

    layout_aggregate = copy.deepcopy(layout)

    if main_graph_hover is None:
        main_graph_hover = {'points': [{'curveNumber': 4, 'pointNumber': 569,
                                        'customdata': 31101173130000}]}

    chosen = [point['customdata'] for point in main_graph_hover['points']]
    well_type = dataset[chosen[0]]['Well_Type']
    dff = filter_dataframe(df, well_statuses, well_types, year_slider)

    selected = dff[dff['Well_Type'] == well_type]['API_WellNo'].values
    index, gas, oil, water = fetch_aggregate(selected, year_slider)

    data = [
        dict(
            type='scatter',
            mode='lines',
            name='Gas Produced (mcf)',
            x=index,
            y=gas,
            line=dict(
                shape="spline",
                smoothing="2",
                color='#F9ADA0'
            )
        ),
        dict(
            type='scatter',
            mode='lines',
            name='Oil Produced (bbl)',
            x=index,
            y=oil,
            line=dict(
                shape="spline",
                smoothing="2",
                color='#849E68'
            )
        ),
        dict(
            type='scatter',
            mode='lines',
            name='Water Produced (bbl)',
            x=index,
            y=water,
            line=dict(
                shape="spline",
                smoothing="2",
                color='#59C3C3'
            )
        )
    ]
    layout_aggregate['title'] = 'Aggregate Production: ' + WELL_TYPES[well_type]  # noqa: E501

    figure = dict(data=data, layout=layout_aggregate)
    return figure


# Selectors, main graph -> pie graph
@app.callback(Output('pie_graph', 'figure'),
              [Input('well_statuses', 'value'),
               Input('well_types', 'value'),
               Input('year_slider', 'value')])
def make_pie_figure(well_statuses, well_types, year_slider):

    layout_pie = copy.deepcopy(layout)

    dff = filter_dataframe(df, well_statuses, well_types, year_slider)

    selected = dff['API_WellNo'].values
    index, gas, oil, water = fetch_aggregate(selected, year_slider)

    aggregate = dff.groupby(['Well_Type']).count()

    data = [
        dict(
            type='pie',
            labels=['Gas', 'Oil', 'Water'],
            values=[sum(gas), sum(oil), sum(water)],
            name='Production Breakdown',
            text=['Total Gas Produced (mcf)', 'Total Oil Produced (bbl)', 'Total Water Produced (bbl)'],  # noqa: E501
            hoverinfo="text+value+percent",
            textinfo="label+percent+name",
            hole=0.5,
            marker=dict(
                colors=['#fac1b7', '#a9bb95', '#92d8d8']
            ),
            domain={"x": [0, .45], 'y':[0.2, 0.8]},
        ),
        dict(
            type='pie',
            labels=[WELL_TYPES[i] for i in aggregate.index],
            values=aggregate['API_WellNo'],
            name='Well Type Breakdown',
            hoverinfo="label+text+value+percent",
            textinfo="label+percent+name",
            hole=0.5,
            marker=dict(
                colors=[WELL_COLORS[i] for i in aggregate.index]
            ),
            domain={"x": [0.55, 1], 'y':[0.2, 0.8]},
        )
    ]
    layout_pie['title'] = 'Production Summary: {} to {}'.format(year_slider[0], year_slider[1])  # noqa: E501
    layout_pie['font'] = dict(color='#777777')
    layout_pie['legend'] = dict(
        font=dict(color='#CCCCCC', size='10'),
        orientation='h',
        bgcolor='rgba(0,0,0,0)'
    )

    figure = dict(data=data, layout=layout_pie)
    return figure


# Selectors -> count graph
@app.callback(Output('count_graph', 'figure'),
              [Input('well_statuses', 'value'),
               Input('well_types', 'value'),
               Input('year_slider', 'value')])
def make_count_figure(well_statuses, well_types, year_slider):

    layout_count = copy.deepcopy(layout)

    dff = filter_dataframe(df, well_statuses, well_types, [1960, 2017])
    g = dff[['API_WellNo', 'Date_Well_Completed']]
    g.index = g['Date_Well_Completed']
    g = g.resample('A').count()

    colors = []
    for i in range(1960, 2018):
        if i >= int(year_slider[0]) and i < int(year_slider[1]):
            colors.append('rgb(192, 255, 245)')
        else:
            colors.append('rgba(192, 255, 245, 0.2)')

    data = [
        dict(
            type='scatter',
            mode='markers',
            x=g.index,
            y=g['API_WellNo'] / 2,
            name='All Wells',
            opacity=0,
            hoverinfo='skip'
        ),
        dict(
            type='bar',
            x=g.index,
            y=g['API_WellNo'],
            name='All Wells',
            marker=dict(
                color=colors
            ),
        ),
    ]

    layout_count['title'] = 'Completed Wells/Year'
    layout_count['dragmode'] = 'select'
    layout_count['showlegend'] = False

    figure = dict(data=data, layout=layout_count)
    return figure


# In[]:
# Main

if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
