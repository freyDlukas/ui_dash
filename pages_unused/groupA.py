import dash
from dash import html, dcc

dash.register_page(__name__, order=2)

layout = html.Div(
    [
        html.H3("Group A"),
        dcc.Input(placeholder="Name Group A", id="Name-Group-A", type="text"),
        dcc.Store(id="Group-A-Store"),
        html.Div(id="meta-data-table-A"),
    ]
)
