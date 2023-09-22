from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D

colors = {
    "Eucalyptus 25": "#e3e8c3",
    "Mahogany 100": "#5acc5c",
    "Mahogany 200": "#1ca31e",
    "Reserve": "#026604",
}

cmap = ListedColormap(['#e3e8c3', '#5acc5c', '#1ca31e', '#026604'])

legend_content = [
    # regions
    Line2D([0], [0], color=cmap(0), lw=4),
    Line2D([0], [0], color=cmap(1), lw=4),
    Line2D([0], [0], color=cmap(2), lw=4),
    Line2D([0], [0], color=cmap(3), lw=4),
    # infrastructure
    Line2D([0], [0], color='black', marker='o', markersize=5, linestyle='None'),
    Line2D([0], [0], color="#302d2a", lw=1, linestyle="dashed"),
]

legend_names = ["Eucalyptus 25y", "Mahogany 100y", "Mahogany 200y", "Reserve", "Sawmill", "Road"]