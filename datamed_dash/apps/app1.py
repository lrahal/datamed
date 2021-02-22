import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash_html_components import A, B, Div, Span, Iframe, Img
from dash.development.base_component import Component
from components.navbar import Navbar
from dash.dependencies import Output, Input

from app1_init import app


def _med_search() -> Component:
    search_bar = dbc.Row(
        [
            dbc.Col(dbc.Input(type="search", placeholder="Search")),
        ],
        no_gutters=True,
        className="search-med ml-auto flex-nowrap mt-3",
        align="center",
    )
    return Div(
        Div([
            Span(
                "Trouvez des données autour du médicament",
                style={"font-size": "30px", 'margin-top': '5rem'}
            ),
            search_bar,
            dbc.Button("RECHERCHER", outline=True, className="mr-1", color="secondary",
                       style={'margin-top': '3rem'})
        ],
            className='med-search'
        ),
        className='med-search-container'
    )


def _donnees_une() -> Component:
    src = '/assets/pills.jpg'
    donnees_une = Div([
        Span(
            'Les données à la une',
            style={"font-size": "30px"},
            className='one'
        ),
        Span(
            [A('265', style={'color': '#ff8c00', 'font-size': '20px'}),
             A(' ruptures de médicaments')],
            className='two grid-content',
        ),
        Span(
            [A('10', style={'color': '#ff8c00', 'font-size': '20px'}),
             A(' pays fabriquant du paracétamol')],
            className='three grid-content',
        ),
        Span(
            [A('1921', style={'color': '#ff8c00', 'font-size': '20px'}),
             A(' effets indésirables vaccin COVID 19')],
            className='four grid-content',
        ),
        Div([
            Img(src=src, style={'width': '100%'}),
            B("Qu'est-ce qu'une rupture ?", style={'font-size': '20px', 'display': 'block', 'text-align': 'left'}),
            A(
                "Déclaration ou réelle rupture ? Nos experts vous expliquent la différence avec des chiffres analysés",
                style={'display': 'block', 'text-align': 'left'}),
            A(id='link', href='analyse_thematique_ruptures', children="VOIR L'ANALYSE THEMATIQUE", target="_blank",
              style={'display': 'block', 'text-align': 'left'})
        ], className='five grid-content'),
        Div([
            Iframe(id='map', srcDoc=open('assets/map.html', 'r').read())],
            className='six grid-content'),
        Div([
            Span(
                [A('265', style={'color': '#00bfff', 'font-size': '20px'}),
                 A(' ruptures de médicaments')], style={'display': 'block'}),
            Span(
                [A('35', style={'color': '#00bfff', 'font-size': '20px'}),
                 A(' importations ce mois-ci')], style={'display': 'block'}),
            Span(
                [A('65', style={'color': '#00bfff', 'font-size': '20px'}),
                 A(' réapprovisionnements')], style={'display': 'block'}),
        ],
            className='seven grid-content'
        ),
    ],
        className='div-donnees-une-2'
    )
    return donnees_une


app.layout = Div(
    [
        dcc.Location(id='url', refresh=False),
        Navbar(),
        _med_search(),
        _donnees_une(),
        Div(id='page-content', className='container')
    ],
    id='layout',
)

if __name__ == '__main__':
    app.run_server(debug=True)
