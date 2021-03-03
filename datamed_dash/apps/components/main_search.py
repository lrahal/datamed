from dash.dependencies import Input, Output
from dash.development.base_component import Component
from dash_bootstrap_components import Button, Row, Col, Input
from dash_html_components import Div, Span
from app import app


def SearchBar() -> Component:
    return Row(
        [
            Col(Input(type="search", placeholder="Médicament, substance active")),
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
                    style={"font-size": "34px", "display": "block"},
                ),
                Span(
                    "autour du médicament",
                    style={"font-size": "34px", "display": "block"},
                ),
                SearchBar(),
                Button(
                    "RECHERCHER",
                    n_clicks=0,
                    outline=True,
                    className="mr-1",
                    color="secondary",
                    id="rechercher-button",
                    style={"margin-top": "3rem"},
                    href="/apps/app2",
                ),
            ],
            className="main-search",
        ),
        className="main-search-container",
    )


# @app.callback(
#     Output('location', 'pathname'),
#     [Input('rechercher-button', 'n_clicks')]
# )
# def update_path(n_clicks):
#     return "/path"
