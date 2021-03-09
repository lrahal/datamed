import json
import zipfile
from urllib.parse import urlparse, parse_qs

import dash.dependencies as dd
import pandas as pd
import plotly.graph_objects as go
from app import app
from dash.development.base_component import Component
from dash.exceptions import PreventUpdate
from dash_core_components import Graph
from dash_html_components import Div, A, P, Img
from sm import SideMenu

#with open("./data/med_dict.json") as jsonfile:
#    med_dict = json.load(jsonfile)

with zipfile.ZipFile('../data/med_dict.json.zip', "r") as z:
    filename = z.namelist()[0]
    with z.open(filename) as f:
        data = f.read()
        med_dict = json.loads(data.decode("utf-8"))

graphs_colors = ["#DFD4E5", "#BFAACB", "#5E2A7E"]

PROD_SUBS = pd.read_csv("./data/liste_produits_substances.csv", sep=";").to_dict(
    orient="records"
)
TYP_MED_DICT = {d["medicament"]: d["typ_medicament"] for d in PROD_SUBS}


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
                        "0",
                        className="box-highlight heading-4 d-inline-block",
                        id="patients-traites",
                    ),
                    Div(
                        "patients/an",
                        className="box-highlight heading-4 d-inline-block ml-2",
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
                            Graph(id="pie-patients-traites-sexe", className="img-card"),
                        ],
                        className="box d-inline-block",
                    ),
                    Div(
                        [
                            Div(
                                "Répartition par âge des patients traités",
                                className="normal-text",
                            ),
                            Graph(id="pie-patients-traites-age", className="img-card"),
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
                            Div(
                                "0",
                                className="box-highlight heading-4 d-inline-block",
                                id="cas-an",
                            ),
                            Div(
                                "cas/an",
                                className="box-highlight heading-4 d-inline-block ml-2",
                            ),
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
                                "0",
                                className="box-highlight heading-4 d-inline-block",
                                id="cas-declares",
                            ),
                            Div(
                                "cas déclarés",
                                className="box-highlight heading-4 d-inline-block ml-2",
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
                                "Répartition par sexe des cas déclarés",
                                className="normal-text",
                            ),
                            Graph(id="pie-cas-declares-sexe", className="img-card"),
                        ],
                        className="box d-inline-block",
                    ),
                    Div(
                        [
                            Div(
                                "Répartition par âge des cas déclarés",
                                className="normal-text",
                            ),
                            Graph(id="pie-cas-declares-age", className="img-card"),
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
                    P(
                        "Effets indésirables les plus déclarés par système d'organe",
                        className="normal-text",
                    ),
                    Img(src="/assets/Graph_EIsystemeorganes.svg", className="d-block"),
                ],
                className="box d-block",
            ),
        ],
        style=({"margin-bottom": "200px"}),
    )


def get_pie_chart(df, var_1, var_2, name):
    return go.Figure(
        go.Pie(
            labels=df[var_1],
            values=df[var_2],
            name=name,
            marker_colors=graphs_colors,
        )
    ).update_layout(margin=dict(t=0, b=0, l=0, r=0))


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


@app.callback(
    [
        dd.Output("pie-patients-traites-sexe", "figure"),
        dd.Output("pie-patients-traites-age", "figure"),
        dd.Output("pie-cas-declares-sexe", "figure"),
        dd.Output("pie-cas-declares-age", "figure"),
    ],
    dd.Input("url", "href"),
)
def generate_chart(href):
    parsed_url = urlparse(href)
    query = parse_qs(parsed_url.query)

    if "search" not in query:
        raise PreventUpdate

    else:
        medicament = query["search"][0]

        df_sexe = pd.DataFrame(med_dict[medicament]["sexe"])
        df_age = pd.DataFrame(med_dict[medicament]["age"])

        fig_patients_sexe = get_pie_chart(
            df_sexe, "sexe", "n_conso", "Répartition par sexe des patients traités"
        )

        if df_sexe.n_cas.sum() >= 10:
            fig_cas_sexe = get_pie_chart(
                df_sexe, "sexe", "n_cas", "Répartition par sexe des cas déclarés"
            )
        else:
            fig_cas_sexe = {}

        fig_patients_age = get_pie_chart(
            df_age, "age", "n_conso", "Répartition par âge des patients traités"
        )

        if df_age.n_cas.sum() >= 10:
            fig_cas_age = get_pie_chart(
                df_age, "age", "n_cas", "Répartition par âge des cas déclarés"
            )
        else:
            fig_cas_age = {}

        return (
            fig_patients_sexe,
            fig_patients_age,
            fig_cas_sexe,
            fig_cas_age,
        )


@app.callback(
    [
        dd.Output("Desc", "children"),
        dd.Output("patients-traites", "children"),
        dd.Output("cas-an", "children"),
        dd.Output("cas-declares", "children"),
        dd.Output("produit-target", "children"),
    ],
    dd.Input("url", "href"),
)
def change_product(href):
    parsed_url = urlparse(href)
    query = parse_qs(parsed_url.query)

    if "search" not in query:
        raise PreventUpdate

    else:
        medicament = query["search"][0]

        df = pd.DataFrame(med_dict[medicament]["annee"])

        # Calcul patients traités
        patients_traites = round(df.n_conso.mean())

        # Calcul nombre de cas par an
        cas_an = round(df.n_cas.sum() / df.n_conso.sum() * 100000)

        # Calcul nombre de cas déclarés
        if 0 < df.n_cas.sum() < 10:
            cas_declares = "< 10"
        else:
            cas_declares = df.n_cas.sum()

        return (
            medicament.lower().capitalize(),
            patients_traites,
            cas_an,
            cas_declares,
            TYP_MED_DICT[medicament],
        )
