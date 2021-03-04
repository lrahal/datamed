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
                H1("Doliprane", className="nav-title", id="Desc"),
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
            H1("Patients traités", className="section-title nav-title", id="Pop"),
            Div(
                [
                    Div("36 832 698,4 patients/an", className="box-highlight"),
                    P(
                        "Nombre moyen de patients traités par an sur la période 2014/2018"
                    ),
                ],
                className="box d-block",
            ),
            Div(
                [
                    Div(
                        [
                            H6("Répartition par sexe des patients traités"),
                            Img(src="/assets/Graph_Nbtraites_sexe.svg"),
                        ],
                        className="box d-inline-block",
                    ),
                    Div(
                        [
                            H6("Répartition par âge des patients traités"),
                            Img(src="/assets/Graph_Nbtraites_age.svg"),
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
            H1(
                "Cas déclarés d'effets indésirables",
                className="section-title nav-title",
                id="Effets",
            ),
            Div(
                [
                    Div(
                        [
                            Div("2,5 cas/an", className="box-highlight"),
                            P(
                                "Taux de déclaration pour 100 000 patients traités sur la période 2014/2018"
                            ),
                        ],
                        className="box d-inline-block",
                    ),
                    Div(
                        [
                            Div("4 654 cas déclarés", className="box-highlight"),
                            P("Nombre de cas déclarés sur la période 2014/2018"),
                        ],
                        className="box d-inline-block",
                    ),
                ],
            ),
            Div(
                [
                    P(
                        "Nombre de cas déclarés d'effets indésirables et patients traités par année"
                    ),
                    Img(src="/assets/Graph_Nbcas_EI.svg", className="d-block"),
                ],
                className="box",
            ),
            Div(
                [
                    Div(
                        [
                            H6("Répartition par sexe des patients traités"),
                            Img(src="/assets/Graph_Nbcas_sexe.svg"),
                        ],
                        className="box d-inline-block",
                    ),
                    Div(
                        [
                            H6("Répartition par âge des patients traités"),
                            Img(src="/assets/Graph_Nbcas_age.svg"),
                        ],
                        className="box d-inline-block",
                    ),
                ]
            ),
            Div(
                [
                    P("Répartition par type de notificateur"),
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
            H1("Effets indésirables par systèmes d'organes", className="section-title"),
            Div(
                [
                    P("Répartition par type de notificateur"),
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
