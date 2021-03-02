from dash.development.base_component import Component
from dash_bootstrap_components import (
    Button,
    Row,
    Col,
    Input,
    Popover,
    PopoverHeader,
    PopoverBody,
    Card,
    CardImg,
    CardBody,
    CardLink,
)
from dash_html_components import Div, A, H1, H2, H3, H4, H6, P, Span


def DescriptionProduit() -> Component:
    return Div(
        Div(
            [
                H1(
                    "Doliprane",
                ),
                H4(
                    "PRODUIT",
                    id="produit-target",
                ),
                Popover(
                    [
                        PopoverHeader("Produit"),
                        PopoverBody("Le produit est ..."),
                    ],
                    id="popover",
                    is_open=False,
                    target="produit-target",
                ),
                H6("Substance(s) active(s)", style={"margin-top": "30px"}),
                A(
                    "PARACÉTAMOL",
                    href="/",
                    style={"font-size": "1rem", "color": "#ff8c00"},
                ),
                H6("Description", style={"margin-top": "30px"}),
                Span(
                    "Classe pharmacothérapeutique - classe ATC N02BE01",
                    style={"font-size": "1rem"},
                ),
                P(
                    "DOLIPRANE est un antalgique (calme la douleur) et un antipyrétique (fait baisser la fièvre). "
                    "La substance active de ce médicament est le paracétamol. "
                    "Il est utilisé pour traiter la douleur et/ou la fièvre, par exemple en cas de maux de tête, "
                    "d'état grippal, de douleurs dentaires, de courbatures.",
                    style={"font-size": "1rem", "margin-top": "10px"},
                ),
            ],
            className="description",
        ),
        className="description-container",
    )


def PatientsTraites() -> Component:
    return Div(
        [
            Div(
                [
                    Span("36 832 698,4 patients/an", className="number"),
                    P(
                        "Nombre moyen de patients traités par an sur la période 2014/2018",
                        className="mt-2",
                    ),
                ],
                className="box d-block",
            ),
            Div(
                [
                    Div(
                        [
                            H6(
                                "Répartition par sexe des patients traités",
                            )
                        ],
                        className="box d-inline-block",
                    ),
                    Div(
                        [
                            H6(
                                "Répartition par sexe des patients traités",
                            ),
                        ],
                        className="box d-inline-block",
                    ),
                ]
            ),
        ]
    )


# /assets/Card chart2.png
