from dash.development.base_component import Component
from dash_bootstrap_components import Button
from dash_html_components import Div, Span, Img, P


def Plateforme() -> Component:
    src = "/assets/screen.jpg"
    return Div(
        [
            Img(src=src, style={"width": "50%"}, className="img-fluid", alt="Responsive image"),
            Div(
                [
                    Span(
                        "Une plateforme unique pour réunir les données essentielles de l'ANSM",
                        className="heading-4",
                    ),
                    P(
                        "Soucieuse de rendre ses données accessibles et transparentes, l'Agence Nationale de Sécurité "
                        "du Médicament et des Produits de Santé a lancé data.ansm.fr, un lieu numérique pour retrouver "
                        "les données autour de l'agence.",
                        className="mt-3 color-black",
                        style={"font-size": "20px", "font-weight": "400"},
                    ),
                    Button(
                        "À PROPOS",
                        outline=True,
                        className="button-text-bold  mr-1",
                        color="secondary",
                        style={"margin-top": "1rem"},
                    ),
                ],
                className="px-3 py-3 mt-2",
            ),
        ],
        className="plateforme px-3 py-3 d-flex",
    )
