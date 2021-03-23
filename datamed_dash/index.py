from urllib.parse import urlparse

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

from app import app, server
from apps import app1, app2

app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


@app.callback(Output("page-content", "children"), Input("url", "href"))
def display_page(href):
    parsed_url = urlparse(href)
    pathname = parsed_url.path

    if pathname == "/apps/accueil":
        return app1.layout
    elif pathname == "/apps/specialite":
        return app2.Layout(parsed_url)
    else:
        return app1.layout


if __name__ == "__main__":
    app.run_server(debug=True)
