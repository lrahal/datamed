import json
from urllib.parse import urlencode, quote_plus

import dash.dependencies as dd
from app import app
from dash.development.base_component import Component
from dash.exceptions import PreventUpdate
from dash_bootstrap_components import Button
from dash_core_components import Dropdown
from dash_html_components import Div, Span, Form

file_liste_spe_sa = open("./data/spe_sa_dict.json", "r")
SPE_SA_DICT = json.loads(file_liste_spe_sa.read())


def MainSearchTitle() -> Component:
    return Div(
        [Div("Plateforme des données publiques"), Div("de l'Agence du Médicament")],
        className="main-search-title heading-4",
    )


def SearchBar(search_bar_class_names: str, search_bar_id: str) -> Component:
    return Form(
        Dropdown(
            id=search_bar_id,
            placeholder="Médicament (par spécialité), substance active",
            className="normal-text main-dropdown",
            style = {'background-color': '#E8E8E8'}
        ),
        autoComplete="off",
        className=search_bar_class_names,
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
                    SearchBar(
                        "search-bar ml-auto flex-nowrap mt-4 align-items-center",
                        "search-bar",
                    ),
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

    values_list = [v for v in SPE_SA_DICT.keys() if v.lower().startswith(search_value)]
    if (len(values_list)<10):
        values_list = values_list + [v for v in SPE_SA_DICT.keys() if search_value in v.lower()][:(10-len(values_list))]
    values_list.sort()
    values_list = sorted(values_list, key=len)

    return [
        {"label": v[:50] + "..." if len(v) > 50 else v, "value": v} for v in values_list
    ]


@app.callback(
    dd.Output("rechercher-button", "href"),
    dd.Input("search-bar", "value"),
)
def update_path(value):
    if value:
        return "/apps/specialite?" + urlencode({"search": quote_plus(value)})
