from typing import List

from dash.development.base_component import Component
from dash_html_components import Div, H3, Img, B, A


def FooterElement(title: str, element_list: List[str]) -> Component:
    text_element_list = [Div(title, className="heading-4 mb-4")] + [
        Div(element, className="normal-text d-block mb-3") for element in element_list
    ]
    return Div(text_element_list, className="footer-right-content")


def Logos() -> Component:
    return Div(
        [
            Div(
                [
                    Img(
                        src="/assets/1200px-Republique-francaise-logo.svg.png",
                        className="img-logo",
                    ),
                    Img(src="/assets/Ansm-logo-Grand.jpg", className="img-logo"),
                ]
            ),
            H3(
                ["data.", B("medicaments.gouv.fr")],
                style={"color": "white", "margin-top": "20px"},
            ),
        ],
        className="logos",
    )


def FooterRight():
    return Div(
        [
            FooterElement(
                "Le site", ["À propos", "Plan de site", "Mentions légales", "Contact"]
            ),
            FooterElement(
                "Partenaires",
                [
                    A("ansm.sante.fr", href="https://ansm.sante.fr/", className="link"),
                    A(
                        "base-donnees-publique.medicaments.gouv.fr",
                        href="https://base-donnees-publique.medicaments.gouv.fr/",
                        className="link",
                    ),
                    A("Etalab", href="https://www.etalab.gouv.fr/", className="link"),
                    A(
                        "La DINUM",
                        href="https://www.numerique.gouv.fr/dinum/",
                        className="link",
                    ),
                ],
            ),
        ],
        className="footer-right",
    )


def Footer() -> Component:
    return Div(
        [
            Logos(),
            FooterRight(),
        ],
        className="footer",
    )
