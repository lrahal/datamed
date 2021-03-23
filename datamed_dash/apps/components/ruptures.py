import json
import zipfile
from urllib.parse import urlparse, parse_qs

import dash.dependencies as dd
import pandas as pd
import plotly.graph_objects as go
from app import app
from dash.development.base_component import Component
from dash.exceptions import PreventUpdate
from dash_bootstrap_components import (
    Button,
    Modal,
    ModalHeader,
    ModalBody,
    ModalFooter,
    Table,
)
from dash_core_components import Graph
from dash_html_components import Div, A, P, Img, I
from plotly.subplots import make_subplots
from sm import SideMenu

from .main_search import SearchBar


PIE_COLORS = ["#DFD4E5", "#BFAACB", "#5E2A7E"]
BAR_CHART_COLORS = [
    "rgba(51,171,102,1)",
    "rgba(102,192,140,1)",
    "rgba(153,213,179,1)",
    "rgba(204,234,217,1)",
    "rgba(191,213,60,1)",
    "rgba(207,223,109,1)",
    "rgba(223,234,157,1)",
    "rgba(239,244,206,1)",
    "rgba(51,194,214,1)",
    "rgba(102,209,224,1)",
]


def DescriptionRuptures() -> Component:
    return Div(
        Div(
            [
                Div(
                    I(
                        className="bi bi-book d-flex justify-content-center pt-3",
                        style={"font-size": "3rem"},
                    ),
                    className="col-1",
                ),
                Div(
                    [
                        Div(
                            "Observatoire des ruptures de stock",
                            className="heading-4",
                            id="description-ruptures",
                        ),
                        Div(
                            [
                                Div(
                                    "BASE DE DONNÉES",
                                    className="caption-text d-inline-block",
                                ),
                                I(
                                    className="info-icon bi bi-info-circle d-inline-block"
                                ),
                            ]
                        ),
                        Div("Bases de données exploitées", className="small-text-bold"),
                        A(
                            "TrustMed, États des lieux des laboratoires",
                            href="/",
                            className="normal-text link",
                            id="refresh-substances",
                        ),
                        Div(
                            "Description",
                            className="small-text-bold",
                        ),
                        P(
                            "L’ANSM a pour mission d’observer tout au long de l’année l’état des ruptures de stock "
                            "de médicaments présents dans les circuits Ville et Hôpital et s’assurer du maintien des "
                            "stocks en cas de tension d’approvisionnement et de rupture. Retrouvez les différentes "
                            "formes et chiffres de signalements que l’Agence reçoit, et les actions mises en place "
                            "pour y remédier et maintenir ainsi l’alimentation des officines au niveau national.",
                            className="normal-text",
                        ),
                        Div(
                            "Avertissement",
                            className="small-text-bold",
                        ),
                        P(
                            "Les chiffres présentés ici ont pour but d’ouvrir les données au grand public afin de "
                            "communiquer les actions de l’Agence. Leur interprétation et diffusion est soumise à de "
                            "strictes réglementations. L’Agence ne se tient pas responsable en cas d’interprétation "
                            "erronnée et de divulgation de ces chiffres et/ou dans un contexte qui ne permettrait pas "
                            "leur lecture dans les conditions optimales. En cas de doute, veuillez nous contacter, "
                            "vous contribuerez directement à l’amélioration de l’information diffusée.",
                            className="normal-text",
                        ),
                        Div(
                            "Réutilisation des données",
                            className="small-text-bold",
                        ),
                        A(
                            "Analyse thématique, data.gouv.fr",
                            href="/",
                            className="normal-text link",
                            id="refresh-substances",
                        ),
                    ],
                    className="col-11",
                ),
            ],
            className="description col-xl-8 col-sm-11 row",
        ),
        style={"margin-top": "31.5px"},
        className="specialite-section",
    )


def Ruptures() -> Component:
    return Div(
        [
            SideMenu(
                id="side-menu",
                items=[
                    {"id": "description-ruptures", "label": "Description"},
                    {"id": "signalements", "label": "Signalements"},
                    {"id": "gestion-ruptures", "label": "Gestion des ruptures"},
                ],
                className="side-menu",
            ),
            Div(
                [
                    DescriptionRuptures(),
                ]
            ),
        ],
        className="side-menu-container",
    )


