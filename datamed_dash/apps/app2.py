from typing import Union
from urllib.parse import parse_qs, ParseResultBytes, ParseResult

from dash.development.base_component import Component
from dash_html_components import Div

from .components.footer import Footer
from .components.navbar import Navbar
from .components.specialite import Specialite


def Layout(parsed_url: Union[ParseResultBytes, ParseResult]) -> Component:
    query = parse_qs(parsed_url.query)
    selected_med = query["search"][0]

    return Div(
        [
            Navbar(),
            Specialite(selected_med),
            Footer(),
        ],
        className="layout",
        id="layout_specialite",
    )
