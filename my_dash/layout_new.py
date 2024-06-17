from dash import dcc, html
from dash.dash_table import DataTable
from dash.development.base_component import Component
import dash_bootstrap_components as dbc
#DONE: Add Fade Objects for Explanations
########TODO: Add Pages one for explanation and one for the actual analysis, FAQ Page?, Contact Page?
########TODO: Navbar for the pages
##TODO: Add loading spinner
#DONE: Input Mail for the user
#TODO: Send Mail to user with link to the results page / make results page on website? (Download Button?)
#DONE: Add Section for the user to specify the Analysis
    #DONE: Switch if user wants Graphs or just the results
    #DONE: Deseq2 and/or Limma, EdgeR?
    #DONE: Define Dataset for GSEA?
#TODO: ADD OFFcanvas for more Information

def render_layout() -> Component:
    return dbc.Container(
        children=[
            html.Header(
                children=[
                    "Analysis",
                    dbc.Button("Help", id="help-toggle", color="primary", className="help-button")
                ],
                className="custom-header"
            ),
            dbc.Card(
                children=[
                    dbc.CardBody(
                        children=[
                            html.H3("Upload Data"),
                            dbc.Alert(
                                "Upload your Gene Data and Meta Data files either by Drag and Drop or by clicking the buttons below. Use CSV or Excel Sheet.",
                                id="alert-upload",
                                is_open=True,
                                dismissable=True,
                                className="custom-alert",
                            ),
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
                            dbc.Alert(
                                "Select Genes to Exclude from the Analysis. You can also search for genes by typing.",
                                id="alert-gene",
                                is_open=True,
                                dismissable=True,
                                className="custom-alert",
                            ),
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
                            dbc.Alert(
                                "Use the | symbol to filter for multiple Values in a single column. For example: Value1|Value2|Value3",
                                id="alert-meta",
                                is_open=True,
                                dismissable=True,
                                className="custom-alert meta",
                            ),
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
                            html.H3("Analysis Settings"),
                            dbc.Alert(
                                "Hover over Components to get more Info.",
                                id="alert-tooltip",
                                is_open=True,
                                dismissable=True,
                                className="custom-alert analyse-settings",
                            ),
                            dbc.Checklist(
                                id="check-controlgenes",
                                options=[
                                    {"label": "Control Genes", "value": True},
                                ],
                                value=[],
                                switch=True,
                                style={"marginBottom": "15px"},
                                className="custom-checklist",
                            ),
                            dbc.Tooltip(
                                "Activate Switch to include Control Genes in the Analysis.",
                                target="check-controlgenes",
                                placement="top-start",
                            ),
                            dcc.Store(id="store-controlgenes"),
                            dbc.Checklist(
                                id="check-graphs",
                                options=[
                                    {"label": "Graphs", "value": True},
                                ],
                                value=[True],
                                switch=True,
                                style={"marginBottom": "15px"},
                                className="custom-checklist",
                            ),
                            dcc.Store(id="store-graphs"),
                            dbc.Tooltip(
                                "Deactivte if you just want the Result Tables without Graphs.",
                                target="check-graphs",
                                placement="top-start",
                            ),
                            dbc.Checklist(
                                options=[
                                    {"label": "DESeq2", "value": "DESeq2"},
                                    {"label": "Limma", "value": "Limma"},
                                    {"label": "EdgeR", "value": "EdgeR"},
                                ],
                                id="check-dea",
                                value=["DESeq2"],
                                inline=False,
                                className="custom-checker",
                                style={"backgroundColor": "#1c1c1c", "padding": "10px"},
                            ),
                            dbc.Tooltip(
                                "Select the \"Differential Expression Analysis\"-Tool you want to use. You can select multiple Tools, but the Analysis will take longer.",
                                target="check-dea",
                                placement="top-start", 
                            ),
                            dcc.Store(id="store-dea"),
                            dbc.Input(id="input-gsea", type="text", placeholder="GSEA Dataset", className="custom-input"),
                            dcc.Store(id="store-gsea"),
                            dbc.Tooltip(
                                "Type in the Name of the Dataset, which you want to use for Gene Set Enrichment Analysis. \n"
                                "For example: GO_Biological_Process_2018, KEGG_2019_Human, Reactome_2016",
                                target="input-gsea",
                                placement="top-start",
                            ),
                        ]
                    ),
                ]
            ),
            dbc.Card(
                children=[
                    dbc.CardBody(
                        children=[
                            html.H3("Finalize Analysis"),
                            dbc.Input(id="input-analysis", type="text", placeholder="Name Analysis", className="custom-input"),
                            dcc.Store(id="store-analysis"),
                            dbc.Textarea(
                                id="box-description",
                                placeholder="Insert Notes or Description here",
                                style={"width": "100%", "height": 300, "marginBottom": "10px"},
                            ),
                            dcc.Store(id="store-description"),
                            dbc.Input(id="input-email", type="email", placeholder="Your Email", className="custom-input"),
                            dcc.Store(id="store-email"),
                            dbc.Button("Start Analysis", id="start-analysis", n_clicks=0),
                            html.Div(id="storage"),
                        ]
                    )
                ]
            ),
        ],
        fluid=True
    )
