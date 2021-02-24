from dash.development.base_component import Component
from dash_html_components import Div, H3, Span, Img, H2, A, B
from dash_bootstrap_components import Button


def Logos() -> Component:
    return Div([
        Div([
            Img(
                src='/assets/1200px-Republique-francaise-logo.svg.png',
                className='img-logo'
            ),
            Img(
                src='/assets/Ansm-logo-Grand.jpg',
                className='img-logo'
            ),
        ]),
        H3(
            [
                'data.',
                B('ansm.sante.fr')
            ],
            style={'color': 'white', 'margin-top': '20px'},
        )
    ],
        className='logos'
    )


def Site():
    return Div([
        H2('Le site'),
        Span('À propos'),
        Span('Plan du site'),
        Span('Mentions légales'),
        Span('Contact'),
    ],
        className='site'
    )


def Footer() -> Component:
    return Div([
        Logos(),
        Site(),
    ],
        style={'display': 'inline-block'}
    )
