from dash.development.base_component import Component
from dash_html_components import Div

from .components.footer import Footer
from .components.navbar import Navbar
from .components.explorer import Explorer


def Layout() -> Component:
    return Div(
        [
            Navbar(),
            Explorer(),
            Footer(),
        ],
        className="layout",
        id="layout_explorer",
    )
