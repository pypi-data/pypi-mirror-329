from tiled.client import from_uri
from nbs_viewer.models.catalog.base import load_catalog_models
from nbs_viewer.models.plot.plotModel import PlotModel


def setup_catalog(url, catalog_name=None):
    """
    Set up a tiled catalog with specified model.

    Parameters
    ----------
    url : str
        The URL of the tiled server
    catalog_name : str, optional
        Name of the subcatalog to access

    Returns
    -------
    catalog
        The configured catalog model
    """
    base_catalog = from_uri(url)
    if catalog_name:
        catalog = base_catalog[catalog_name]["raw"]
    else:
        catalog = base_catalog

    catalog_models = load_catalog_models()

    # For now, let's use the first available model
    # You might want to make this configurable later
    first_model = list(catalog_models.values())[0]
    return first_model(catalog)


def get_latest_runs(catalog, n=5):
    """
    Get the n latest runs from a catalog.

    Parameters
    ----------
    catalog : catalog model
        The configured catalog model
    n : int, optional
        Number of runs to retrieve, defaults to 5

    Returns
    -------
    list
        List of selected runs
    """
    # Assuming the catalog is sorted with newest first
    return [run for run in list(catalog)[:n]]


def main():
    """
    Main function to demonstrate catalog and plot model usage.
    """
    # Example usage - modify these parameters as needed
    url = "http://localhost:8000"
    catalog_name = "your_catalog_name"  # Set to None if not needed

    # Set up catalog
    catalog = setup_catalog(url, catalog_name)

    # Get latest runs
    runs = get_latest_runs(catalog)

    # Set up plot model
    plot_model = PlotModel()

    # Add runs to plot model
    for run in runs:
        plot_model.add_run(run)

    return catalog, runs, plot_model


# if __name__ == "__main__":
#     catalog, runs, plot_model = main()
#     print(f"Loaded {len(runs)} runs from catalog")
#     print("Access these objects as catalog, runs, and plot_model")
