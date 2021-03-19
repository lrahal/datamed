import json


import dash.dependencies as dd
from app import app
from dash.development.base_component import Component
from dash.exceptions import PreventUpdate
from dash_bootstrap_components import Button, Row, Col
from dash_core_components import Dropdown
from dash_html_components import Div, Span


file_liste_spe = open("./data/liste_specialites.json", "r")
SPE_DICT = json.loads(file_liste_spe.read())
SPE_LIST = list(set(SPE_DICT.keys()))


def MainSearchTitle() -> Component:
    return Div(
        [Div("Plateforme des données publiques"), Div("de l'Agence du Médicament")],
        className="main-search-title heading-4"
    )


def SearchBar() -> Component:
    return Row(
        [
            Col(
                Dropdown(
                    id="search-bar",
                    placeholder="Médicament, substance active",
                    className="normal-text main-dropdown",
                )
            ),
        ],
        no_gutters=True,
        className="search-bar ml-auto flex-nowrap mt-4",
        align="center",
    )


def MainSearch() -> Component:
    return Div(
        [
            MainSearchTitle(),
            Div(
                [
                    Span(
                        "Trouvez des données",
                        className="heading-4 d-block",
                    ),
                    Span(
                        "autour du médicament",
                        className="heading-4 d-block",
                    ),
                    SearchBar(),
                    Button(
                        "RECHERCHER",
                        n_clicks=0,
                        outline=True,
                        className="button-text-bold",
                        color="secondary",
                        id="rechercher-button",
                        type="submit",
                        style={"margin-top": "2.5rem"},
                    ),
                ],
                className="main-search",
            ),
        ],
        className="main-search-container",
    )


@app.callback(
    dd.Output("search-bar", "options"),
    dd.Input("search-bar", "search_value"),
)

def update_search_bar_options(search_value):
    if not search_value:
        raise PreventUpdate


    search_value = search_value.lower()
    values_list = [v for v in SPE_LIST if search_value in v.lower()][:10]
    return [
        {"label": v[:50]+"..." if len(v)>50 else v, "value": v} for v in values_list
    ]


@app.callback(
    dd.Output("rechercher-button", "href"),
    dd.Input("search-bar", "value"),
)
def update_path(value):
    if value:
        return "/apps/app2?search=" + value
