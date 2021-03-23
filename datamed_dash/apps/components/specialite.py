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

with zipfile.ZipFile("./data/med_dict.json.zip", "r") as z:
    filename = z.namelist()[0]
    with z.open(filename) as f:
        data = f.read()
        MED_DICT = json.loads(data.decode("utf-8"))

with zipfile.ZipFile("./data/notice_by_spe.json.zip", "r") as z:
    filename = z.namelist()[0]
    with z.open(filename) as f:
        data = f.read()
        NOTICE_BY_SPE = json.loads(data.decode("utf-8"))

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

file_sub_by_spe = open("./data/substance_by_specialite.json", "r")
SUBSTANCE_BY_SPECIALITE = json.loads(file_sub_by_spe.read())

file_liste_spe = open("./data/liste_specialites.json", "r")
SPE_DICT = json.loads(file_liste_spe.read())
SPE_LIST = list(set(SPE_DICT.keys()))

file_atc_by_spe = open("./data/atc_by_spe.json", "r")
ATC_BY_SPE = json.loads(file_atc_by_spe.read())


def SearchDiv() -> Component:
    return Div(
        [
            SearchBar("col-xl-6 col-sm-9 pl-0", "specialite-search-bar"),
            Button(
                "RECHERCHER",
                n_clicks=0,
                outline=True,
                className="col-xl-2 col-sm-2 button-text-bold",
                color="secondary",
                type="submit",
                id="specialite-rechercher-button",
            ),
        ],
        style={"margin-left": "20px", "margin-top": "2rem"},
        className="row",
    )


def DescriptionSpecialite(specialite) -> Component:
    substances_actives = ", ".join(
        SUBSTANCE_BY_SPECIALITE[specialite]["substances"]
    ).upper()
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
                            specialite,
                            className="heading-4",
                            id="Desc",
                        ),
                        Div(
                            [
                                Div(
                                    "SPÉCIALITÉ DE MÉDICAMENT",
                                    className="caption-text d-inline-block",
                                ),
                                I(
                                    className="info-icon bi bi-info-circle d-inline-block"
                                ),
                            ]
                        ),
                        Div("Substance(s) active(s)", className="small-text-bold"),
                        A(
                            substances_actives,
                            href="/",
                            className="normal-text link",
                            id="refresh-substances",
                        ),
                        Div(
                            "Description",
                            className="small-text-bold",
                        ),
                        P(
                            "Classe ATC (Anatomique, Thérapeutique et Chimique) : {} ({})".format(
                                ATC_BY_SPE[specialite]["nom_atc"],
                                ATC_BY_SPE[specialite]["code_atc"],
                            ),
                            className="normal-text",
                        ),
                        P(
                            NOTICE_BY_SPE[specialite],
                            className="normal-text mt-3",
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


def NoData() -> Div:
    return Div(
        [
            Img(
                src="/assets/illu_no_data.svg",
                className="img-fluid",
                alt="Responsive image",
            ),
            Div(
                "Données insuffisantes pour affichage",
                className="small-text",
                style={"color": "#9e9e9e"},
            ),
        ],
        className="d-flex flex-column align-items-center",
    )


def PieChart(specialite, var_1, var_2) -> Graph:
    produit = SUBSTANCE_BY_SPECIALITE[specialite]["produit"]
    df = pd.DataFrame(MED_DICT[produit][var_1])

    if var_2 == "n_cas" and df.n_cas.isnull().all():
        return NoData()

    else:
        fig = go.Figure(
            go.Pie(
                labels=df[var_1],
                values=df[var_2],
                name="Répartition par {} des patients traités".format(var_1),
                marker_colors=PIE_COLORS,
            )
        ).update_layout(
            margin=dict(t=0, b=0, l=0, r=0),
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
        )
        return Graph(
            figure=fig,
            className="img-card",
            responsive=True,
        )


def CourbesAnnees(specialite) -> Graph:
    produit = SUBSTANCE_BY_SPECIALITE[specialite]["produit"]
    df_annee = pd.DataFrame(MED_DICT[produit]["annee"])

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    if df_annee.n_cas.isnull().all():
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


def BarNotif(specialite) -> Graph:
    if MED_DICT[SUBSTANCE_BY_SPECIALITE[specialite]["produit"]]["notif"]:
        df_notif = pd.DataFrame(
            MED_DICT[SUBSTANCE_BY_SPECIALITE[specialite]["produit"]]["notif"]
        )

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
            figure=fig, className="img-card", responsive=True, style={"height": "328px"}
        )
    else:
        return NoData()


def BarSoc(specialite) -> Graph:
    if MED_DICT[SUBSTANCE_BY_SPECIALITE[specialite]["produit"]]["soclong"]:
        df_soc = pd.DataFrame(
            MED_DICT[SUBSTANCE_BY_SPECIALITE[specialite]["produit"]]["soclong"]
        )
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

        return Div(
            [
                Div(
                    Graph(
                        figure=fig,
                        className="img-card",
                        responsive=True,
                        clear_on_unhover=True,
                        id="soc-bar-chart",
                        style={"height": "472px"},
                    ),
                    id="soc-chart-container",
                ),
                Div(id="selected-soc", className="d-none"),
                HltModal(),
            ]
        )
    else:
        return NoData()


def HltModal() -> Modal:
    return Modal(
        [
            ModalHeader(id="header-modal"),
            ModalBody(id="body-modal"),
            ModalFooter(
                Button(
                    "Fermer",
                    id="close-backdrop",
                    className="ml-auto button-text-bold",
                    color="secondary",
                    outline=True,
                )
            ),
        ],
        scrollable=True,
        centered=True,
        id="update-on-click-data",
    )


def PatientsTraites(specialite) -> Component:
    produit = SUBSTANCE_BY_SPECIALITE[specialite]["produit"]
    df = pd.DataFrame(MED_DICT[produit]["annee"])
    patients_traites = round(df.n_conso.mean())

    return Div(
        [
            Div(
                [
                    Div(
                        "Patients traités",
                        className="heading-4 d-inline-block",
                        id="Pop",
                    ),
                    I(className="info-icon bi bi-info-circle d-inline-block"),
                ],
                className="section-title nav-title",
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
                                PieChart(specialite, "sexe", "n_conso"),
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
                                PieChart(specialite, "age", "n_conso"),
                            ],
                            className="box",
                        ),
                        className="col-xl-4 col-lg-5",
                    ),
                ],
                className="row no-gutters",
            ),
        ],
        className="specialite-section",
    )


def CasDeclares(specialite) -> Component:
    produit = SUBSTANCE_BY_SPECIALITE[specialite]["produit"]
    df = pd.DataFrame(MED_DICT[produit]["annee"])
    cas_an = round(df.n_cas.sum() / df.n_conso.sum() * 100000)

    if 0 <= df.n_cas.sum() < 10:
        cas_declares = "< 10"
    else:
        cas_declares = df.n_cas.sum()

    return Div(
        [
            Div(
                [
                    Div(
                        "Cas déclarés d'effets indésirables",
                        className="heading-4 d-inline-block",
                        id="Effets",
                    ),
                    I(className="info-icon bi bi-info-circle d-inline-block"),
                ],
                className="section-title nav-title ",
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
                            CourbesAnnees(specialite),
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
                                PieChart(specialite, "sexe", "n_cas"),
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
                                PieChart(specialite, "age", "n_cas"),
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
                                BarNotif(specialite),
                            ],
                            className="box",
                        ),
                        className="col-xl-8",
                    ),
                ],
                className="row",
            ),
        ],
        className="specialite-section",
    )


def Organes(specialite) -> Component:
    return Div(
        [
            Div(
                [
                    Div(
                        "Effets indésirables par système d'organe",
                        className="heading-4 d-inline-block",
                    ),
                    I(className="info-icon bi bi-info-circle d-inline-block"),
                ],
                className="section-title",
            ),
            Div(
                Div(
                    Div(
                        [
                            P(
                                "Effets indésirables les plus déclarés par système d'organe",
                                className="normal-text",
                            ),
                            BarSoc(specialite),
                        ],
                        className="box",
                    ),
                    className="col-xl-8",
                ),
                className="row",
            ),
        ],
        className="specialite-section",
    )


def Specialite(specialite) -> Component:
    return Div(
        [
            SideMenu(
                id="side-menu",
                items=[
                    {"id": "Desc", "label": "Description"},
                    {"id": "Pop", "label": "Population concernée"},
                    {"id": "Effets", "label": "Effets indésirables"},
                ],
                className="side-menu",
            ),
            SearchDiv(),
            Div(
                [
                    DescriptionSpecialite(specialite),
                    PatientsTraites(specialite),
                    CasDeclares(specialite),
                    Organes(specialite),
                ]
            ),
        ],
        className="side-menu-container",
    )


@app.callback(
    dd.Output("specialite-search-bar", "options"),
    dd.Input("specialite-search-bar", "search_value"),
)
def update_search_bar_options(search_value):
    if not search_value:
        raise PreventUpdate

    search_value = search_value.lower()
    values_list = [v for v in SPE_LIST if search_value in v.lower()][:10]
    return [
        {"label": v[:90] + "..." if len(v) > 90 else v, "value": v} for v in values_list
    ]


@app.callback(
    dd.Output("specialite-rechercher-button", "href"),
    dd.Input("specialite-search-bar", "value"),
)
def update_path(value):
    if value:
        return "/apps/app2?search=" + value


@app.callback(
    [
        dd.Output("update-on-click-data", "is_open"),
        dd.Output("body-modal", "children"),
        dd.Output("header-modal", "children"),
        dd.Output("selected-soc", "children"),
    ],
    [
        dd.Input("soc-chart-container", "n_clicks"),
        dd.Input("close-backdrop", "n_clicks"),
        dd.Input("url", "href"),
    ],
    [dd.State("selected-soc", "children"), dd.State("soc-bar-chart", "hoverData")],
)
def update_callback(
    clicks_container, clicks_close, href, previous_selected_soc, hover_data
):
    if not hover_data:
        return False, "", "", ""

    selected_soc = hover_data["points"][0]["label"]
    selected_soc_has_changed = selected_soc != previous_selected_soc

    if selected_soc_has_changed:
        parsed_url = urlparse(href)
        query = parse_qs(parsed_url.query)
        specialite = query["search"][0]

        df_hlt = pd.DataFrame(
            MED_DICT[SUBSTANCE_BY_SPECIALITE[specialite]["produit"]]["hlt"]
        )
        df_hlt = df_hlt.rename(
            columns={"effet_hlt": "Détail des effets rapportés par nombre décroissant"}
        )
        df_hlt_details = df_hlt[df_hlt.soc_long == selected_soc][
            ["Détail des effets rapportés par nombre décroissant"]
        ]
        return (
            True,
            Table.from_dataframe(
                df_hlt_details,
                striped=True,
                bordered=True,
                hover=True,
                responsive=True,
            ),
            selected_soc,
            selected_soc,
        )
    else:
        return False, "", "", ""
