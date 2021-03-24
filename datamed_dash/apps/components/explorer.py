from dash.development.base_component import Component
from dash_bootstrap_components import Card, CardImg, CardBody, CardLink
from dash_html_components import Div, B


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
                "bases de données. Laissez-vous guider par ses modalités d’utilisation.",
                className="explorer-text large-text",
            ),
        ],
        className="explorer-header-container",
    )


def BddCard(
    src_img: str, title: str, open_data: str, body: str, source_bdd: str, href: str
) -> Card:
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
                                    B("Source de données : "),
                                    source_bdd,
                                ],
                                className="button-text d-inline-block col-6",
                            ),
                        ],
                        className="d-flex row mt-4 mb-5",
                    ),
                    CardLink(
                        "DÉCOUVRIR LE JEU DE DONNÉES",
                        href=href,
                        className="normal-text link",
                    ),
                ],
                className="px-4",
            ),
        ],
        className="explorer-card",
    )


def Modalites() -> Component:
    return Div(
        [
            Div(
                "Modalités d'utilisation",
                className="heading-4 text-center",
            )
        ],
        style={"margin-top": "376px"},
    )


def Explorer() -> Component:
    return Div(
        [
            ExplorerHeader(),
            BddCard(
                "/assets/ansm_entree.svg",
                "Cartographie des sites de fabrication",
                "Non",
                "Surveillez les ruptures de stock et trouvez des alternatives thérapeutiques en fonction du profil du "
                "patient concerné.",
                "État des lieux des laboratoires pharmaceutiques (ANSM)",
                "/apps/ruptures",
            ),
            BddCard(
                "/assets/pills_2.svg",
                "Observatoire des ruptures de stock",
                "Non",
                "Découvrez les indicateurs observés par les agents de l’ANSM pour anticiper les ruptures de stock et "
                "les actions mises en place pour y pallier.",
                "TrustMed (ANSM)",
                "/apps/explorer",
            ),
            Modalites(),
        ]
    )
