import base64
import io
import os

import pandas as pd
from dash import Input, Output, State, dash_table


from .app import app

#FIXME: not working on linux yet (create folder)
#TODO: Logging (1 at least one dea has to be selected, 2 check if 2 different files are uploaded, ...)
#NOTE: If Control Genes = True include them if empty list exclude them

# Define data types and excluded columns
types = {
    "id": "numeric",
    "Complaint_ID": "numeric",
    "ZIP_code": "numeric",
    "Date_received": "datetime",
    "Date_sent_to_company": "datetime",
}
excluded_columns = ["ID", "name"]

# Callback to toggle alerts
@app.callback(
    [
        Output("alert-upload", "is_open"),
        Output("alert-gene", "is_open"),
        Output("alert-meta", "is_open"),
        Output("alert-tooltip", "is_open"),
    ],
    [Input("help-toggle", "n_clicks")],
    [
        State("alert-upload", "is_open"),
        State("alert-gene", "is_open"),
        State("alert-meta", "is_open"),
        State("alert-tooltip", "is_open"),
    ]
)
def toggle_alerts(n_clicks, is_open_upload, is_open_gene, is_open_meta, is_open_tooltip):
    if n_clicks:
        # If all alerts are open, close all alerts
        if is_open_upload and is_open_gene and is_open_meta and is_open_tooltip:
            return False, False, False, False
        else:
            # If any alert is closed, open all alerts
            return True, True, True, True
    # Default to return the current state of the alerts
    return is_open_upload, is_open_gene, is_open_meta, is_open_tooltip


@app.callback(Output("store-analysis", "data"), Input("input-analysis", "value"))
def name_analysis(value):
    if value is None:
        return "Analysis"
    else:
        return value


# Store Group A Name
@app.callback(Output("store-a", "data"), Input("input-name-a", "value"))
def name_group_a(value):
    if value is None:
        return "Group A"
    else:
        return value


# Store Group B Name
@app.callback(Output("store-b", "data"), Input("input-name-b", "value"))
def name_group_b(value):
    if value is None:
        return "Group B"
    else:
        return value


# store notes/description box
@app.callback(Output("store-description", "data"), Input("box-description", "value"))
def store_description(value):
    if value is None:
        return "No Description"
    else:
        return value
    
# store control genes yes/no
@app.callback(Output("store-controlgenes", "data"), Input("check-controlgenes", "value"))
def store_controlgenes(value):
    return value

#store include Graphs
@app.callback(Output("store-graphs", "data"), Input("check-graphs", "value"))
def store_graphs(value):
    return value

#store Diff Expressions Analyse
@app.callback(Output("store-dea", "data"), Input("check-dea", "value"))
def store_dea(value):
    return value

#store Gene Set Enrichment Analysis
@app.callback(Output("store-gsea", "data"), Input("input-gsea", "value"))

#store Email
@app.callback(Output("store-email", "data"), Input("input-email", "value"))
def store_email(value):
    if value is None:
        return
    else:
        return value

# Callback to read uploaded gene file and store it
@app.callback(
    Output("store-gene", "data"),
    Input("upload-gene", "contents"),
    State("upload-gene", "filename"),
)
def read_genedata(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        # Determine file extension
        file_extension = os.path.splitext(filename)[1].lower()
        # Read uploaded file into DataFrame based on file extension
        if file_extension == ".csv":
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), sep="\t")
        elif file_extension in [".xls", ".xlsx"]:
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return None
        # Convert DataFrame to JSON and return
        return df.to_json(orient="records")


# show gene file
@app.callback(Output("container-gene", "children"), Input("store-gene", "data"))
def display_genedata(data):
    if data is None:
        return "No Input"
    # Load data from store
    loaded_gene_data = pd.read_json(data, orient="records")
    # Display loaded data
    return dash_table.DataTable(
        data=loaded_gene_data.to_dict("records"),
        columns=[{"name": i, "id": i} for i in loaded_gene_data.columns],
        page_size=10,
        style_table={"overflowX": "auto"},
        style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white'
        },
        style_data={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white'
        },
    )
# Populate gene options in dropdown
@app.callback(
    Output("excluded-genes", "options"), 
    Input("store-gene", "data")
)
def populate_gene_options(data):
    if data is None:
        return []
    # Load data from store
    loaded_gene_data = pd.read_json(data, orient="records")
    # Create list for dropdown options
    options = [{"label": gene, "value": gene} for gene in loaded_gene_data.iloc[:,0].tolist()]
    return options


#store excluded genes
@app.callback(
    Output("store-excluded-genes", "data"),
    Input("excluded-genes", "value"),
)
def store_excluded_genes(value):
    if value is None:
        return []
    return value

# show excluded genes
@app.callback(
    Output("container-excluded-genes", "children"),
    Input("excluded-genes", "value"),
)
def display_excluded_genes(value):
    if value is None:
        return "No Genes Excluded"
    else:
        return f'Following Genes are excluded from the Analysis: {value}'

# Callback to read uploaded meta file and store it
@app.callback(
    Output("store-meta", "data"),
    Input("upload-meta", "contents"),
    State("upload-meta", "filename"),
)
def read_metadata(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        # Determine file extension
        file_extension = os.path.splitext(filename)[1].lower()
        # Read uploaded file into DataFrame based on file extension
        if file_extension == ".csv":
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), sep="\t")
        elif file_extension in [".xls", ".xlsx"]:
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return None
        # Convert DataFrame to JSON and return
        return df.to_json(orient="records")


# #Data Table for Group A
@app.callback(
    [Output("table-a", "data"), Output("table-a", "columns")],
    Input("store-meta", "data"),
)
def on_meta_upload_a(data):
    if data is None:
        return [], []
    # Load data from store
    df = pd.read_json(data, orient="records")
    columns = [{"id": col, "name": col} for col in df.columns]
    rows = df.to_dict("records")
    return rows, columns


@app.callback(
    Output("table-a", "data", allow_duplicate=True),
    [Input("table-a", "derived_filter_query_structure"), Input("store-meta", "data")],
    prevent_initial_call=True,
)
def onFilterUpdate_a(derived_query_structure, data):
    if data is None:
        return []
    df = pd.read_json(data, orient="records")
    return filter_df(df, derived_query_structure)


# store table A
@app.callback(Output("store-a-table", "data"), Input("table-a", "data"))
def store_table_a(data):
    if data is None:
        return []
    df = pd.DataFrame.from_dict(data)
    return df.to_json(orient="records")


# Data Table for Group B
@app.callback(
    [Output("table-b", "data"), Output("table-b", "columns")],
    Input("store-meta", "data"),
)
def on_meta_upload_b(data):
    if data is None:
        return [], []
    # Load data from store
    df = pd.read_json(data, orient="records")
    columns = [{"id": col, "name": col} for col in df.columns]
    rows = df.to_dict("records")
    return rows, columns


@app.callback(
    Output("table-b", "data", allow_duplicate=True),
    [Input("table-b", "derived_filter_query_structure"), Input("store-meta", "data")],
    prevent_initial_call=True,
)
def onFilterUpdate_b(derived_query_structure, data):
    if data is None:
        return []
    df = pd.read_json(data, orient="records")
    return filter_df(df, derived_query_structure)


# store table B
@app.callback(Output("store-b-table", "data"), Input("table-b", "data"))
def store_table_b(data):
    if data is None:
        return []
    df = pd.DataFrame.from_dict(data)
    return df.to_json(orient="records")


# Funcs for filtering Table A & B
def filter_df(df, derived_query_structure):
    (pd_query_string, df_filtered) = construct_filter(derived_query_structure, df)

    if pd_query_string != "":
        df_filtered = df_filtered.query(pd_query_string)

    return df_filtered.to_dict("records")


def to_string(filter):
    operator_type = filter.get("type")
    operator_subtype = filter.get("subType")

    if operator_type == "relational-operator":
        if operator_subtype == "=":
            return "=="
        else:
            return operator_subtype
    elif operator_type == "logical-operator":
        if operator_subtype == "&&":
            return "&"
        else:
            return "|"
    elif (
        operator_type == "expression"
        and operator_subtype == "value"
        and isinstance(filter.get("value"), str)
    ):
        return '"{}"'.format(filter.get("value"))
    else:
        return filter.get("value")


def construct_filter(derived_query_structure, df, complexOperator=None):
    # there is no query; return an empty filter string and the
    # original dataframe
    if derived_query_structure is None:
        return ("", df)

    # the operator typed in by the user; can be both word-based or
    # symbol-based
    operator_type = derived_query_structure.get("type")

    # the symbol-based representation of the operator
    operator_subtype = derived_query_structure.get("subType")

    # the LHS and RHS of the query, which are both queries themselves
    left = derived_query_structure.get("left", None)
    right = derived_query_structure.get("right", None)

    # the base case
    if left is None and right is None:
        return (to_string(derived_query_structure), df)

    # recursively apply the filter on the LHS of the query to the
    # dataframe to generate a new dataframe
    (left_query, left_df) = construct_filter(left, df)

    # apply the filter on the RHS of the query to this new dataframe
    (right_query, right_df) = construct_filter(right, left_df)

    # 'datestartswith' and 'contains' can't be used within a pandas
    # filter string, so we have to do this filtering ourselves
    if complexOperator is not None:
        right_query = right.get("value")
        # perform the filtering to generate a new dataframe
        if complexOperator == "datestartswith":
            return (
                "",
                right_df[right_df[left_query].astype(str).str.startswith(right_query)],
            )
        elif complexOperator == "contains":
            return (
                "",
                right_df[right_df[left_query].astype(str).str.contains(right_query)],
            )

    if operator_type == "relational-operator" and operator_subtype in [
        "contains",
        "datestartswith",
    ]:
        return construct_filter(
            derived_query_structure, df, complexOperator=operator_subtype
        )

    # construct the query string; return it and the filtered dataframe
    return (
        "{} {} {}".format(
            left_query,
            to_string(derived_query_structure)
            if left_query != "" and right_query != ""
            else "",
            right_query,
        ).strip(),
        right_df,
    )


###start analysis button /Users/lukas-danielf/Documents/PathologieMarburg/dashtest/dashtest/store_cache
# save Stores to files
# json
@app.callback(
    [Output("storage", "children"),
     Output("container-analysis", "children"),
     Output("start-analysis", "disabled")],
    Input("start-analysis", "n_clicks"),
    [
        State("store-a", "data"),
        State("store-b", "data"),
        State("store-description", "data"),
        State("store-analysis", "data"),
        State("store-gene", "data"),
        State("store-meta", "data"),
        State("store-a-table", "data"),
        State("store-b-table", "data"),
        State("store-excluded-genes", "data"),
        State("store-controlgenes", "data"),
        State("store-graphs", "data"),
        State("store-dea", "data"),
        State("store-email", "data"),
        State("store-gsea", "data"),
    ]
)
def handle_analysis(
    n_clicks, group_a, group_b, description, analysis, gene, meta, table_a, table_b, excluded_genes, control_genes, graphs, dea, email, gsea
):
    if n_clicks > 0:
        # Check if any critical files are missing
        if not all([group_a, group_b, analysis, gene, meta, table_a, table_b, dea]):
            return "Error: Some files are missing.", "", False

        path = "/Users/lukas-danielf/Documents/PathologieMarburg/ui_dash/store_cache/"
        if not os.path.exists(path):
            os.makedirs(path)
        
        # Save text data to files
        with open(os.path.join(path, "group_a.txt"), "w") as file:
            file.write(group_a)
        with open(os.path.join(path, "group_b.txt"), "w") as file:
            file.write(group_b)
        with open(os.path.join(path, "description.txt"), "w") as file:
            file.write(description)
        with open(os.path.join(path, "analysis.txt"), "w") as file:
            file.write(analysis)
        with open(os.path.join(path, "excluded_genes.txt"), "w") as file:
            file.write(str(excluded_genes))
        with open(os.path.join(path, "control_genes.txt"), "w") as file:
            file.write(str(control_genes))
        with open(os.path.join(path, "graphs.txt"), "w") as file:
            file.write(str(graphs))
        with open(os.path.join(path, "dea.txt"), "w") as file:
            file.write(str(dea))
        with open(os.path.join(path, "email.txt"), "w") as file:
            file.write(str(email))
        with open(os.path.join(path, "gsea.txt"), "w") as file:
            file.write(str(gsea))

        # Save DataFrame data to CSV
        pd.read_json(gene, orient="records").to_csv(os.path.join(path, "gene.csv"), sep="\t", index=False)
        pd.read_json(meta, orient="records").to_csv(os.path.join(path, "meta.csv"), sep="\t", index=False)
        pd.read_json(table_a, orient="records").to_csv(os.path.join(path, "group_a.csv"), sep="\t", index=False)
        pd.read_json(table_b, orient="records").to_csv(os.path.join(path, "group_b.csv"), sep="\t", index=False)

        # Trigger the analysis script
        os.system('python3 /Users/lukas-danielf/Documents/PathologieMarburg/ui_dash/my_dash/scripts/start_analysis.py')
        
        return "Files saved successfully.", "Analysis started.", True

    return "", "", False



@app.callback(
    Output("offcanvas", "is_open"),
    Input("info-toggle", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open