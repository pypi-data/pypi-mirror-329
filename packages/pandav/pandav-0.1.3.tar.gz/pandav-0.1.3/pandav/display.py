import nbformat
from nbconvert import HTMLExporter

def display_1():
    """Converts the notebook to HTML and prints it."""
    with open("1.ipynb", "r", encoding="utf-8") as f:
        notebook_data = nbformat.read(f, as_version=4)

    # Convert notebook to HTML
    html_exporter = HTMLExporter()
    html_body, _ = html_exporter.from_notebook_node(notebook_data)

    # Print HTML output
    from IPython.core.display import display, HTML
    display(HTML(html_body))



def display_2():
    """Converts the notebook to HTML and prints it."""
    with open("2.ipynb", "r", encoding="utf-8") as f:
        notebook_data = nbformat.read(f, as_version=4)

    # Convert notebook to HTML
    html_exporter = HTMLExporter()
    html_body, _ = html_exporter.from_notebook_node(notebook_data)

    # Print HTML output
    from IPython.core.display import display, HTML
    display(HTML(html_body))

