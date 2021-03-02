from dash.development.base_component import Component
from dash_bootstrap_components import (
    Popover,
    PopoverHeader,
    PopoverBody,
)
from dash_html_components import Div, A, H1, H4, H6, P, Span, Img


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
            H1("Patients traités", className="section-title"),
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
                                className="d-block",
                            ),
                            Img(
                                src="/assets/Graph_Nbtraites_sexe.svg",
                                className="d-block",
                            ),
                        ],
                        className="box d-inline-block",
                    ),
                    Div(
                        [
                            H6(
                                "Répartition par âge des patients traités",
                                className="d-block",
                            ),
                            Img(
                                src="/assets/Graph_Nbtraites_age.svg",
                                className="d-block",
                            ),
                        ],
                        className="box d-inline-block",
                    ),
                ]
            ),
        ],
        style=({"margin-bottom": "200px"}),
    )


def CasDeclares() -> Component:
    return Div(
        [
            H1("Cas déclarés d'effets indésirables", className="section-title"),
            Div(
                [
                    Div(
                        [
                            Span("2,5 cas/an", className="number"),
                            P(
                                "Taux de déclaration pour 100 000 patients traités sur la période 2014/2018",
                                className="mt-2",
                            ),
                        ],
                        className="box d-inline-block",
                    ),
                    Div(
                        [
                            Span("4 654 cas déclarés", className="number"),
                            P(
                                "Nombre de cas déclarés sur la période 2014/2018",
                                className="mt-2",
                            ),
                        ],
                        className="box d-inline-block",
                    ),
                ],
                className="d-block",
            ),
            Div(
                [
                    P(
                        "Nombre de cas déclarés d'effets indésirables et patients traités par année",
                        className="mt-2",
                    ),
                    Img(src="/assets/Graph_Nbcas_EI.svg", className="d-block"),
                ],
                className="box d-block",
            ),
            Div(
                [
                    Div(
                        [
                            H6(
                                "Répartition par sexe des patients traités",
                                className="d-block",
                            ),
                            Img(
                                src="/assets/Graph_Nbcas_sexe.svg", className="d-block"
                            ),
                        ],
                        className="box d-inline-block",
                    ),
                    Div(
                        [
                            H6(
                                "Répartition par âge des patients traités",
                                className="d-block",
                            ),
                            Img(
                                src="/assets/Graph_Nbcas_age.svg",
                                className="d-block",
                            ),
                        ],
                        className="box d-inline-block",
                    ),
                ]
            ),
            Div(
                [
                    P(
                        "Répartition par type de notificateur",
                        className="mt-2",
                    ),
                    Img(src="/assets/Graph_TypeNotificateur.svg", className="d-block"),
                ],
                className="box d-block",
            ),
        ],
        style=({"margin-bottom": "200px"}),
    )


def Organes() -> Component:
    return Div(
        [
            H1("Effets indésirables par systèmes d'organes", className="section-title"),
            Div(
                [
                    P(
                        "Répartition par type de notificateur",
                        className="mt-2",
                    ),
                    Img(src="/assets/Graph_EIsystemeorganes.svg", className="d-block"),
                ],
                className="box d-block",
            ),
        ],
        style=({"margin-bottom": "200px"}),
    )
