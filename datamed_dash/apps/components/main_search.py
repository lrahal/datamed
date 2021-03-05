import dash.dependencies as dd
from dash.development.base_component import Component
from dash.exceptions import PreventUpdate
from dash_bootstrap_components import Button, Row, Col
from dash_core_components import Dropdown
from dash_html_components import Div, Span
import pandas as pd
from app import app


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
        className="search-bar ml-auto flex-nowrap",
        align="center",
    )


def MainSearch() -> Component:
    return Div(
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
                    className="button-text-bold mr-1",
                    color="secondary",
                    id="rechercher-button",
                    type="submit",
                    style={"margin-top": "3rem"},
                ),
            ],
            className="main-search",
        ),
        className="main-search-container",
    )


df_med = pd.read_csv("./data/liste_produits_substances.csv", delimiter=";")
med_list = df_med.medicament.tolist()


@app.callback(
    dd.Output("search-bar", "options"),
    dd.Input("search-bar", "search_value"),
)
def update_search_bar_options(search_value):
    if not search_value:
        raise PreventUpdate

    search_value = search_value.lower()
    return [
        {"label": v.lower(), "value": v} for v in med_list if search_value in v.lower()
    ]


@app.callback(
    dd.Output("rechercher-button", "href"),
    dd.Input("search-bar", "value"),
)
def update_path(value):
    if value:
        return "/apps/app2?search=" + value
