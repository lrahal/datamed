from dash_html_components import Div

from .components.donnees_une import DonneesUne
from .components.footer import Footer
from .components.main_search import MainSearch
from .components.navbar import Navbar
from .components.plateforme import Plateforme

layout = Div(
    [
        Navbar(),
        MainSearch(),
        DonneesUne(),
        Plateforme(),
        Footer(),
    ],
    className="layout",
    id="layout_landing_page",
)
