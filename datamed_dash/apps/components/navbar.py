import dash_core_components as dcc
from dash.development.base_component import Component
from dash_bootstrap_components import Button, DropdownMenu, DropdownMenuItem
from dash_html_components import Div, Img, Span, A, B


def LogoAnsm() -> Component:
    src = '/assets/logo_ansm.png'
    img = Img(src=src, style={'width': '100px', 'display': 'inline-block'})
    return dcc.Link(img, href='/')


def UrlAnsm() -> Component:
    return Span(
        ["data.", B("ansm.sante.fr")],
        className="ml-2 d-inline-block text-dark",
    )


def MenuItem(title: str, href: str) -> Component:
    return A(
        title,
        href=href,
        className='nav-link text-secondary d-inline-block',
    )


def DropDown() -> Component:
    return DropdownMenu(
        label="Explorer",
        children=[
            DropdownMenuItem("Cartographie"),
            DropdownMenuItem("Erreurs médicamenteuses"),
            DropdownMenuItem("Effets indésirables"),
        ],
        className='navbar-dropdown d-inline-block',
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
                            MenuItem('Analyses thématiques', '/'),
                            DropDown(),
                            MenuItem('À propos', '/'),
                            Button("CONTACT", outline=True, className="mr-1", color="primary")],
                        className='navbar-menu',
                    ),
                ],
                className='navbar-span'
            )
        ],
        className='navbar-layout container-fluid d-flex'
    )
