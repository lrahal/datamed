import dash_core_components as dcc
from dash_html_components import Div

from app1_init import app
from components.donnees_une import DonneesUne
from components.main_search import MainSearch
from components.plateforme import Plateforme
from components.navbar import Navbar

app.layout = Div(
    [
        dcc.Location(id='url', refresh=False),
        Navbar(),
        MainSearch(),
        DonneesUne(),
        Plateforme(),
        Div(id='page-content', className='container')
    ],
    id='layout',
)

if __name__ == '__main__':
    app.run_server(debug=True)
