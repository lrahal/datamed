import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from app_init import app
from map import get_dataframe

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button("Search", color="primary", className="ml-2"),
            width="auto",
        ),
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand("Dashboard DataMed", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://ansm.sante.fr",
        ),
        dbc.NavItem(dbc.NavLink("Analyses thématiques", href="#")),
        dbc.NavItem(dbc.NavLink("Jeux de données", href="#")),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
    ],
    color="dark",
    dark=True,
)

df = get_dataframe()

app.layout = html.Div(className='container-fluid', children=[
    html.Div(
        id="wrap",
        children=dbc.Container(
            id="main",
            children=[
                html.Div(id="hidden_div_for_redirect_callback"),
                dcc.Location(id="url", refresh=False),
                navbar,
                html.Div(id="page-content"),
            ],
            fluid=True,
            className="clear-top",
        ),
    ),
    dcc.Dropdown(id='dropdown', options=[
        {'label': i, 'value': i} for i in df.atc2.unique()
    ]),
    # html.Iframe(id='map', srcDoc=open('map.html', 'r').read(), width='100%', height='600')
])

if __name__ == '__main__':
    app.run_server(debug=True)
