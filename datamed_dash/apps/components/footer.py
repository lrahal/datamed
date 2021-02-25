from dash.development.base_component import Component
from dash_html_components import Div, H3, Span, Img, H2, A, B
from dash_bootstrap_components import Button
from typing import List


def FooterElement(title: str, element_list: List[str]) -> Component:
    text_element_list = [H2(title, className='mb-4')] + \
                        [Span(element, className='d-block mb-3') for element in element_list]
    return Div(
        text_element_list,
        className='footer-left-content'
    )


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


def FooterLeft():
    return Div([
        FooterElement(
            'Le site',
            ['À propos', 'Plan de site', 'Mentions légales', 'Contact']
        ),
        FooterElement(
            'Partenaires',
            ['ansm.sante.fr', 'base-donnees-publique.medicaments.gouv.fr', 'Etalab', 'La DINUM']
        ),
    ],
        className='footer-left'
    )


def Footer() -> Component:
    return Div([
        Logos(),
        FooterLeft(),
    ],
        className='footer'
    )
