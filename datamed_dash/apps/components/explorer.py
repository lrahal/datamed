from dash.development.base_component import Component
from dash_html_components import Div, B
from dash_bootstrap_components import Button, Card, CardImg, CardBody, CardLink


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


def BddCard(src_img, title, open_data, body, source_bdd) -> Card:
    return Card(
        [
            CardImg(src=src_img, style={"width": "270px", "height": "240px"}),
            CardBody(
                [
                    Div(title, className="heading-6"),
                    Div(["Open data : ", open_data], className="small-text"),
                    Div(
                        [
                            Div(
                                body,
                                className="button-text d-inline-block col-6",
                            ),
                            Div(
                                [
                                    B("Source de données :"),
                                    source_bdd,
                                ],
                                className="button-text d-inline-block col-6",
                            ),
                        ],
                        className="d-flex row mt-4 mb-5",
                    ),
                    CardLink(
                        "DÉCOUVRIR LE JEU DE DONNÉES",
                        href="/apps/ruptures",
                        className="normal-text link",
                        id="link-donnees-ruptures",
                    ),
                ],
                className="px-4",
            ),
        ],
        className="explorer-card",
        style={"width": "956px"},
    )


def Explorer() -> Component:
    return Div(
        [
            ExplorerHeader(),
            BddCard(
                "/assets/screen.jpg",
                "Cartographie des sites de fabrication",
                "Non",
                "Surveillez les ruptures de stock et trouvez des alternatives thérapeutiques en fonction du profil du "
                "patient concerné.",
                "ANSM, Base de données publique des médicaments",
            ),
        ]
    )
