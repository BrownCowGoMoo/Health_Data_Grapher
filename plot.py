from __future__ import annotations
from datetime import datetime

import matplotlib.pyplot as plt

class PlotItemsSelector:
    @staticmethod
    def get_item_to_plot(choices) -> str:
        for idx, name in enumerate(choices, start=1):
            print(f"{idx}: {name}")
        while True:
            ans = input("Enter the index of the item you would like to graph: ")
            try:
                i = int(ans) - 1
                return choices[i]
            except (ValueError, IndexError):
                print(f"{ans} is not a valid index.")

def plot_graph(plot_values: tuple[tuple]):
    """
    plot_values: sequence of tuples
        (name, flag, value, lower_range, upper_range, units, file_name, date_str)
    """
    # unpack into lists
    dates = [datetime.strptime(r[7], "%Y-%m-%d %H:%M") for r in plot_values]
    values = [r[2] for r in plot_values]
    low, high = plot_values[0][3], plot_values[0][4]
    unit = plot_values[0][5]
    title = plot_values[0][0]

    # config dict in place of PlotConfig
    cfg = {
        "marker": "o",
        "line_style": "-",
        "range_color": "green",
        "range_alpha": 0.2,
        "padding": 10,
        "min_zero": True,
        "label_offset": (0, 10)
    }

    # y-limits
    all_vals = values + [low, high]
    min_y = 0 if cfg["min_zero"] else min(all_vals) - cfg["padding"]
    max_y = max(all_vals) + cfg["padding"]

    # plot line
    plt.plot(dates, values,
             marker=cfg["marker"],
             linestyle=cfg["line_style"])

    # shaded normal range
    plt.axhspan(low, high,
                color=cfg["range_color"],
                alpha=cfg["range_alpha"])

    # annotations
    for i, v in enumerate(values):
        plt.annotate(f"({v})",
                     (dates[i], v),
                     textcoords="offset points",
                     xytext=cfg["label_offset"],
                     ha="center")

    plt.ylim(min_y, max_y)
    plt.ylabel(f"Values ({unit})")
    plt.xlabel("Date")
    plt.xticks(rotation=45, ha="right")
    plt.title(title)
    plt.tight_layout()
    plt.show()



        




    

    