from typing import Union
from urllib.parse import parse_qs, ParseResultBytes, ParseResult

from dash_html_components import Div

from .components.footer import Footer
from .components.navbar import Navbar
from .components.produit import Produit


def Layout(parsed_url: Union[ParseResultBytes, ParseResult]):
    query = parse_qs(parsed_url.query)
    specialite = query["search"][0]

    return Div(
        [
            Navbar(),
            Produit(specialite),
            Footer(),
        ],
        className="layout",
        id="layout_produit",
    )
