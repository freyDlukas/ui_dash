import dash
from dash import html, dcc

dash.register_page(__name__, order=3)

layout = html.Div(
    [
        html.H3("Group B"),
        dcc.Input(placeholder="Name Group B", id="Name-Group-B", type="text"),
        dcc.Store(id="Group-B-Store"),
        html.Div(id="meta-data-table-B"),
    ]
)
