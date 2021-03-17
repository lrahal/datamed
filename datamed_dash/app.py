import dash
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        __file__.replace("index.py", "./assets/style.css"),
    ],
    external_scripts=[
        dbc.themes.BOOTSTRAP,
        __file__.replace("index.py", "./assets/menu.js"),
    ],
    suppress_callback_exceptions=True,
    title="Dashboard - DataMed",
)
server = app.server
