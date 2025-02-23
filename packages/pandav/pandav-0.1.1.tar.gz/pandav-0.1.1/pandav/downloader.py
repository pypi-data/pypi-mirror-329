import shutil
import os

def dataframe(destination_folder="."):
    """
    Copies the Jupyter notebook to the specified destination.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    notebook_path = os.path.join(current_dir, "1.ipynb")
    destination_path = os.path.join(destination_folder, "1.ipynb")

    # Check if the file exists before copying
    if not os.path.exists(notebook_path):
        raise FileNotFoundError(f"Notebook file not found: {notebook_path}")

    shutil.copy(notebook_path, destination_path)
    print(f"downloaded to: {destination_path}")
    return destination_path
