from dash_html_components import Div

from .components.footer import Footer
from .components.navbar import Navbar
from .components.produit import DescriptionProduit

layout = Div(
    [
        Navbar(),
        DescriptionProduit(),
        Footer(),
    ],
    className='layout',
    id='layout_produit',
)
