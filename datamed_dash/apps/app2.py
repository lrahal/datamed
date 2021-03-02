from dash_html_components import Div

from .components.footer import Footer
from .components.navbar import Navbar
from .components.produit import DescriptionProduit, PatientsTraites, CasDeclares, Organes

layout = Div(
    [
        Navbar(),
        DescriptionProduit(),
        PatientsTraites(),
        CasDeclares(),
        Organes(),
        Footer(),
    ],
    className="layout",
    id="layout_produit",
)
