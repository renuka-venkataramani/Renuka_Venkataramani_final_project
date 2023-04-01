"""Tasks running the results formatting (tables, figures)."""
import geopandas as gpd
import pytask

from final_project.config import BLD, GROUP, SRC
from final_project.data_management import load_data
from final_project.final.plot import map_agriculture_diversity
from final_project.final.tables import create_table_1_agricultural_production_data
from final_project.utilities import read_yaml


@pytask.mark.depends_on(
    {
        "scripts": ["tables.py"],
        "main_data": BLD / "python" / "data" / "outcome_variables_data.csv",
        "data": BLD / "python" / "data" / "constructed_variables.csv",
        "data_info": SRC / "data_management" / "data_info.yaml",
    },
)
@pytask.mark.produces(
    BLD / "python" / "predictions" / "Table1_agricultural_production_data.pkl",
)
def task_table_1_agricultural_production_data(depends_on, produces):
    """Create table1: agriculture_production_data.

    Args:
        depends_on (dict): Path to extract input
        produces (dict): path to store output

    """
    data = load_data(depends_on["data"])
    outcome_variable_data = load_data(depends_on["main_data"])
    data_info = read_yaml(depends_on["data_info"])
    outcome_variables_data = create_table_1_agricultural_production_data(
        data,
        outcome_variable_data,
        data_info,
    )
    outcome_variables_data.to_pickle(produces)


for group in GROUP:

    kwargs = {
        "group": group,
        "produces": BLD / "python" / "figures" / f"{group}.png",
    }

    @pytask.mark.depends_on(
        {
            "scripts": ["plot.py"],
            "data": BLD / "python" / "data" / "outcome_variables_data.csv",
            "shape_file": SRC / "data" / "counties_shapefile.dbf",
            "data_info": SRC / "data_management" / "data_info.yaml",
        },
    )
    @pytask.mark.task(id=group, kwargs=kwargs)
    def task_map1_agriculture_diversity(depends_on, group, produces):
        """Clean the data (Python version)."""
        shp_data = gpd.read_file(depends_on["shape_file"])
        data = load_data(depends_on["data"])
        read_yaml(depends_on["data_info"])
        map1_agri_div = map_agriculture_diversity(
            csv_data=data,
            geo_data=shp_data,
            variable=group,
        )
        fig = map1_agri_div.get_figure()
        fig.savefig(produces)
