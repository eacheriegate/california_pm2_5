import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
import os
from geopandas.tools import clip

proj_dir = r"C:\Users\eache\.vscode\projects\california_pm2_5"
pollut_path = os.path.join(proj_dir, "data\pm2_5", "calenviroscreen40shpf2021shp", "CES4 Final Shapefile.shp")
road_path = os.path.join(proj_dir, "data\roads", "tl_2021_us_primaryroads", "tl_2021_us_primaryroads.shp")
field = "PM2_5"

all_data = gpd.read_file(pollut_path).to_crs(epsg=3310)

bay_counties = [
    "alameda", "contra costa", "marin", "napa", "san francisco",
    "san mateo", "santa clara", "solano", "sonoma"
]
bay_gdf = all_data[all_data["County"].str.lower().isin(bay_counties)].copy()

# Roads
roads = gpd.read_file(road_path).to_crs(epsg=3310)
roads = roads[roads["RTTYP"].isin(["I", "U", "S", "M", "C"])]
sf_union = bay_gdf.geometry.union_all.buffer(500)
roads_clipped = clip(roads, sf_union)

# Quantile Bins
n_bins = 6
bay_gdf["bin"], bin_edges = pd.qcut(bay_gdf[field], q=n_bins, labels=False, retbins=True, duplicates='drop')

# Color Palette and Colormap
colors = ['#ffffcc', '#ffeda0', '#fd8d3c', '#f03b20', '#bd0026', '#800026']
cmap = ListedColormap(colors[:n_bins])
norm = BoundaryNorm(bin_edges, ncolors=n_bins)

# Map
fig, ax = plt.subplots(figsize=(8, 10))
bay_gdf.plot(column="bin", cmap=cmap, linewidth=0, ax=ax, edgecolor='none', antialiased=False)
roads_clipped.plot(ax=ax, color="white", linewidth=0.3, alpha=0.6)

ax.set_xlim(*bay_gdf.total_bounds[[0, 2]])
ax.set_ylim(*bay_gdf.total_bounds[[1, 3]])
ax.axis('off')

plt.tight_layout()
os.makedirs("results", exist_ok=True)
plt.savefig("results/pm25_sf_map.png", dpi=600, bbox_inches="tight", facecolor='none')
plt.show()

# Legend
handles = []
for i in range(len(bin_edges) - 1):
    label = f"{bin_edges[i]:.2f} – {bin_edges[i+1]:.2f}"
    patch = mpatches.Patch(
        facecolor=colors[i],
        label=label,
        edgecolor='black',
        linewidth=0.25
    )
    handles.append(patch)

ax.legend(
    handles=handles,
    title="PM2.5 (μg/m³) by Census Tract",
    loc='lower center',
    bbox_to_anchor=(0.5, -0.08),
    frameon=True,
    framealpha=1,
    ncol=1,
    fontsize=9,
    title_fontsize=10
)

fig_legend, ax_legend = plt.subplots(figsize=(2, 2))
ax_legend.axis('off')

legend = ax_legend.legend(
    handles=handles,
    title="PM2.5 (μg/m³) by Census Tract",
    loc='center',
    frameon=False,
    edgecolor="black",
    framealpha=1,
    fontsize=9,
    title_fontsize=12,
    prop={'family': 'monospace'}
)
legend._legend_box.align = "left"
legend._legend_box.sep = 8
legend.get_frame().set_linewidth(0.5) 

plt.tight_layout()
plt.savefig("results/pm25_sf_leg.png", dpi=600, bbox_inches="tight", facecolor='none')
plt.show()