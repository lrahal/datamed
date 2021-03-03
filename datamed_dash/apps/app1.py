from dash_html_components import Div

from .components.donnees_une import DonneesUne
from .components.footer import Footer
from .components.main_search import MainSearch
from .components.navbar import Navbar
from .components.plateforme import Plateforme
from .components.arrow import Arrow
import pandas as pd

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

df_med = pd.read_csv("./data/liste_produits_substances.csv", delimiter=";")
