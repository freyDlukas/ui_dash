import dash
from dash import html, dcc

dash.register_page(__name__, order=1)

layout = (
    html.Div(
        [
            html.H1("Upload Files"),
            html.Div(
                [
                    html.Div(
                        [
                            html.P("Upload Gene Data"),
                            dcc.Upload(
                                id="upload-gene-data",
                                children=html.Button("Upload Gene Data"),
                                multiple=False,
                            ),  # genedata
                            html.Br(),
                            dcc.Store(id="gene-data-store"),
                            html.Div(id="gene-data-loaded"),  # show genedata (snippet)
                            html.Hr(),
                            html.P("Upload Metadata"),
                            dcc.Upload(
                                id="upload-meta-data",
                                children=html.Button("Upload Meta Data"),
                                multiple=False,
                            ),  # metadata
                            html.Br(),
                            dcc.Store(id="meta-data-store"),
                            html.Div(id="meta-data-loaded"),  # metadata (filtered)
                        ]
                    ),
                ]
            ),
        ]
    ),
)
