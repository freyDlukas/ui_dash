from dash import dcc, html
from dash.dash_table import DataTable
from dash.development.base_component import Component


def Container(*children: Component) -> Component:
    return html.Div(
        children,
        style={
            "max-width": "100vw",
        },
    )


def halfContainer(*children: Component) -> Component:
    return html.Div(
        children,
        style={
            "max-width": "50vw",
        },
    )


def Column(*children: Component) -> Component:
    return html.Div(
        children,
        style={
            "display": "flex",
            "flex-direction": "column",
        },
    )


def Row(*children: Component) -> Component:
    return html.Div(
        children,
        style={
            "display": "flex",
            "flex-direction": "row",
        },
    )


def render_layout() -> Component:
    return Container(
        html.H1("Analyses"),
        html.Div(
            [
                html.H3("Upload Data"),
                html.Div(
                    [
                        html.Div(
                            [
                                html.P("Upload Gene Data"),
                                dcc.Upload(
                                    id="upload-gene",
                                    children=html.Button("Upload Gene Data"),
                                    multiple=False,
                                ),  # genedata
                                html.Br(),
                                dcc.Store(id="store-gene"),
                                html.Div(
                                    id="container-gene"
                                ),  # show genedata (snippet)
                                html.Hr(),
                            ]
                        ),
                        html.Div(
                            [
                                html.P("Upload Metadata"),
                                dcc.Upload(
                                    id="upload-meta",
                                    children=html.Button("Upload Meta Data"),
                                    multiple=False,
                                ),  # metadata
                                html.Br(),
                                dcc.Store(id="store-meta"),  # metadata
                                html.Hr(),
                            ]
                        ),
                    ]
                ),
            ]
        ),
        html.Div(
            [
                html.H3("Group A"),
                dcc.Input(placeholder="Name Group A", id="input-name-a", type="text"),
                dcc.Store(id="store-a"),
                DataTable(
                    id="table-a",
                    columns=[],
                    data=[],
                    page_action="native",
                    page_size=15,
                    export_format="csv",
                    virtualization=True,
                    filter_action="custom",
                ),
                # dcc.Store(id="Group-A-demo-table"),
                html.Hr(),
            ]
        ),
        html.Div(
            [
                html.H3("Group B"),
                dcc.Input(placeholder="Name Group B", id="input-name-b", type="text"),
                dcc.Store(id="store-b"),
                html.Div(id=""),
                # dcc.Store(id="Group-B-meta-data-table"),
                html.Hr(),
            ]
        ),
        html.Div(
            [
                html.H3("Finalyze Analyses"),
                dcc.Input(id="Analysis-Name", type="text", placeholder="Name Analysis"),
                dcc.Store(id="input-name-analyze"),
                html.Hr(),
            ]
        ),
        html.Div(
            [
                html.Br(),
                html.Button("Start Analysis", id="Start-Analysis"),
            ]
        ),
    )
