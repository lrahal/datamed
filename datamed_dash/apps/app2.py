from dash_html_components import Div

from .components.footer import Footer
from .components.navbar import Navbar
from .components.produit import DescriptionProduit, PatientsTraites

layout = Div(
    [
        Navbar(),
        DescriptionProduit(),
        PatientsTraites(),
        Footer(),
    ],
    className="layout",
    id="layout_produit",
)
