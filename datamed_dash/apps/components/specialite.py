import json
import zipfile
from typing import List
from urllib.parse import urlparse, parse_qs, urlencode, quote_plus, unquote_plus

import dash.dependencies as dd
import dash_table
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
    Tooltip,
    Jumbotron,
)
from dash_core_components import Graph
from dash_html_components import Div, A, P, Img, I
from plotly.subplots import make_subplots
from sm import SideMenu

from .main_search import SearchBar
from ..constants.colors import PIE_COLORS, BAR_CHART_COLORS
from ..constants.layouts import BAR_LAYOUT, CURVE_LAYOUT, PIE_LAYOUT

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

file_sub_by_spe = open("./data/substance_by_specialite.json", "r")
SUBSTANCE_BY_SPECIALITE = json.loads(file_sub_by_spe.read())

file_liste_spe_sa = open("./data/spe_sa_dict.json", "r")
SPE_SA_DICT = json.loads(file_liste_spe_sa.read())

file_atc_by_spe = open("./data/atc_by_spe.json", "r")
ATC_BY_SPE = json.loads(file_atc_by_spe.read())


def SearchDiv() -> Component:
    return Div(
        Div(
            [
                SearchBar("input-group-content mr-3 pl-0", "specialite-search-bar"),
                Div(
                    Div(
                        Button(
                            "RECHERCHER",
                            n_clicks=0,
                            outline=True,
                            className="button-text-bold",
                            color="secondary",
                            type="submit",
                            id="specialite-rechercher-button",
                            style={"min-width": "fit-content"},
                        )
                    ),
                    className="input-group-append",
                ),
            ],
            className="input-group col-xl-8",
        ),
        style={"padding-left": "20px", "margin-top": "2rem"},
        className="row",
        id="Desc",
    )


def SubstanceLinks(substances_list: List[str]) -> Component:
    return Div(
        [
            A(
                sa.upper(),
                href="/apps/specialite?{}".format(
                    urlencode({"search": quote_plus(sa)})
                ),
                className="normal-text link d-block",
                id="refresh-substances",
            )
            for sa in substances_list
        ]
    )


def SpecialiteDiv(selected_med: str, substances_list) -> Component:
    tooltip_text = (
        "Les médicaments peuvent être regroupés suivant différents niveaux de "
        "précision (du plus au moins précis) : la présentation (Doliprane "
        "1000 mg, comprimé, boîte de 8 comprimés), la spécialité (Doliprane "
        "1000 mg, comprimé), le produit (Doliprane), la substance active "
        "(Paracétamol). La spécialité d’un médicament est donc caractérisée par "
        "une dénomination spéciale (Doliprane) et un conditionnement "
        "particulier (1000 mg, comprimé)."
    )
    rcp_link = (
        "https://base-donnees-publique.medicaments.gouv.fr/affichageDoc.php?specid="
        + SUBSTANCE_BY_SPECIALITE[selected_med]["cis"][0]
        + "&typedoc=R"
    )
    notice_link = (
        "https://base-donnees-publique.medicaments.gouv.fr/affichageDoc.php?specid="
        + SUBSTANCE_BY_SPECIALITE[selected_med]["cis"][0]
        + "&typedoc=N"
    )
    return Div(
        Div(
            Div(
                [
                    Div(
                        I(
                            className="bi bi-book d-flex justify-content-center pt-3",
                            style={"font-size": "3rem"},
                        ),
                        className="position-absolute",
                    ),
                    Div(
                        [
                            Div(
                                selected_med,
                                className="heading-4",
                            ),
                            Div(
                                [
                                    Div(
                                        "SPÉCIALITÉ DE MÉDICAMENT",
                                        className="caption-text d-inline-block",
                                    ),
                                    I(
                                        className="info-icon bi bi-info-circle d-inline-block",
                                        id="specialite-info-icon",
                                    ),
                                    Tooltip(
                                        tooltip_text,
                                        target="specialite-info-icon",
                                        placement="right",
                                    ),
                                ]
                            ),
                            Div(
                                "Substance(s) active(s)",
                                className="small-text-bold",
                            ),
                            SubstanceLinks(substances_list),
                            Div(
                                "Description",
                                className="small-text-bold",
                            ),
                            P(
                                "Classe ATC (Anatomique, Thérapeutique et Chimique) : {} ({})".format(
                                    ATC_BY_SPE[selected_med]["nom_atc"],
                                    ATC_BY_SPE[selected_med]["code_atc"],
                                ),
                                className="normal-text",
                            ),
                            P(
                                NOTICE_BY_SPE[selected_med],
                                className="normal-text text-justify mt-3",
                            ),
                            Div(
                                [
                                    A(
                                        "Afficher le RCP",
                                        href=rcp_link,
                                        className="normal-text link d-inline-block",
                                        id="refresh-substances",
                                    ),
                                    A(
                                        "Afficher la notice",
                                        href=notice_link,
                                        className="normal-text link d-inline-block ml-5",
                                        id="refresh-substances",
                                    ),
                                ],
                                style={"margin-top": "34px"},
                            ),
                        ],
                        className="pr-5",
                        style={"padding-left": "70px"},
                    ),
                ],
                className="description",
            ),
            className="col-xl-8",
        ),
        style={"margin-top": "31.5px"},
        className="topic-section row no-gutters",
    )


def SubstanceDiv(selected_med: str, spe_dataframe: pd.DataFrame) -> Component:
    return Div(
        Div(
            Div(
                [
                    Div(
                        I(
                            className="bi bi-book d-flex justify-content-center pt-3",
                            style={"font-size": "3rem"},
                        ),
                        className="position-absolute",
                    ),
                    Div(
                        [
                            Div(
                                selected_med,
                                className="heading-4",
                            ),
                            Div(
                                [
                                    Div(
                                        "SUBSTANCE ACTIVE",
                                        className="caption-text d-inline-block",
                                    ),
                                    I(
                                        className="info-icon bi bi-info-circle d-inline-block",
                                        id="substance-info-icon",
                                    ),
                                    Tooltip(
                                        "Composant d'une spécialité pharmaceutique reconnu "
                                        "comme possédant des propriétés thérapeutiques.",
                                        target="substance-info-icon",
                                        placement="right",
                                    ),
                                ]
                            ),
                            Div(
                                "Spécialités de médicaments contenant : {}".format(
                                    selected_med
                                ),
                                className="medium-text mt-5",
                            ),
                            Div(
                                "{} médicaments identifiés".format(len(spe_dataframe)),
                                className="normal-text mt-3",
                                style={"color": "#33C2D6"},
                            ),
                            dash_table.DataTable(
                                id="substance-specialite-table",
                                columns=[
                                    {"name": i, "id": i} for i in spe_dataframe.columns
                                ],
                                data=spe_dataframe.to_dict("records"),
                                page_size=10,
                                style_as_list_view=True,
                                style_table={"overflowX": "auto"},
                                style_cell={
                                    "height": "40px",
                                },
                                style_data={
                                    "fontSize": "12px",
                                    "fontWeight": "400",
                                    "font-family": "Roboto",
                                    "lineHeight": "16px",
                                    "textAlign": "left",
                                },
                                style_header={"display": "none"},
                            ),
                        ],
                        className="pr-5",
                        style={"padding-left": "70px"},
                    ),
                ],
                className="description",
            ),
            className="col-xl-8",
        ),
        style={"margin-top": "31.5px"},
        className="topic-section row no-gutters",
    )


def DescriptionSpecialite(selected_med: str) -> Component:
    if SPE_SA_DICT[selected_med] == "spécialité":
        substances_actives = ", ".join(
            SUBSTANCE_BY_SPECIALITE[selected_med]["substances"]
        ).upper()
        substances_list = SUBSTANCE_BY_SPECIALITE[selected_med]["substances"]
        return SpecialiteDiv(selected_med, substances_list)
    else:
        selected_med_spe_list = [
            k
            for k, values in SUBSTANCE_BY_SPECIALITE.items()
            for v in values["substances"]
            if selected_med in v
        ]
        selected_med_spe_list.sort()

        df = pd.DataFrame(
            selected_med_spe_list,
            columns=["Spécialités de médicaments contenant : {}".format(selected_med)],
        )
        return SubstanceDiv(selected_med, df)


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


def PieChart(medicament: str, var_1: str, var_2: str) -> Graph:
    df = pd.DataFrame(MED_DICT[medicament][var_1])

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
        ).update_layout(PIE_LAYOUT)
        return Graph(
            figure=fig,
            className="img-card",
            responsive=True,
        )


def SingleCurve(x: pd.Series, y: pd.Series, name: str, color: str) -> go.Scatter:
    return go.Scatter(
        x=x,
        y=y,
        mode="lines",
        name=name,
        line={
            "shape": "spline",
            "smoothing": 1,
            "width": 4,
            "color": color,
        },
    )


def CourbesAnnees(medicament: str) -> Graph:
    df_annee = pd.DataFrame(MED_DICT[medicament]["annee"])

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    if df_annee.n_cas.min() >= 10:
        fig.add_trace(
            SingleCurve(df_annee.annee, df_annee.n_cas, "Cas déclarés", PIE_COLORS[1]),
            secondary_y=False,
        )

    fig.add_trace(
        SingleCurve(
            df_annee.annee, df_annee.n_conso, "Patients traités", PIE_COLORS[2]
        ),
        secondary_y=True,
    )

    fig.update_yaxes(title_text="Nombre de cas déclarés", secondary_y=False)
    fig.update_yaxes(title_text="Nombre de patients traités", secondary_y=True)

    fig.update_xaxes(nticks=len(df_annee))

    fig.update_layout(CURVE_LAYOUT)
    return Graph(
        figure=fig,
        className="img-card",
        responsive=True,
    )


def BarNotif(medicament: str) -> Graph:
    if MED_DICT[medicament]["notif"]:
        df_notif = pd.DataFrame(MED_DICT[medicament]["notif"])

        fig = go.Figure(
            go.Bar(
                y=df_notif.typ_notif,
                x=df_notif.n_decla,
                orientation="h",
                marker=dict(color=BAR_CHART_COLORS),
            )
        )
        fig.update_layout(BAR_LAYOUT)
        return Graph(
            figure=fig, className="img-card", responsive=True, style={"height": "328px"}
        )
    else:
        return NoData()


def BarSoc(medicament: str) -> Graph:
    if MED_DICT[medicament]["soclong"]:
        df_soc = pd.DataFrame(MED_DICT[medicament]["soclong"])
        df_soc = df_soc.head(10)

        fig = go.Figure(
            go.Bar(
                y=df_soc.soc_long,
                x=df_soc.n_decla_eff,
                orientation="h",
                marker=dict(color=BAR_CHART_COLORS),
            )
        )

        fig.update_layout(BAR_LAYOUT)

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


def SectionTitle(
    title: str, icon_id: str, tooltip_text: str, side_menu_id: str
) -> Component:
    return Div(
        [
            Div(
                title,
                className="heading-4 d-inline-block",
            ),
            I(className="info-icon bi bi-info-circle d-inline-block", id=icon_id),
            Tooltip(
                tooltip_text,
                target=icon_id,
                placement="right",
            ),
        ],
        className="section-title nav-title",
        id=side_menu_id,
    )


def Indicateur(
    value: float, units: str, description: str, class_name: str
) -> Component:
    return Div(
        [
            Div(
                value,
                className="box-highlight heading-4 d-inline-block",
            ),
            Div(
                units,
                className="box-highlight heading-4 d-inline-block ml-2",
            ),
            Div(
                description,
                className="normal-text",
            ),
        ],
        className=class_name,
        style={"max-width": "390px"},
    )


def PatientsTraites(selected_med: str) -> Component:
    if SPE_SA_DICT[selected_med] == "spécialité":
        medicament = SUBSTANCE_BY_SPECIALITE[selected_med]["produit"]
        jumbotron = Div(
            Jumbotron(
                [
                    Div("Note d'attention", className="medium-text"),
                    Div(
                        "Les données affichées ci-dessous sont l'agrégations des données de "
                        "toutes les spécialités de médicament rattachées au produit : [{}]".format(
                            medicament
                        ),
                        className="normal-text mt-3",
                    ),
                ],
                className="col-xl-8 p-3 mb-2",
            ),
            className="row patients-traites-jumbotron",
        )
    else:
        medicament = selected_med
        jumbotron = []

    df = pd.DataFrame(MED_DICT[medicament]["annee"])
    patients_traites = round(df.n_conso.mean())

    tooltip_text = (
        "Nombre de patients par présentation ayant eu au moins un remboursement dans l’année cumulé par "
        "produit/substance active. Estimations obtenues à partir des données Open-Medic ("
        "https://www.etalab.gouv.fr/licence-ouverte-open-licence) portant sur l’usage du médicament, "
        "délivré en pharmacie de ville en 2014 à 2018 et remboursé par l’Assurance Maladie. Pour plus "
        "d’informations, consultez : http://open-data-assurance-maladie.ameli.fr/medicaments/index.php "
        "Attention : Les patients étant restitués par présentation dans les données Open Medic, ils sont "
        "comptabilisés autant de fois qu’ils ont eu de remboursements de présentations différentes d’un même"
        " produit/substance active. Les indicateurs restitués pourraient être surestimés pour certains "
        "médicaments."
    )

    return Div(
        [
            jumbotron,
            Div(
                [
                    Div(
                        "Patients traités",
                        className="heading-4 d-inline-block",
                    ),
                    I(
                        className="info-icon bi bi-info-circle d-inline-block",
                        id="patients-traites-info-icon",
                    ),
                    Tooltip(
                        tooltip_text,
                        target="patients-traites-info-icon",
                        placement="right",
                    ),
                ],
                className="section-title",
                id="Pop",
            ),
            Indicateur(
                patients_traites,
                "patients/an",
                "Nombre moyen de patients traités par an sur la période 2014/2018",
                "box f-content d-block",
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
                                PieChart(medicament, "sexe", "n_conso"),
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
                                PieChart(medicament, "age", "n_conso"),
                            ],
                            className="box",
                        ),
                        className="col-xl-4 col-lg-5",
                    ),
                ],
                className="row no-gutters",
            ),
        ],
        className="topic-section",
    )


def CasDeclares(selected_med: str) -> Component:
    if SPE_SA_DICT[selected_med] == "spécialité":
        medicament = SUBSTANCE_BY_SPECIALITE[selected_med]["produit"]
    else:
        medicament = selected_med

    df = pd.DataFrame(MED_DICT[medicament]["annee"])
    cas_an = round(df.n_cas.sum() / df.n_conso.sum() * 100000)

    if 0 <= df.n_cas.sum() < 10:
        cas_declares = "< 10"
    else:
        cas_declares = df.n_cas.sum()

    tooltip_text = (
        "Nombre de cas notifiés d’effets indésirables (EI) en France estimé à partir des données de la Base "
        "Nationale de PharmacoVigilance (BNPV). La BNPV est alimentée par les centres régionaux de pharmacovigilance"
        " qui sont notifiés par les professionnels de santé ou par les patients et association agréées via un "
        "portail dédié : XX. Sont notifiés les EI que le patient ou son entourage suspecte d’être liés à l’utilisation "
        "d’un ou plusieurs médicaments et les mésusages, abus ou erreurs médicamenteuses. Il s’agit de cas évalués et "
        "validés par un comité d’experts. Pour plus d’informations, consultez : "
        "https://ansm.sante.fr/page/la-surveillance-renforcee-des-medicaments Attention : Les cas déclarés par produit "
        "ne tiennent pas compte de cas potentiels déclarés au niveau de la substance active "
        "(environ 20% des observations)."
    )

    return Div(
        [
            SectionTitle(
                "Cas déclarés d'effets indésirables",
                "cas-declares-info-icon",
                tooltip_text,
                "Effets",
            ),
            Indicateur(
                cas_an,
                "cas/an",
                "Taux de déclaration pour 100 000 patients traités sur la période 2014/2018",
                "box d-inline-block",
            ),
            Indicateur(
                cas_declares,
                "cas déclarés",
                "Nombre de cas déclarés sur la période 2014/2018",
                "box d-inline-block",
            ),
            Div(
                Div(
                    Div(
                        [
                            Div(
                                "Nombre de cas déclarés d'effets indésirables et patients traités par année",
                                className="normal-text",
                            ),
                            CourbesAnnees(medicament),
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
                                PieChart(medicament, "sexe", "n_cas"),
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
                                PieChart(medicament, "age", "n_cas"),
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
                                BarNotif(medicament),
                            ],
                            className="box",
                        ),
                        className="col-xl-8",
                    ),
                ],
                className="row",
            ),
        ],
        className="topic-section",
    )


def Organes(selected_med: str) -> Component:
    if SPE_SA_DICT[selected_med] == "spécialité":
        medicament = SUBSTANCE_BY_SPECIALITE[selected_med]["produit"]
    else:
        medicament = selected_med

    tooltip_text = (
        "Systèmes d’organes (SOC) avec le plus d’effets indésirables déclarés. En cliquant sur les barres latérales, "
        "vous pourrez connaître le détail des EI déclarés pour chaque SOC. Attention : un cas n'est comptabilisé "
        "qu’une seule fois par SOC en cas de plusieurs EI affectant le même SOC. Un cas peut en revanche être "
        "comptabilisé sur plusieurs SOC différents (en fonction des EI déclarés)."
    )
    return Div(
        [
            SectionTitle(
                "Effets indésirables par système d'organes",
                "organes-info-icon",
                tooltip_text,
                "",
            ),
            Div(
                Div(
                    Div(
                        [
                            P(
                                "Effets indésirables les plus déclarés par système d'organes",
                                className="normal-text",
                            ),
                            BarSoc(medicament),
                        ],
                        className="box",
                    ),
                    className="col-xl-8",
                ),
                className="row",
            ),
        ],
        className="topic-section",
    )


def Specialite(selected_med: str) -> Component:
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
                    DescriptionSpecialite(selected_med),
                    PatientsTraites(selected_med),
                    CasDeclares(selected_med),
                    Organes(selected_med),
                ]
            ),
        ],
        className="side-menu-container",
    )


@app.callback(
    dd.Output("specialite-search-bar", "options"),
    dd.Input("specialite-search-bar", "search_value"),
)
def update_search_bar_options(search_value: str):
    if not search_value:
        raise PreventUpdate

    search_value = search_value.lower()

    values_list = [v for v in SPE_SA_DICT.keys() if v.lower().startswith(search_value)]
    values_list.sort()
    values_list = sorted(values_list, key=len)
    return [
        {"label": v[:90] + "..." if len(v) > 90 else v, "value": v} for v in values_list
    ]


@app.callback(
    dd.Output("specialite-rechercher-button", "href"),
    dd.Input("specialite-search-bar", "value"),
)
def update_path(value: str):
    if value:
        return "/apps/specialite?" + urlencode({"search": quote_plus(value)})


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
        parsed_url = urlparse(unquote_plus(href))
        query = parse_qs(parsed_url.query)
        selected_med = query["search"][0]

        if SPE_SA_DICT[selected_med] == "spécialité":
            medicament = SUBSTANCE_BY_SPECIALITE[selected_med]["produit"]
        else:
            medicament = selected_med

        df_hlt = pd.DataFrame(MED_DICT[medicament]["hlt"])
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


@app.callback(
    dd.Output("url", "href"),
    dd.Input("substance-specialite-table", "active_cell"),
    dd.State("substance-specialite-table", "data"),
)
def getActiveCell(active_cell, data):
    if active_cell:
        col = active_cell["column_id"]
        row = active_cell["row"]
        cellData = data[row][col]
        return "/apps/specialite?" + urlencode({"search": quote_plus(cellData)})
    else:
        raise PreventUpdate
