from dash.development.base_component import Component
from dash_html_components import Div

from .components.footer import Footer
from .components.navbar import Navbar
from .components.ruptures import Ruptures


def Layout() -> Component:
    return Div(
        [
            Navbar(),
            Ruptures(),
            Footer(),
        ],
        className="layout",
        id="layout_ruptures",
    )
