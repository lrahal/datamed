import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

from datamed_dash.app import app
from datamed_dash.map import get_dataframe, get_map


df = get_dataframe()

app.layout = html.Div(className='container-fluid', children=[
    html.Div(
        id="wrap",
        children=dbc.Container(
            id="main",
            children=[
                html.Div(id="hidden_div_for_redirect_callback"),
                dcc.Location(id="url", refresh=False),
                html.Div(id="page-content"),
            ],
            fluid=True,
            className="clear-top",
        ),
    ),
    dcc.Dropdown(id='dropdown_atc', options=[
        {'label': i, 'value': i} for i in df.atc2.unique()
    ], placeholder="ATC2"),
    dcc.Dropdown(id='dropdown_voie', options=[
        {'label': i, 'value': i} for i in df.voie.unique()], placeholder="Voie"),
    html.Iframe(id='map', srcDoc=open('map.html', 'r').read(), width='100%', height='600')
])


@app.callback(
    Output('dropdown_voie', 'options'),
    [Input('dropdown_atc', 'value')])
def compute_df(dropdown_value):
    voies = df[df.atc2 == dropdown_value].voie.unique()
    return [{'label': i, 'value': i} for i in voies]


@app.callback(
    Output('map', 'srcDoc'),
    [Input('dropdown_atc', 'value'), Input('dropdown_voie', 'value')])
def compute_map(dropdown_atc_value, dropdown_voie_values):
    get_map(df, dropdown_atc_value, dropdown_voie_values)
    return open('map.html', 'r').read()
