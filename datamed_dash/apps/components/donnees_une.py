from dash.development.base_component import Component
from dash_bootstrap_components import Card, CardImg, CardBody, CardLink
from dash_html_components import Div, A, H2, H4, Span, Iframe, P


def Indicateur(value: int, text: str, color: str, class_name: str) -> Component:
    return Span(
        [Span(str(value), style={'color': color, 'font-size': '20px'}), text],
        className=class_name,
    )


def RuptureCard():
    src = '/assets/pills.jpg'
    return Card(
        [
            CardImg(src=src, top=True),
            CardBody(
                [
                    H4(
                        "Qu'est-ce qu'une rupture ?",
                        className='card-title'
                    ),
                    P(
                        "Déclaration ou réelle rupture ? Nos experts vous "
                        "expliquent la différence avec des chiffres analysés",
                        className='card-text',
                    ),
                    CardLink(
                        "VOIR L'ANALYSE THÉMATIQUE",
                        href='analyse_thematique_ruptures',
                        className='analyse-thematique',
                    ),
                ]
            ),
        ],
        className='five grid-content d-flex flex-column align-items-center text-left'
    )


def DonneesUne() -> Component:
    src = '/assets/pills.jpg'
    return Div([
        Div(
            [],
            className='top'
        ),
        Div([
            H2(
                'Les données à la une',
            ),
            Div([
                Indicateur(265, ' ruptures de médicaments', '#ff8c00', 'two grid-content'),
                Indicateur(10, ' pays fabriquent du paracétamol', '#ff8c00', 'three grid-content'),
                Indicateur(1921, ' effets indésirables vaccin COVID 19', '#ff8c00', 'four grid-content'),
                RuptureCard(),
                Div([
                    Iframe(
                        id='map',
                        srcDoc=open('./assets/map.html', 'r').read()
                    )
                ],
                    className='six grid-content'
                ),
                Div([
                    Indicateur(265, ' ruptures de médicaments', '#00bfff', 'd-block'),
                    Indicateur(35, ' importations ce mois-ci', '#00bfff', 'd-block'),
                    Indicateur(65, ' réapprovisionnements', '#00bfff', 'd-block'),
                ],
                    className='seven grid-content d-flex flex-column justify-content-between py-5'
                ),
                Div([
                    A('Répartition par sexe des patients traités au Doliprane')
                ],
                    className='eight grid-content px-3 py-4',
                ),
                Div([
                    A('Répartition par âge des patients traités au Doliprane')
                ],
                    className='nine grid-content px-3 py-4',
                ),
            ],
                className='donnees-une',
            ),
        ], className='donnees-une-content'),
        Div(
            [],
            className='bottom'
        ),
    ],
        className='donnees-une-container'
    )
