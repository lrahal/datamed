from dash.development.base_component import Component
from dash_bootstrap_components import Button, Row, Col, Input
from dash_html_components import Div, A, H1, H4, H6, P


def DescriptionProduit() -> Component:
    return Div(
        Div([
            H1(
                'Doliprane',
            ),
            H4(
                'PRODUIT',
            ),
            H6(
                'Substance(s) active(s)',
                style={'margin-top': '30px'}
            ),
            A(
                'PARACÉTAMOL',
                style={'font-size': '1rem', 'color': '#ff8c00'}
            ),
            H6(
                'Description',
                style={'margin-top': '30px'}
            ),
            A(
                'Classe pharmacothérapeutique - classe ATC N02BE01',
                style={'font-size': '1rem'}
            ),
            P(
                "DOLIPRANE est un antalgique (calme la douleur) et un antipyrétique (fait baisser la fièvre). "
                "La substance active de ce médicament est le paracétamol. "
                "Il est utilisé pour traiter la douleur et/ou la fièvre, par exemple en cas de maux de tête, "
                "d'état grippal, de douleurs dentaires, de courbatures.",
                style={'font-size': '1rem', 'margin-top': '10px'}
            )
        ],
            className='description'
        ),
        className='description-container'
    )
