import os
import shutil
from datetime import datetime, timedelta


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


# Example usage:
directory_to_clean = "/path/to/your/directory"
remove_old_folders(directory_to_clean)


# start snakemake
os.system("snakemake --cores 4 -s folder/snakefilename")
