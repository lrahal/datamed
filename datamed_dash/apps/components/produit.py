import json
import zipfile

import pandas as pd
import plotly.graph_objects as go
from dash.development.base_component import Component
from dash_core_components import Graph, Dropdown
from dash_bootstrap_components import Button, Row, Col
from dash_html_components import Div, A, P
from plotly.subplots import make_subplots
from sm import SideMenu
from app import app
import dash.dependencies as dd
from dash.exceptions import PreventUpdate

with zipfile.ZipFile("./data/med_dict.json.zip", "r") as z:
    filename = z.namelist()[0]
    with z.open(filename) as f:
        data = f.read()
        med_dict = json.loads(data.decode("utf-8"))

graphs_colors = ["#DFD4E5", "#BFAACB", "#5E2A7E"]

PROD_SUBS = pd.read_csv("./data/liste_produits_substances.csv", sep=";").to_dict(
    orient="records"
)
TYP_MED_DICT = {d["medicament"]: d["typ_medicament"] for d in PROD_SUBS}

f = open("./data/substance_by_produit.json", "r")
SUBSTANCE_BY_PRODUIT = json.loads(f.read())


def SearchDiv(produit) -> Component:
    return Div(
        [
            Row(
                [
                    Col(
                        Dropdown(
                            placeholder="Médicament, substance active",
                            className="normal-text main-dropdown",
                            id="produit-search-bar",
                        )
                    ),
                ],
                no_gutters=True,
                className="col-xl-7 pl-0",
            ),
            Button(
                "RECHERCHER",
                n_clicks=0,
                outline=True,
                className="col-xl-1 button-text-bold",
                color="secondary",
                type="submit",
                id="produit-rechercher-button",
            ),
        ],
        style={"margin-left": "20px", "margin-top": "2rem"},
        className="row",
    )


def DescriptionProduit(produit) -> Component:
    return Div(
        Div(
            [
                Div(
                    produit.lower().capitalize(),
                    className="heading-4",
                    id="Desc",
                ),
                Div(
                    TYP_MED_DICT[produit],
                    className="caption-text",
                ),
                Div("Substance(s) active(s)", className="small-text-bold mt-3"),
                A(
                    ", ".join(SUBSTANCE_BY_PRODUIT[produit.lower()]),
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
            className="description col-xl-8 col-sm-6",
        ),
        style={"margin-top": "2rem"},
        className="product-section",
    )


def PiePatientTraiteSexe(produit) -> Graph:
    df_sexe = pd.DataFrame(med_dict[produit]["sexe"])

    fig = get_pie_chart(
        df_sexe, "sexe", "n_conso", "Répartition par sexe des patients traités"
    )
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return Graph(
        figure=fig,
        className="img-card",
        responsive=True,
    )


def PiePatientTraiteAge(produit) -> Graph:
    df_age = pd.DataFrame(med_dict[produit]["age"])

    fig = get_pie_chart(
        df_age, "age", "n_conso", "Répartition par âge des patients traités"
    )
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return Graph(
        figure=fig,
        className="img-card",
        responsive=True,
    )


def PieCasDeclareSexe(produit) -> Graph:
    df_sexe = pd.DataFrame(med_dict[produit]["sexe"])

    if df_sexe.n_cas.sum() >= 10:
        fig = get_pie_chart(
            df_sexe, "sexe", "n_cas", "Répartition par sexe des cas déclarés"
        )
        fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
    else:
        fig = {}

    return Graph(
        figure=fig,
        className="img-card",
        responsive=True,
    )


def PieCasDeclareAge(produit) -> Graph:
    df_age = pd.DataFrame(med_dict[produit]["age"])

    if df_age.n_cas.sum() >= 10:
        fig = get_pie_chart(
            df_age, "age", "n_cas", "Répartition par âge des cas déclarés"
        )
        fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
    else:
        fig = {}

    return Graph(
        figure=fig,
        className="img-card",
        responsive=True,
    )


def CourbesAnnees(produit) -> Graph:
    df_annee = pd.DataFrame(med_dict[produit]["annee"])

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    if df_annee.n_cas.min() >= 10:
        fig.add_trace(
            go.Scatter(
                x=df_annee.annee,
                y=df_annee.n_cas,
                mode="lines",
                name="Cas déclarés",
                line={
                    "shape": "spline",
                    "smoothing": 1,
                    "width": 4,
                    "color": "#BFAACB",
                },
            ),
            secondary_y=False,
        )

    fig.add_trace(
        go.Scatter(
            x=df_annee.annee,
            y=df_annee.n_conso,
            mode="lines",
            name="Patients traités",
            line={
                "shape": "spline",
                "smoothing": 1,
                "width": 4,
                "color": "#5E2A7E",
            },
        ),
        secondary_y=True,
    )

    fig.update_yaxes(title_text="Nombre de cas déclarés", secondary_y=False)
    fig.update_yaxes(title_text="Nombre de patients traités", secondary_y=True)

    fig.update_xaxes(nticks=len(df_annee))
    fig.update_layout(
        xaxis_showgrid=False,
        yaxis_showgrid=True,
        yaxis2_showgrid=False,
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=0, b=0, l=0, r=0),
        font={"size": 12, "color": "black"},
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return Graph(
        figure=fig,
        className="img-card",
        responsive=True,
    )


def BarNotif(produit) -> Graph:
    if med_dict[produit]["notif"]:
        df_notif = pd.DataFrame(med_dict[produit]["notif"])

        fig = go.Figure(
            go.Bar(
                y=df_notif.typ_notif,
                x=df_notif.n_decla,
                orientation="h",
                marker=dict(
                    color=[
                        "rgba(51,171,102,1)",
                        "rgba(102,192,140,1)",
                        "rgba(153,213,179,1)",
                        "rgba(204,234,217,1)",
                        "rgba(191,213,60,1)",
                        "rgba(207,223,109,1)",
                        "rgba(239,244,206,1)",
                    ]
                ),
            )
        )

        fig.update_layout(
            xaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=False,
                zeroline=False,
            ),
            yaxis=dict(
                showgrid=False,
                showline=False,
                zeroline=False,
                autorange="reversed",
                ticks="outside",
                tickcolor="white",
                ticklen=1,
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=0, b=0),
            barmode="group",
            bargap=0.10,
            bargroupgap=0.0,
            font={"size": 12, "color": "black"},
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
        )
        return Graph(
            figure=fig,
            className="img-card",
            responsive=True,
        )


def BarSoc(produit) -> Graph:
    if med_dict[produit]["soclong"]:
        df_soc = pd.DataFrame(med_dict[produit]["soclong"])
        df_soc = df_soc.head(10)

        fig = go.Figure(
            go.Bar(
                y=df_soc.soc_long,
                x=df_soc.n_decla_eff,
                orientation="h",
                marker=dict(
                    color=[
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
                ),
            )
        )

        fig.update_layout(
            xaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=False,
                zeroline=False,
            ),
            yaxis=dict(
                showgrid=False,
                showline=False,
                zeroline=False,
                autorange="reversed",
                ticks="outside",
                tickcolor="white",
                ticklen=1,
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=0, b=0),
            barmode="group",
            bargap=0.10,
            bargroupgap=0.0,
            font={"size": 12, "color": "black"},
        )
        return Graph(
            figure=fig,
            className="img-card",
            responsive=True,
        )


def PatientsTraites(produit) -> Component:
    df = pd.DataFrame(med_dict[produit]["annee"])
    patients_traites = round(df.n_conso.mean())

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
                        patients_traites,
                        className="box-highlight heading-4 d-inline-block",
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
                className="box f-content d-block",
            ),
            Div(
                [
                    Div(
                        Div(
                            [
                                Div(
                                    "Répartition par sexe des patients traités",
                                    className="normal-text",
                                ),
                                PiePatientTraiteSexe(produit),
                            ],
                            className="box",
                        ),
                        className="col-xl-4 col-lg-5",
                    ),
                    Div(
                        Div(
                            [
                                Div(
                                    "Répartition par âge des patients traités",
                                    className="normal-text",
                                ),
                                PiePatientTraiteAge(produit),
                            ],
                            className="box",
                        ),
                        className="col-xl-4 col-lg-5",
                    ),
                ],
                className="row no-gutters",
            ),
        ],
        className="product-section",
    )


def CasDeclares(produit) -> Component:
    df = pd.DataFrame(med_dict[produit]["annee"])
    cas_an = round(df.n_cas.sum() / df.n_conso.sum() * 100000)

    if 0 < df.n_cas.sum() < 10:
        cas_declares = "< 10"
    else:
        cas_declares = df.n_cas.sum()

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
                                cas_an,
                                className="box-highlight heading-4 d-inline-block",
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
                                cas_declares,
                                className="box-highlight heading-4 d-inline-block",
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
                Div(
                    Div(
                        [
                            Div(
                                "Nombre de cas déclarés d'effets indésirables et patients traités par année",
                                className="normal-text",
                            ),
                            CourbesAnnees(produit),
                        ],
                        className="box",
                    ),
                    className="col-xl-8",
                ),
                className="row",
            ),
            Div(
                [
                    Div(
                        Div(
                            [
                                Div(
                                    "Répartition par sexe des cas déclarés",
                                    className="normal-text",
                                ),
                                PieCasDeclareSexe(produit),
                            ],
                            className="box",
                        ),
                        className="col-xl-4 col-lg-5",
                    ),
                    Div(
                        Div(
                            [
                                Div(
                                    "Répartition par âge des cas déclarés",
                                    className="normal-text",
                                ),
                                PieCasDeclareAge(produit),
                            ],
                            className="box",
                        ),
                        className="col-xl-4 col-lg-5",
                    ),
                    Div(
                        Div(
                            [
                                Div(
                                    "Répartition par type de notificateur",
                                    className="normal-text",
                                ),
                                BarNotif(produit),
                            ],
                            className="box",
                        ),
                        className="col-xl-8",
                    ),
                ],
                className="row",
            ),
        ],
        className="product-section",
    )


def Organes(produit) -> Component:
    return Div(
        [
            Div(
                "Effets indésirables par système d'organe",
                className="section-title heading-4",
            ),
            Div(
                Div(
                    Div(
                        [
                            P(
                                "Effets indésirables les plus déclarés par système d'organe",
                                className="normal-text",
                            ),
                            BarSoc(produit),
                        ],
                        className="box",
                    ),
                    className="col-xl-8",
                ),
                className="row",
            ),
        ],
        className="product-section",
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


def Produit(produit) -> Component:
    return Div(
        [
            SearchDiv(produit),
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
                    DescriptionProduit(produit),
                    PatientsTraites(produit),
                    CasDeclares(produit),
                    Organes(produit),
                ]
            ),
        ],
        className="side-menu-container",
    )


df_med = pd.read_csv("./data/liste_produits_substances.csv", delimiter=";")
med_list = df_med.medicament.tolist()


@app.callback(
    dd.Output("produit-search-bar", "options"),
    dd.Input("produit-search-bar", "search_value"),
)
def update_search_bar_options(search_value):
    if not search_value:
        raise PreventUpdate

    search_value = search_value.lower()
    return [
        {"label": v.lower(), "value": v} for v in med_list if search_value in v.lower()
    ]


@app.callback(
    dd.Output("produit-rechercher-button", "href"),
    dd.Input("produit-search-bar", "value"),
)
def update_path(value):
    if value:
        return "/apps/app2?search=" + value
