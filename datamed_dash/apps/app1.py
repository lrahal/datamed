import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.development.base_component import Component
from dash.dependencies import Output, Input

from app1_init import app


def _get_nav() -> Component:
    dropdown = dbc.DropdownMenu(
        label="Explorer",
        children=[
            dbc.DropdownMenuItem("Cartographie"),
            dbc.DropdownMenuItem("Erreurs médicamenteuses"),
            dbc.DropdownMenuItem("Effets indésirables"),
        ],
        style={'display': 'inline-block'},
        className='navbar-dropdown',
    )
    nav = html.Span(
        [
            dbc.NavbarBrand(
                ["data.", html.B("ansm.sante.fr")],
                className="ml-2",
                style={'color': 'black', 'display': 'inline-block', "font-size": "15px"}),
            html.Span(
                [
                    html.Span(
                        html.A(
                            'Analyses thématiques',
                            href='/',
                            className='nav-link',
                            style={'color': 'grey', 'display': 'inline-block'})
                    ),
                    dropdown,
                    html.Span(
                        html.A(
                            'À propos',
                            href='/',
                            className='nav-link',
                            style={'color': 'grey', 'display': 'inline-block'})
                    ),
                    dbc.Button("CONTACT", outline=True, className="mr-1", color="primary")]
            ),
        ],
        className='navbar-span'
    )
    return nav


def _get_page_heading() -> Component:
    src = '/assets/logo_ansm.png'
    sticky_style = {
        'position': 'absolute',
        'height': '88px',
        'left': '0px',
        'top': '0px',
        'border': '1px solid  #9E9E9E',
        'width': '100%',
        'border-right': 'none',
        'border-left': 'none',
        'display': 'flex',
        'align-items': 'center',
    }
    img = html.Img(src=src, style={'width': '100px', 'display': 'inline-block'})
    return html.Div(html.Div([dcc.Link(img, href='/'), _get_nav()], className='container'), style=sticky_style)


def get_med_search() -> Component:
    search_bar = dbc.Row(
        [
            dbc.Col(dbc.Input(type="search", placeholder="Search")),
        ],
        no_gutters=True,
        className="search-med ml-auto flex-nowrap mt-3",
        align="center",
    )
    med_search = html.Div([
        html.Span(
            "Trouvez des données autour du médicament",
            style={"font-size": "30px", 'margin-top': '5rem'}
        ),
        search_bar,
        dbc.Button("RECHERCHER", outline=True, className="mr-1", color="secondary",
                   style={'margin-top': '3rem'})
    ],
        className='div-med-search'
    )
    return med_search


def get_donnees_une_prout() -> Component:
    src = '/assets/pills.jpg'
    donnees_une = html.Div([
        html.Div([
            html.Span(
                "Les données à la une",
                style={"font-size": "30px"}
            )
        ]),
        html.Div([
            html.Span(
                [html.A('265', style={'color': '#ff8c00', 'font-size': '20px'}),
                 html.A(' ruptures de médicaments')],
                className='span-donnees-une',
            ),
            html.Span(
                [html.A('10', style={'color': '#ff8c00', 'font-size': '20px'}),
                 html.A(' pays fabriquant du paracétamol')],
                className='span-donnees-une',
            ),
            html.Span(
                [html.A('1921', style={'color': '#ff8c00', 'font-size': '20px'}),
                 html.A(' effets indésirables vaccin COVID 19')],
                className='span-donnees-une',
            ),
        ], style={'display': 'flex', 'justify-content': 'space-evenly'}),
        html.Div([
            html.Div([
                html.Img(src=src, style={'width': '50%'}),
            ], style={'width': '20%', 'display': 'inline-block'}),
            html.Iframe(id='map', srcDoc=open('assets/map.html', 'r').read(), style={'width': '60%'})
        ], style={'display': 'flex', 'justify-content': 'space-evenly', 'padding': '30px'})
    ],
        className='div-donnees-une'
    )
    return donnees_une


def get_donnees_une() -> Component:
    src = '/assets/pills.jpg'
    donnees_une = html.Div([
        html.Span(
            'Les données à la une',
            style={"font-size": "30px"},
            className='one'
        ),
        html.Span(
            [html.A('265', style={'color': '#ff8c00', 'font-size': '20px'}),
             html.A(' ruptures de médicaments')],
            className='two grid-content',
            ),
        html.Span(
                [html.A('10', style={'color': '#ff8c00', 'font-size': '20px'}),
                 html.A(' pays fabriquant du paracétamol')],
                className='three grid-content',
            ),
        html.Span(
                [html.A('1921', style={'color': '#ff8c00', 'font-size': '20px'}),
                 html.A(' effets indésirables vaccin COVID 19')],
                className='four grid-content',
            ),
        html.Div([
            html.Img(src=src, style={'width': '100%'}),
            html.B("Qu'est-ce qu'une rupture ?", style={'font-size': '20px', 'display': 'block', 'text-align': 'left'}),
            html.A("Déclaration ou réelle rupture ? Nos experts vous expliquent la différence avec des chiffres analysés",
                   style={'display': 'block', 'text-align': 'left'}),
            html.A(id='link', href='analyse_thematique_ruptures', children="VOIR L'ANALYSE THEMATIQUE", target="_blank",
                   style={'display': 'block', 'text-align': 'left'})
        ], className='five grid-content'),
        html.Div([
            html.Iframe(id='map', srcDoc=open('assets/map.html', 'r').read())],
            className='six grid-content'),
        html.Div([
            html.Span(
                [html.A('265', style={'color': '#00bfff', 'font-size': '20px'}),
                 html.A(' ruptures de médicaments')], style={'display': 'block'}),
            html.Span(
                [html.A('35', style={'color': '#00bfff', 'font-size': '20px'}),
                 html.A(' importations ce mois-ci')], style={'display': 'block'}),
            html.Span(
                [html.A('65', style={'color': '#00bfff', 'font-size': '20px'}),
                 html.A(' réapprovisionnements')], style={'display': 'block'}),
        ],
            className='seven grid-content'
        ),
    ],
        className='div-donnees-une-2'
    )
    return donnees_une


app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        _get_page_heading(),
        get_med_search(),
        get_donnees_une(),
        html.Div(id='page-content', className='container')
    ],
    id='layout',
)

if __name__ == '__main__':
    app.run_server(debug=True)

