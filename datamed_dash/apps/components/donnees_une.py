from dash.development.base_component import Component
from dash_html_components import Div, A, B, Span, Iframe, Img


def Indicateur(value, text, color, class_name):
    return Span(
            [Span(str(value), style={'color': color, 'font-size': '20px'}), text],
            className=class_name,
        )


def DonneesUne() -> Component:
    src = '/assets/pills.jpg'
    return Div([
        Span(
            'Les données à la une',
            style={"font-size": "30px"},
            className='one'
        ),
        Indicateur(265, ' ruptures de médicaments', '#ff8c00', 'two grid-content'),
        Indicateur(10, ' pays fabriquant du paracétamol', '#ff8c00', 'three grid-content'),
        Indicateur(1921, ' effets indésirables vaccin COVID 19', '#ff8c00', 'four grid-content'),
        Div([
            Img(
                src=src,
                style={'width': '100%'}
            ),
            B(
                "Qu'est-ce qu'une rupture ?",
                style={'font-size': '20px', 'display': 'block', 'text-align': 'left'}
            ),
            Span(
                "Déclaration ou réelle rupture ? Nos experts vous expliquent la différence avec des chiffres analysés",
                style={'display': 'block', 'text-align': 'left'}
            ),
            A(
                id='link',
                href='analyse_thematique_ruptures',
                children="VOIR L'ANALYSE THEMATIQUE",
                target="_blank",
                style={'display': 'block', 'text-align': 'left'})
        ],
            className='five grid-content'),
        Div([
            Iframe(
                id='map',
                srcDoc=open('assets/map.html', 'r').read()
            )
        ],
            className='six grid-content'
        ),
        Div([
            Indicateur(265, ' ruptures de médicaments', '#00bfff', 'd-block'),
            Indicateur(35, ' importations ce mois-ci', '#00bfff', 'd-block'),
            Indicateur(65, ' réapprovisionnements', '#00bfff', 'd-block'),
        ],
            className='seven grid-content'
        ),
    ],
        className='donnees-une'
    )
