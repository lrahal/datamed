from dash.development.base_component import Component
from dash_bootstrap_components import Button, Row, Col, Input
from dash_html_components import Div, A


def SearchBar() -> Component:
    return Row(
        [
            Col(Input(type="search", placeholder="Médicament, substance active")),
        ],
        no_gutters=True,
        className="ml-auto flex-nowrap mt-3",
        align="center",
    )


def MainSearch() -> Component:
    return Div(
        Div([
            A(
                "Trouvez des données autour du médicament",
                style={"font-size": "30px", 'margin-top': '5rem'}
            ),
            SearchBar(),
            Button("RECHERCHER", outline=True, className="mr-1", color="secondary",
                   style={'margin-top': '3rem'})
        ],
            className='main-search'
        ),
        className='main-search-container'
    )
