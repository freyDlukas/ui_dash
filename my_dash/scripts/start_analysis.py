import os
import shutil
from datetime import datetime, timedelta
import yaml
import ast
import subprocess

# remove folders older than 30 days
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

# cleanup cache
directory_to_clean = "/Users/lukas-danielf/Documents/PathologieMarburg/ui_dash/"
remove_old_folders(directory_to_clean)

# create folder with timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
folder = f"/Users/lukas-danielf/Documents/PathologieMarburg/ui_dash/cache/{timestamp}"
os.makedirs(folder)
# copy data from cache to folder
shutil.move("/Users/lukas-danielf/Documents/PathologieMarburg/ui_dash/store_cache", folder)


#write the config file
#paths
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

# Function to parse file content into the desired format
def parse_content(content):
    try:
        # Attempt to parse the content as a Python list
        parsed_content = ast.literal_eval(content)
        if isinstance(parsed_content, list):
            return parsed_content
    except (ValueError, SyntaxError):
        # If parsing fails, treat content as a single string item list
        pass
    return [content]


def add_timestamp(data):
    data['timestamp'] = timestamp


# Read existing data from the YAML file
config = '/Users/lukas-danielf/Documents/PathologieMarburg/ui_dash/Snakemake/config.yaml'
text_files = [dea, analysis, control_genes, description, email, excluded_genes, graphs, group_a, group_b, gsea]

try:
    with open(config, 'r') as yaml_file:
        existing_data = yaml.safe_load(yaml_file)
except FileNotFoundError:
    existing_data = {}

# Read content from other text files and update the dictionary
for file_path in text_files:
    with open(file_path, 'r') as file:
        file_content = file.read().strip()
        # Use the file name (without extension) as the key
        key = os.path.splitext(os.path.basename(file_path))[0]
        existing_data[key] = parse_content(file_content)

# Add timestamp to existing data
add_timestamp(existing_data)

# Write the updated data back to the YAML file
with open(config, 'w') as yaml_file:
    yaml.dump(existing_data, yaml_file, default_flow_style=False)
# check dea and run the system command based on the data
# Read the contents of the file
with open(dea, 'r') as file:
    content = file.read().strip()

# Extract the list from the content
analyses = content.strip('[]').split(', ')

# List to store the subprocesses
processes = []

# Iterate through each analysis and run Snakemake sequentially
for analysis in analyses:
    command = f"snakemake -s /Users/lukas-danielf/Documents/PathologieMarburg/ui_dash/Snakemake/snakefiles/{analysis}"
    print(f"Running: {analysis}")
    
    # Run the command in a subprocess
    process = subprocess.Popen(command, shell=True)
    processes.append(process)

# Wait for all subprocesses to complete
for process in processes:
    process.wait()

print("All Snakemake commands executed.")
