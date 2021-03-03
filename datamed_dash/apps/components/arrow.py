from dash_html_components import Div, Img, Span
from dash.development.base_component import Component


def Arrow() -> Component:
    return Div(
        [
            Img(src="/assets/arrow_downward_grey.svg", className="mb-3"),
            Span("OU EXPLOREZ DAVANTAGE", style={"font-size": "1.15rem"}),
        ],
        className="arrow",
    )
