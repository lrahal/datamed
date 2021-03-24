from dash.development.base_component import Component
from dash_html_components import Div


def ExplorerHeader() -> Component:
    return Div(
        [
            Div(
                "Explorez notre sélection de données publiques",
                className="explorer-title heading-4",
            ),
            Div(
                "L’Agence Nationale de Sécurité du Médicament et des "
                "Produits de Santé met à votre disposition une sélection de ses "
                "bases de données. Laissez-vous guider par ses modalités d’utilisation",
                className="explorer-text large-text",
            ),
        ],
        className="explorer-header-container",
    )


def Explorer() -> Component:
    return Div([ExplorerHeader()])
