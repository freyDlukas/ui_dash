import base64
import io
import os

import pandas as pd
from dash import Input, Output, State, dash_table

from .app import app

# Define data types and excluded columns
types = {
    "id": "numeric",
    "Complaint_ID": "numeric",
    "ZIP_code": "numeric",
    "Date_received": "datetime",
    "Date_sent_to_company": "datetime",
}
excluded_columns = ["ID", "name"]


# Callback to store analysis name
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
    )


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


###start analysis button /Users/lukas-danielf/Documents/Pathologie Marburg/dashtest/dashtest/store_cache
# save Stores to files
# json
@app.callback(
    Output("storage", "children"),
    Input("start_analysis", "n_clicks"),
    [
        State("store-a", "data"),
        State("store-b", "data"),
        State("store-description", "data"),
        State("store-analysis", "data"),
        State("store-gene", "data"),
        State("store-meta", "data"),
        State("store-a-table", "data"),
        State("store-b-table", "data"),
    ],
)
def store_files(
    n_clicks, group_a, group_b, description, analysis, gene, meta, table_a, table_b
):
    path = "/Users/lukas-danielf/Documents/Pathologie Marburg/ui_dash/store_cache/"
    if n_clicks > 0:
       #Check if Folder exists if not create it
        if not os.path.exists(path):
            os.makedirs(path)
        # Save Group A, Group B, and Description to files
        with open(path + "group_a.txt", "w") as file:
            file.write(group_a)
        with open(path + "group_b.txt", "w") as file:
            file.write(group_b)
        with open(path + "description.txt", "w") as file:
            file.write(description)
        with open(path + "analysis.txt", "w") as file:
            file.write(analysis)
        gene = pd.read_json(gene, orient="records")
        meta = pd.read_json(meta, orient="records")
        table_a = pd.read_json(table_a, orient="records")
        table_b = pd.read_json(table_b, orient="records")
        gene.to_csv(path + "gene.csv", index=False)
        meta.to_csv(path + "meta.csv", index=False)
        table_a.to_csv(path + "group_a.csv", index=False)
        table_b.to_csv(path + "group_b.csv", index=False)
        return "Files saved successfully."
    return ""

#TODO: throw error when no files are uploaded and start button is clicked

# start script not tested yet, button "cooldown einfügen"
# @app.callback(
#     Output("storage", "children"),
#     Input("start_analysis", "n_clicks"),
# )
# def start_analysis(n_clicks):
#     if n_clicks > 0:
#         os.system("snakemake --cores 4 -s folder/snakefilename")
#         return "Analysis started."
#     return ""
