from dash_html_components import Div, Img, Span, A
from dash.development.base_component import Component


def Arrow() -> Component:
    return A(
        [
            Img(src="/assets/arrow_downward_grey.svg", className="mb-3"),
            Span("OU EXPLOREZ DAVANTAGE", style={"font-size": "18px", "font-weight": "400"}),
        ],
        className="arrow",
        href="#donnees-une"
    )
