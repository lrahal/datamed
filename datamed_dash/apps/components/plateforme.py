from dash.development.base_component import Component
from dash_bootstrap_components import Button, Card, CardImg, CardBody
from dash_html_components import Div


def Plateforme() -> Component:
    return Card(
        [
            Div(
                [
                    CardImg(src="/assets/screen.jpg", className="col-7 h-100"),
                    CardBody(
                        [
                            Div(
                                "Une plateforme unique pour réunir les données essentielles de l'ANSM",
                                className="heading-4",
                            ),
                            Div(
                                "Soucieuse de rendre ses données accessibles et transparentes, l'Agence Nationale de "
                                "Sécurité du Médicament et des Produits de Santé a lancé data.ansm.fr, un lieu "
                                "numérique pour retrouver les données de l'agence.",
                                className="medium-text mt-3",
                            ),
                            Button(
                                "À PROPOS",
                                outline=True,
                                className="button-text-bold",
                                type="submit",
                                color="secondary",
                            ),
                        ],
                        className="col-5 plateforme-card-body",
                    ),
                ],
                className="row",
            ),
        ],
        className="plateforme-card w-75 mx-auto",
    )
