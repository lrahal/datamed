from dash.development.base_component import Component
from dash_bootstrap_components import (
    Popover,
    PopoverHeader,
    PopoverBody,
)
from dash_html_components import Div, A, H1, H4, H6, P, Span, Img
from sm import SideMenu


def DescriptionProduit() -> Component:
    return Div(
        Div(
            [
                Div("Doliprane", className="heading-4 nav-title", id="Desc"),
                Div(
                    "PRODUIT",
                    id="produit-target",
                    className="caption-text",
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
                Div("Substance(s) active(s)", className="small-text-bold mt-3"),
                A(
                    "PARACÉTAMOL",
                    href="/",
                    style={"color": "#EF7D00"},
                    className="normal-text",
                ),
                Div(
                    "Description",
                    style={"margin-top": "30px"},
                    className="small-text-bold",
                ),
                P(
                    "Classe pharmacothérapeutique - classe ATC N02BE01",
                    className="normal-text mt-2",
                ),
                P(
                    "DOLIPRANE est un antalgique (calme la douleur) et un antipyrétique (fait baisser la fièvre). "
                    "La substance active de ce médicament est le paracétamol. "
                    "Il est utilisé pour traiter la douleur et/ou la fièvre, par exemple en cas de maux de tête, "
                    "d'état grippal, de douleurs dentaires, de courbatures.",
                    className="normal-text mt-1",
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
                "Patients traités",
                className="section-title nav-title heading-4",
                id="Pop",
            ),
            Div(
                [
                    Div(
                        "36 832 698,4 patients/an", className="box-highlight heading-4"
                    ),
                    P(
                        "Nombre moyen de patients traités par an sur la période 2014/2018",
                        className="normal-text",
                    ),
                ],
                className="box d-block",
            ),
            Div(
                [
                    Div(
                        [
                            Div(
                                "Répartition par sexe des patients traités",
                                className="normal-text",
                            ),
                            Img(src="/assets/Graph_Nbtraites_sexe.svg", className="img-card"),
                        ],
                        className="box d-inline-block",
                    ),
                    Div(
                        [
                            Div(
                                "Répartition par âge des patients traités",
                                className="normal-text",
                            ),
                            Img(src="/assets/Graph_Nbtraites_age.svg", className="img-card"),
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
            Div(
                "Cas déclarés d'effets indésirables",
                className="section-title nav-title heading-4",
                id="Effets",
            ),
            Div(
                [
                    Div(
                        [
                            Div("2,5 cas/an", className="box-highlight heading-4"),
                            Div(
                                "Taux de déclaration pour 100 000 patients traités sur la période 2014/2018",
                                className="normal-text",
                            ),
                        ],
                        className="box d-inline-block",
                    ),
                    Div(
                        [
                            Div(
                                "4 654 cas déclarés",
                                className="box-highlight heading-4",
                            ),
                            Div(
                                "Nombre de cas déclarés sur la période 2014/2018",
                                className="normal-text",
                            ),
                        ],
                        className="box d-inline-block",
                    ),
                ],
            ),
            Div(
                [
                    Div(
                        "Nombre de cas déclarés d'effets indésirables et patients traités par année",
                        className="normal-text",
                    ),
                    Img(src="/assets/Graph_Nbcas_EI.svg", className="d-block"),
                ],
                className="box",
            ),
            Div(
                [
                    Div(
                        [
                            Div(
                                "Répartition par sexe des patients traités",
                                className="normal-text",
                            ),
                            Img(src="/assets/Graph_Nbcas_sexe.svg", className="img-card"),
                        ],
                        className="box d-inline-block",
                    ),
                    Div(
                        [
                            Div(
                                "Répartition par âge des patients traités",
                                className="normal-text",
                            ),
                            Img(src="/assets/Graph_Nbcas_age.svg", className="img-card"),
                        ],
                        className="box d-inline-block",
                    ),
                ]
            ),
            Div(
                [
                    Div(
                        "Répartition par type de notificateur", className="normal-text"
                    ),
                    Img(src="/assets/Graph_TypeNotificateur.svg"),
                ],
                className="box",
            ),
        ],
        style=({"margin-bottom": "200px"}),
    )


def Organes() -> Component:
    return Div(
        [
            Div(
                "Effets indésirables par système d'organe",
                className="section-title heading-4",
            ),
            Div(
                [
                    P("Effets indésirables les plus déclarés par système d'organe", className="normal-text"),
                    Img(src="/assets/Graph_EIsystemeorganes.svg", className="d-block"),
                ],
                className="box d-block",
            ),
        ],
        style=({"margin-bottom": "200px"}),
    )


def Produit() -> Component:
    return Div(
        [
            SideMenu(
                id="side-menu",
                items=[
                    {"id": "Desc", "label": "Description"},
                    {"id": "Pop", "label": "Population concernée"},
                    {"id": "Effets", "label": "Effets indésirables"},
                    {"id": "EM", "label": "Erreurs médicamenteuses"},
                    {"id": "PF", "label": "Pays de fabrication"},
                ],
                className="side-menu",
            ),
            Div(
                [
                    DescriptionProduit(),
                    PatientsTraites(),
                    CasDeclares(),
                    Organes(),
                ]
            ),
        ],
        className="side-menu-container",
    )
