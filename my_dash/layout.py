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
                                html.Br(),
                                dcc.Input(
                                    id="excluded-genes",
                                    type="text",
                                    placeholder=" Genes to exclude",
                                    multiple = True,
                                    list = "store-gene-options",
                                    autoComplete = "on",

                                ),
                                html.Br(),
                                html.Br(),
                                html.Div(id="container-excluded-genes"),
                                html.Br(),
                                dcc.Store(id="store-gene-options"),
                                dcc.Store(id="store-excluded-genes"),
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
                html.Br(),
                dcc.Store(id="store-a"),
                html.Br(),
                html.P("Use the \"|\" symbol to filter for multiple values"),
                html.Br(),
                DataTable(
                    id="table-a",
                    columns=[],
                    data=[],
                    page_action="native",
                    page_size=15,
                    fixed_rows={"headers": True},
                    export_format="csv",
                    virtualization=True,
                    filter_action="custom",
                ),
                dcc.Store(id="store-a-table"),
                html.Hr(),
            ]
        ),
        html.Div(
            [
                html.H3("Group B"),
                dcc.Input(placeholder="Name Group B", id="input-name-b", type="text"),
                html.Br(),
                dcc.Store(id="store-b"),
                html.Br(),
                html.P("Use the \"|\" symbol to filter for multiple values"),
                html.Br(),
                DataTable(
                    id="table-b",
                    columns=[],
                    data=[],
                    page_action="native",
                    page_size=15,
                    fixed_rows={"headers": True},
                    export_format="csv",
                    virtualization=True,
                    filter_action="custom",
                ),
                dcc.Store(id="store-b-table"),
                html.Hr(),
            ]
        ),
        html.Div(
            [
                html.H3("Finalyze Analyses"),
                dcc.Input(
                    id="input-analysis", type="text", placeholder="Name Analysis"
                ),
                html.Br(),
                html.P("Include Control Genes in Analysis?"),
                dcc.RadioItems([
                    {'label': 'Yes', 'value': 'True'},
                    {'label': 'No', 'value': 'False'}, 
                ],
                value = 'True',
                inline= True,
                id = "controlgenes"
                ),
                dcc.Store(id="store-controlgenes"),
                html.Br(),
                dcc.Store(id="store-analysis"),
                html.Br(),
                dcc.Textarea(
                    id="box-description",
                    placeholder="Insert Notes or Description here",
                    style={"width": "100%", "height": 300},
                ),
                dcc.Store(id="store-description"),
                html.Hr(),
            ]
        ),
        html.Div(
            [
                html.Br(),
                html.Button("Start Analysis", id="start_analysis", n_clicks=0),
                html.Br(),
                html.Div(id="storage"),
            ]
        ),
    )
