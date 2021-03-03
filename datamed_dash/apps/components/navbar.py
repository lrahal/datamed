import dash_core_components as dcc
from dash.development.base_component import Component
from dash_bootstrap_components import Button, DropdownMenu, DropdownMenuItem
from dash_html_components import Div, Img, Span, A, B


def LogoAnsm() -> Component:
    src = "/assets/logo_ansm.png"
    img = Img(src=src, style={"width": "100px", "display": "inline-block"})
    return dcc.Link(img, href="/")


def UrlAnsm() -> Component:
    return Span(
        ["data.", B("ansm.sante.fr")],
        style={"color": "black"},
        className="ml-2 d-inline-block",
    )


def MenuItem(title: str, href: str) -> Component:
    return A(
        title,
        href=href,
        className="nav-link text-secondary d-inline-block mr-4",
    )


def DropDown() -> Component:
    return DropdownMenu(
        label="Explorer",
        children=[
            DropdownMenuItem("Cartographie"),
            DropdownMenuItem("Erreurs médicamenteuses"),
            DropdownMenuItem("Effets indésirables"),
        ],
        className="navbar-dropdown d-inline-block mr-4",
    )


def Navbar() -> Component:
    return Div(
        [
            LogoAnsm(),
            Div(
                [
                    UrlAnsm(),
                    Div(
                        [
                            MenuItem("Analyses thématiques", "/"),
                            DropDown(),
                            Div(className="vl mr-4"),
                            MenuItem("À propos", "/"),
                            Button(
                                "CONTACT",
                                outline=True,
                                className="mr-1",
                                color="primary",
                            ),
                        ],
                        className="navbar-menu",
                    ),
                ],
                className="navbar-span",
            ),
        ],
        className="navbar-layout container-fluid d-flex sticky-top",
    )
