from dash import dcc, html
from dash.dash_table import DataTable
from dash.development.base_component import Component
import dash_bootstrap_components as dbc
#TODO: Add Fade Objects for Explanations

def render_layout() -> Component:
    return dbc.Container(
        children=[
            html.Header("Analyses", className="custom-header"),
            dbc.Card(
                children=[
                    dbc.CardBody(
                        children=[
                            html.H3("Upload Data"),
                            dbc.Row(
                                children=[
                                    dbc.Col(
                                        children=[
                                            dcc.Upload(
                                                id="upload-gene",
                                                children=html.Button("Upload Gene Data"),
                                                multiple=False,
                                                className="upload-custom"
                                            ),
                                            dcc.Store(id="store-gene"),
                                        ]
                                    ),
                                    dbc.Col(
                                        children=[
                                            dcc.Upload(
                                                id="upload-meta",
                                                children=html.Button("Upload Meta Data"),
                                                multiple=False,
                                                className="upload-custom"
                                            ),
                                            dcc.Store(id="store-meta"),
                                        ]
                                    )
                                ]
                            ),
                        ]
                    )
                ]
            ),
            dbc.Card(
                children=[
                    dbc.CardBody(
                        children=[
                            html.H3("Gene Data"),
                            DataTable(
                                id="gene-data",
                                columns=[],
                                data=[],
                            ),
                            html.Div(id="container-gene"),
                            dcc.Dropdown(
                                id="excluded-genes",
                                options=[],
                                placeholder="Select Genes to Exclude",
                                multi=True,
                                optionHeight=50,
                                className="dropdown-darkmode",
                                clearable=True,
                                style={
                                    "background-color": "#303030",  # Dark grey background
                                    "color": "#CCCCCC",  # Light grey text color
                                    "border": "none",  # No border
                                    "box-shadow": "none",  # No box shadow
                                    "marginTop": "15px",
                                    "marginBottom": "15px",
                                },
                            ),
                            html.Div(id="container-excluded-genes"),
                            dcc.Store(id="store-gene-options"),
                            dcc.Store(id="store-excluded-genes"),
                        ]
                    )
                ]
            ),
            dbc.Card(
                children=[
                    dbc.CardBody(
                        children=[
                            html.H3("Meta Data"),
                            dbc.Card(
                                dbc.CardBody(
                                    children=[
                                        html.H4("Group A"),
                                        dbc.Input(placeholder="Name Group A", id="input-name-a", type="text", className="custom-input"),
                                        dcc.Store(id="store-a"),
                                        DataTable(
                                            id="table-a",
                                            columns=[],
                                            data=[],
                                            page_action="native",
                                            page_size=10,
                                            fixed_rows={"headers": False},
                                            export_format="csv",
                                            virtualization=True,
                                            filter_action="custom",
                                            style_table={'overflowX': 'auto', 'overflowY': 'auto', 'maxHeight': '300px'},
                                            style_header={
                                                "backgroundColor": "rgb(30, 30, 30)",
                                                "color": "white",
                                            },
                                            style_data={
                                                "backgroundColor": "rgb(50, 50, 50)",
                                                "color": "white",
                                            },
                                        ),
                                        dcc.Store(id="store-a-table"),
                                    ]
                                )
                            ),
                            dbc.Card(
                                dbc.CardBody(
                                    children=[
                                        html.H4("Group B"),
                                        dbc.Input(placeholder="Name Group B", id="input-name-b", type="text", className="custom-input"),
                                        dcc.Store(id="store-b"),
                                        DataTable(
                                            id="table-b",
                                            columns=[],
                                            data=[],
                                            page_action="native",
                                            page_size=10,
                                            fixed_rows={"headers": False},
                                            export_format="csv",
                                            virtualization=True,
                                            filter_action="custom",
                                            style_table={'overflowX': 'auto', 'overflowY': 'auto', 'maxHeight': '300px'},
                                            style_header={
                                                "backgroundColor": "rgb(30, 30, 30)",
                                                "color": "white",
                                            },
                                            style_data={
                                                "backgroundColor": "rgb(50, 50, 50)",
                                                "color": "white",
                                            },
                                        ),
                                        dcc.Store(id="store-b-table"),
                                    ]
                                )
                            ),
                        ]
                    )
                ]
            ),
            dbc.Card(
                children=[
                    dbc.CardBody(
                        children=[
                            html.H3("Finalize Analysis"),
                            dbc.Input(id="input-analysis", type="text", placeholder="Name Analysis", className="custom-input"),
                            dbc.FormText("Include Control Genes in Analysis?"),
                            dbc.Checklist(
                                id="controlgenes",
                                options=[
                                    {"label": "Control Genes", "value": True},
                                ],
                                value=[True],
                                switch=True,
                                style={"marginBottom": "15px"},
                            ),
                            dcc.Store(id="store-controlgenes"),
                            dcc.Store(id="store-analysis"),
                            dbc.Textarea(
                                id="box-description",
                                placeholder="Insert Notes or Description here",
                                style={"width": "100%", "height": 300, "marginBottom": "10px"},
                            ),
                            dcc.Store(id="store-description"),
                            dbc.Button("Start Analysis", id="start-analysis", n_clicks=0),
                            html.Div(id="storage"),
                        ]
                    )
                ]
            ),
        ],
        fluid=True
    )
