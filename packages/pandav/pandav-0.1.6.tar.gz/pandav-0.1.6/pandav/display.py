import nbformat
from nbconvert import HTMLExporter
import os

def display_1():
    """Converts 2.ipynb to HTML and prints it."""
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the same directory as dataframe2
    notebook_path = os.path.join(current_dir, "1.ipynb")  # Correct file path

    print("Looking for file at:", notebook_path)  # Debugging statement

    if not os.path.exists(notebook_path):
        print("❌ Error: 1.ipynb not found at", notebook_path)
        return
    
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook_data = nbformat.read(f, as_version=4)

    html_exporter = HTMLExporter()
    html_body, _ = html_exporter.from_notebook_node(notebook_data)
    from IPython.core.display import display, HTML

    display(HTML(html_body))



def display_2():
    """Converts 2.ipynb to HTML and prints it."""
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the same directory as dataframe2
    notebook_path = os.path.join(current_dir, "2.ipynb")  # Correct file path

    print("Looking for file at:", notebook_path)  # Debugging statement

    if not os.path.exists(notebook_path):
        print("❌ Error: 2.ipynb not found at", notebook_path)
        return
    
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook_data = nbformat.read(f, as_version=4)

    html_exporter = HTMLExporter()
    html_body, _ = html_exporter.from_notebook_node(notebook_data)
    from IPython.core.display import display, HTML

    display(HTML(html_body))




