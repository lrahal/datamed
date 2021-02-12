import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.development.base_component import Component
from dash.dependencies import Output, Input

from app1_init import app


def _get_page_heading() -> Component:
    src = '/assets/logo_ansm.png'
    sticky_style = {
        'position': 'absolute',
        'height': '88px',
        'left': '0px',
        'top': '0px',
        'border': '1px solid  #9E9E9E',
        'width': '100%',
        'border-right': 'none',
        'border-left': 'none',
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
        style={'display': 'inline-block'},
        className='navbar-dropdown',
    )
    nav = html.Span(
        [
            dbc.NavbarBrand(
                ["data.", html.B("ansm.sante.fr")],
                className="ml-2",
                style={'color': 'black', 'display': 'inline-block', "font-size": "15px"}),
            html.Span(
                [
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
                    dbc.Button("Contact", outline=True, className="mr-1", color="primary")]
            ),
        ],
        className='navbar-span'
    )
    img = html.Img(src=src, style={'width': '100px', 'display': 'inline-block'})
    return html.Div(html.Div([dcc.Link(img, href='/'), nav], className='container'), style=sticky_style)


app.layout = html.Div(
    [dcc.Location(id='url', refresh=False), _get_page_heading(),
     html.Div(id='page-content', className='container')],
    id='layout',
)

if __name__ == '__main__':
    app.run_server(debug=True)

