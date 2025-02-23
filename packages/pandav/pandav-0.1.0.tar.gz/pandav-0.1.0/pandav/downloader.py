import shutil
import os

def dataframe(destination_folder="."):
    """
    Copies the included Jupyter notebook to the specified destination folder.
    
    Parameters:
        destination_folder (str): The path where the notebook should be copied. Defaults to the current directory.
    
    Returns:
        str: The full path of the copied file.
    """
    # Get the absolute path of this script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Path of the notebook inside the package
    notebook_path = os.path.join(current_dir, "1.ipynb")

    # Destination path
    destination_path = os.path.join(destination_folder, "1.ipynb")

    # Copy file to destination
    shutil.copy(notebook_path, destination_path)

    print(f"Notebook downloaded to: {destination_path}")
    return destination_path
