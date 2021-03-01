from dash_html_components import Div

from .components.navbar import Navbar
from .components.produit import DescriptionProduit

layout = Div(
    [
        Navbar(),
        DescriptionProduit(),
    ],
    className='layout',
    id='layout_produit',
)
