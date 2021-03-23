from dash_html_components import Div

from .components.arrow import Arrow
from .components.donnees_une import DonneesUne
from .components.footer import Footer
from .components.main_search import MainSearch
from .components.navbar import Navbar
from .components.plateforme import Plateforme

layout = Div(
    [
        Navbar(),
        MainSearch(),
        Arrow(),
        DonneesUne(),
        Plateforme(),
        Footer(),
    ],
    className="layout",
    id="layout_landing_page",
)
