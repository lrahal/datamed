from dash_html_components import Div
from urllib.parse import urlparse, parse_qs, ParseResultBytes, ParseResult
from typing import Union

from .components.footer import Footer
from .components.navbar import Navbar
from .components.produit import Produit

def Layout(parsed_url: Union[ParseResultBytes, ParseResult]):
    query = parse_qs(parsed_url.query)
    produit = query["search"][0]

    return Div(
        [
            Navbar(),
            Produit(produit),
            Footer(),
        ],
        className="layout",
        id="layout_produit",
    )
