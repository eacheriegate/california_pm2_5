# Custom continuous legend #

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

vmin, vmax = 5.5, 15.0
cmap = plt.cm.YlOrRd
norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

fig, ax = plt.subplots(figsize=(6, 1.2))
cb = plt.colorbar(
    plt.cm.ScalarMappable(norm=norm, cmap=cmap),
    cax=ax,
    orientation='horizontal'
)
cb.set_label('PM2.5 (µg/m³)')

plt.tight_layout()
plt.show()
