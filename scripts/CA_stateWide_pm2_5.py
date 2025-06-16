import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from mapclassify import Quantiles
from matplotlib.patches import Patch
import numpy as np
import os

proj_dir = r"C:/Users/eache/.vscode/projects/invisible-air"
pollut_path = os.path.join(proj_dir, "data", "calenviroscreen40shpf2021shp", "CES4 Final Shapefile.shp")
road_path = os.path.join(proj_dir, "data", "tl_2021_us_primaryroads", "tl_2021_us_primaryroads.shp")

# === Load Data ===
ca_gdf = gpd.read_file(pollut_path).to_crs(epsg=3310)
ca_roads = gpd.read_file(road_path).to_crs(epsg=3310)
ca_roads = ca_roads[ca_roads["RTTYP"].isin(["I", "U", "S", "M"])].copy()

# === Clip Roads to California Area ===
ca_union_geom = ca_gdf.geometry.unary_union  # fixed method call
ca_roads = ca_roads[ca_roads.intersects(ca_union_geom)].copy()

# === PM2.5 Classification ===
field = "PM2_5"
k = 5
qclass = Quantiles(ca_gdf[field], k=k)
bins = [ca_gdf[field].min()] + list(qclass.bins)
labels = [f"{round(bins[i], 2)} – {round(bins[i+1], 2)}" for i in range(k)]

# === Colormap Setup ===
colors = plt.cm.magma(np.linspace(0.2, 0.9, k))[::-1]
cmap = mcolors.ListedColormap(colors)
norm = mcolors.BoundaryNorm(bins, ncolors=cmap.N)

# === Plot Map ===
fig, ax = plt.subplots(figsize=(12, 14))

ca_gdf.plot(
    column=field,
    cmap=cmap,
    norm=norm,
    linewidth=0,
    edgecolor='none',
    alpha=0.85,
    ax=ax,
    zorder=1
)
ca_roads.plot(
    ax=ax,
    color="white",
    linewidth=0.15,
    alpha=0.8,
    zorder=2
)

ax.set_xlim(*ca_gdf.total_bounds[[0, 2]])
ax.set_ylim(*ca_gdf.total_bounds[[1, 3]])
ax.set_axis_off()
plt.title("PM2.5 Concentration in California", fontsize=16)
plt.tight_layout()

os.makedirs("results", exist_ok=True)
plt.savefig("results/ca_pm25_map.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.show()


fig, ax = plt.subplots(figsize=(3, 2))
legend_elements = [
    Patch(facecolor=colors[i], edgecolor='none', label=labels[i])
    for i in range(k)
]

ax.legend(
    handles=legend_elements,
    title="PM2.5 (μg/m³)",
    frameon=True,
    fontsize=8,
    title_fontsize=9,
    loc="center left"
)
ax.axis("off")
plt.tight_layout()
plt.savefig("results/ca_pm25_legend.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.show()
