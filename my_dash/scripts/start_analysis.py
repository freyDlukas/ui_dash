import os
import shutil
import subprocess
import yaml
from datetime import datetime, timedelta
import ast

def remove_old_folders(directory, days=30):
    # Calculate the date threshold
    threshold_date = datetime.now() - timedelta(days=days)

    # Iterate through all items in the directory
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        # Check if it's a directory
        if os.path.isdir(item_path):
            # Get the modification time of the directory
            modification_time = datetime.fromtimestamp(os.path.getmtime(item_path))

            # Check if the directory is older than the threshold
            if modification_time < threshold_date:
                # Remove the directory
                shutil.rmtree(item_path)
                print(f"Removed {item_path}")

# Cleanup cache
directory_to_clean = "/Users/lukas-danielf/Documents/PathologieMarburg/ui_dash/"
remove_old_folders(directory_to_clean)

# Create folder with timestamp (ensure unique timestamp)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
folder_name = timestamp
folder_path = f"/Users/lukas-danielf/Documents/PathologieMarburg/ui_dash/cache/{folder_name}"

# Check if the folder already exists, append milliseconds if necessary
counter = 0
while os.path.exists(folder_path):
    counter += 1
    folder_name = f"{timestamp}_{counter}"
    folder_path = f"/Users/lukas-danielf/Documents/PathologieMarburg/ui_dash/cache/{folder_name}"

os.makedirs(folder_path)
print(f"Created folder: {folder_path}")

# Copy data from cache to folder
source_folder = "/Users/lukas-danielf/Documents/PathologieMarburg/ui_dash/store_cache"
destination_folder = os.path.join(folder_path, "store_cache")
shutil.copytree(source_folder, destination_folder)
print(f"Copied {source_folder} to {destination_folder}")

# Define file paths
dea = "/Users/lukas-danielf/Documents/PathologieMarburg/ui_dash/store_cache/dea.txt"
analysis = "/Users/lukas-danielf/Documents/PathologieMarburg/ui_dash/store_cache/analysis.txt"
control_genes = "/Users/lukas-danielf/Documents/PathologieMarburg/ui_dash/store_cache/control_genes.txt"
description = "/Users/lukas-danielf/Documents/PathologieMarburg/ui_dash/store_cache/description.txt"
email = "/Users/lukas-danielf/Documents/PathologieMarburg/ui_dash/store_cache/email.txt"
excluded_genes = "/Users/lukas-danielf/Documents/PathologieMarburg/ui_dash/store_cache/excluded_genes.txt"
graphs = "/Users/lukas-danielf/Documents/PathologieMarburg/ui_dash/store_cache/graphs.txt"
group_a = "/Users/lukas-danielf/Documents/PathologieMarburg/ui_dash/store_cache/group_a.txt"
group_b = "/Users/lukas-danielf/Documents/PathologieMarburg/ui_dash/store_cache/group_b.txt"
gsea = "/Users/lukas-danielf/Documents/PathologieMarburg/ui_dash/store_cache/gsea.txt"


# Dictionary to store configuration data
config_data = {}

# Function to parse file content into the desired format
def parse_content(content):
    try:
        # Attempt to parse the content as a Python list or dictionary
        parsed_content = ast.literal_eval(content)
        if isinstance(parsed_content, (list, dict)):
            return parsed_content
    except (ValueError, SyntaxError):
        # If parsing fails, treat content as a single string item list
        pass
    return content.strip()  # Assuming it's a single line string

# Read and parse each file
def read_and_parse_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read().strip()
        return parse_content(content)

# Read content from each file
config_data['dea'] = read_and_parse_file(dea)
config_data['analysis'] = read_and_parse_file(analysis)
config_data['control_genes'] = read_and_parse_file(control_genes)
config_data['description'] = read_and_parse_file(description)
config_data['email'] = read_and_parse_file(email)
config_data['excluded_genes'] = read_and_parse_file(excluded_genes)
config_data['graphs'] = read_and_parse_file(graphs)
config_data['group_a'] = read_and_parse_file(group_a)
config_data['group_b'] = read_and_parse_file(group_b)
config_data['gsea'] = read_and_parse_file(gsea)
config_data['timestamp'] = timestamp
# Output YAML file path
output_yaml = "/Users/lukas-danielf/Documents/PathologieMarburg/ui_dash/Snakemake/config.yaml"

# Write dictionary to YAML file
with open(output_yaml, 'w') as yaml_file:
    yaml.dump(config_data, yaml_file, default_flow_style=False)

print(f"Config file '{output_yaml}' successfully created.")

# Check dea and run the system command based on the data
# Read the contents of the file
with open(dea, 'r') as file:
    content = file.read().strip()
    

# Extract the list from the content
analyses = content.strip('[]').split(', ')

# List to store the subprocesses
processes = []

# Iterate through each analysis and run Snakemake sequentially
for analysis in analyses:
    # command = f"snakemake --use-conda -s /Users/lukas-danielf/Documents/PathologieMarburg/ui_dash/Snakemake/snakefiles/{analysis} --cores 1"
    command = "snakemake --use-conda -s /Users/lukas-danielf/Documents/PathologieMarburg/ui_dash/Snakemake/snakefiles/Snakefile --cores 1"
    print(f"Running: {analysis}")
    
    # Run the command in a subprocess
    process = subprocess.run(command, shell=True)
    processes.append(process)

print("All Snakemake commands executed.")
