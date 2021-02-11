import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.development.base_component import Component
from dash.dependencies import Output, Input

from app1_init import app


ANSM_LOGO = "https://ansm.sante.fr/design/afssaps/images/header/ansm_logo.gif"


def _get_page_heading() -> Component:
    src = '/assets/logo_ansm.png'
    navbar = dbc.Navbar(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=ANSM_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("data.ansm.sante.fr", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="https://ansm.sante.fr/",
            ),
        ],
        color="white",
        dark=True,
    )
    return navbar


def _get_page_heading_simple() -> Component:
    src = '/assets/logo_ansm.png'
    sticky_style = {
        'position': 'absolute',
        'width': '1200px',
        'height': '88px',
        'left': '0px',
        'top': '0px',
        'border': '1px solid  #9E9E9E',
        'display': 'flex',
        'align-items': 'center',
    }
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Analyses thématiques", href="#")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Cartographie", href="#"),
                    dbc.DropdownMenuItem("Erreurs médicamenteuses", href="#"),
                    dbc.DropdownMenuItem("Effets indésirables", href="#"),
                ],
                nav=True,
                in_navbar=True,
                label="Explorer",
            ),
        ],
        brand="data.ansm.sante.fr",
        brand_href="#",
        color="#808080",
        dark=True,
        style={'display': 'inline-block'},
    )
    img = html.Img(src=src, style={'width': '100px', 'display': 'inline-block'})
    return html.Div(html.Div([dcc.Link(img, href='/'), navbar], className='container'), style=sticky_style)


def _get_page_heading_en() -> Component:
    src = '/assets/logo_ansm.png'
    sticky_style = {
        'position': 'absolute',
        'width': '1200px',
        'height': '88px',
        'left': '0px',
        'top': '0px',
        'border': '1px solid  #9E9E9E',
        'display': 'flex',
        'align-items': 'center',
    }
    dropdown = dbc.DropdownMenu(
        label="Explorer",
        children=[
            dbc.DropdownMenuItem("Cartographie"),
            dbc.DropdownMenuItem("Erreurs médicamenteuses"),
            dbc.DropdownMenuItem("Effets indésirables"),
        ],
        color='#808080',
        style={'display': 'inline-block'},
    )
    nav = html.Span(
        [
            dbc.NavbarBrand("data.ansm.sante.fr", className="ml-2",
                            style={'color': 'black', 'display': 'inline-block', "font-size": "15px"}),
            html.Span(
                html.A(
                    'Analyses thématiques',
                    href='/',
                    className='nav-link',
                    style={'color': 'grey', 'display': 'inline-block'})
            ),
            dropdown,
            html.Span(
                html.A(
                    'À propos',
                    href='/',
                    className='nav-link',
                    style={'color': 'grey', 'display': 'inline-block'})
            ),
            dbc.Button("Contact", outline=True, className="mr-1", style={'color': '#a03189'}),
        ],
        style={'display': 'inline-block'},
    )
    img = html.Img(src=src, style={'width': '100px', 'display': 'inline-block'})
    return html.Div(html.Div([dcc.Link(img, href='/'), nav], className='container'), style=sticky_style)


app.layout = html.Div(
    [dcc.Location(id='url', refresh=False), _get_page_heading_en(),
     html.Div(id='page-content', className='container')],
    id='layout',
)

if __name__ == '__main__':
    app.run_server(debug=True)

