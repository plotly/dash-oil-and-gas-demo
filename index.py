# Import necessary libraries 
from dash import html, dcc
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app

# Connect to your app pages
from pages import dinosaurs, home, page1

# Connect the navbar to the index
from components import navbar

# define the navbar
nav = navbar.Navbar()

# Define the index page layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav, 
    html.Div(id='page-content', children=[]), 
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/home':
        return home.layout
    if pathname == '/dinosaurs':
        return dinosaurs.layout
    else:
        return home.layout

# Run the app on localhost:8050
if __name__ == '__main__':
    app.run_server(debug=True)