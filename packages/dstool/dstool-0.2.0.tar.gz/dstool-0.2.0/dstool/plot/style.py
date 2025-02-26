import urllib
import tempfile
import seaborn as sns
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties

font_urls = {
    "Fira Code": "https://github.com/google/fonts/raw/main/ofl/firacode/FiraCode%5Bwght%5D.ttf",
    "Inter": "https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz,wght%5D.ttf",
}

palettes = {
    # Default palette extracted from example_image1
    "default": [
        "#808080",
        "#FFA500",
        "#00C957",
        "#4169E1",
    ],  # Gray, Orange, Green, Royal Blue
    # Throughput palette from example_image2
    "throughput": [
        "#D3D3D3",
        "#1E3A8A",
        "#3B82F6",
    ],  # Light gray, dark blue, light blue
    # Bar chart palette from grouped_bar_chart
    "comparison": [
        "#D3D3D3",
        "#264A73",
        "#4A7CBA",
    ],  # Light gray, dark blue, medium blue
    # Expanded palette combining unique colors from all examples
    "extended": [
        "#808080",  # Gray
        "#FFA500",  # Orange
        "#00C957",  # Green
        "#4169E1",  # Royal Blue
        "#264A73",  # Dark Blue
        "#4A7CBA",  # Medium Blue
        "#3B82F6",  # Light Blue
        "#D3D3D3",  # Light Gray
        "#1E3A8A",  # Navy Blue
    ],
}


def _add_fonts():
    path = Path(tempfile.mkdtemp())
    for font in font_urls.keys():
        font_path = path / f"{font.replace(" ","-")}.ttf"
        urllib.request.urlretrieve(font_urls[font], font_path)
        font_entry = font_manager.FontEntry(
            fname=str(font_path), name=f"{font}"
        )
        font_manager.fontManager.ttflist.append(font_entry)

        font_entry = font_manager.FontEntry(
            fname=str(font_path),
            name=f"{font}",
            weight="bold",
            variant="bold",
            style="normal",
        )
        font_manager.fontManager.ttflist.append(font_entry)


def set_styles(
    style="whitegrid",
    font_scale=1.2,
    title_size=22,
    label_size=18,
    tick_size=14,
    legend_size=16,
    annotation_size=12,
):
    _add_fonts()
    sns.set_theme(style=style, font_scale=font_scale)
    # Set default figure size
    plt.rcParams["figure.figsize"] = (12, 6)
    # Set font sizes for different elements
    plt.rcParams["axes.titlesize"] = title_size  # Size of plot titles
    plt.rcParams["axes.labelsize"] = label_size  # Size of axis labels
    plt.rcParams["xtick.labelsize"] = tick_size  # Size of x-tick labels
    plt.rcParams["ytick.labelsize"] = tick_size  # Size of y-tick labels
    plt.rcParams["legend.fontsize"] = legend_size  # Size of legend text
    plt.rcParams["figure.titlesize"] = (
        title_size + 4
    )  # Size of figure suptitle

    sns.set_context(
        "paper",
        font_scale=2,
        rc={
            "lines.linewidth": 3,
            "lines.markersize": 10,
        },
    )
    plt.rcParams["axes.titleweight"] = "bold"  # Bold plot titles
    plt.rcParams["axes.labelweight"] = "bold"  # Bold axis labels
    plt.rcParams["figure.titleweight"] = "bold"  # Bold figure title

    # Improve font appearance
    plt.rcParams["font.family"] = "Inter"
    plt.rcParams["font.sans-serif"] = ["Fira Code"]

    # Adjust grid appearance
    plt.rcParams["grid.linestyle"] = "--"
    plt.rcParams["grid.alpha"] = 0.7
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42
    sns.despine()


def autolabel(rects, ax, prec=1, size=12):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate(
            f"{height:.{prec}f}",
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(0, 3),  # 3 points vertical offset
            textcoords="offset points",
            ha="center",
            va="bottom",
            size=size,
        )
