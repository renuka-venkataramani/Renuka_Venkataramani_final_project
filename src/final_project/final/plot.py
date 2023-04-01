import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.axes_grid1 import make_axes_locatable


def map_agriculture_diversity(csv_data, geo_data, variable):
    geo_data["GISJOIN2"] = pd.to_numeric(geo_data["GISJOIN2"])
    merge_df_shp = geo_data.merge(
        csv_data[[variable, "GISJOIN2"]],
        on="GISJOIN2",
        how="left",
    )
    fig, ax = plt.subplots(1, 1)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.4)
    map = merge_df_shp.plot(
        column=variable,
        ax=ax,
        legend=True,
        cax=cax,
        missing_kwds={
            "color": "lightgrey",
            "label": "Missing values",
            "edgecolor": "black",
        },
        legend_kwds={
            "label": "Share of population in manufacturing",
            "orientation": "vertical",
        },
        cmap="ocean",
    )
    return map
