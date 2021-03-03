from dash_html_components import Div

from .components.footer import Footer
from .components.navbar import Navbar
from .components.produit import Produit

layout = Div(
    [
        Navbar(),
        Produit(),
        Footer(),
    ],
    className="layout",
    id="layout_produit",
)
