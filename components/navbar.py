# Import necessary libraries
from dash import html
import dash_bootstrap_components as dbc


# Define the navbar structure
def Navbar():

    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Home", href="/home")),
                dbc.NavItem(dbc.NavLink("Dinosaurs", href="/dinosaurs")),
            ] ,
            brand="Dinosaur Dashboard",
            brand_href="/page1",
            color="dark",
            dark=True,
        ), 
    ])

    return layout