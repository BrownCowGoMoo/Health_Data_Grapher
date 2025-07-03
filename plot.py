from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime

from models import PlotConfig, PlotValues

import matplotlib.pyplot as plt

if TYPE_CHECKING:
    from models import ResultInfoSeries, ResultInfo

class PlotValaueCalculator:
    @staticmethod
    def calculate_y_limits(plot_values_list: list[PlotValues], config: PlotConfig) -> tuple[float, float]:
        values = []
        normal_range = []
        for result in plot_values_list:
            values.append(result.value)
            normal_range.extend([result.lower_range, result.upper_range])
        
        min_y = min(*values, *normal_range) - config.y_axis_padding
        max_y = max(*values, *normal_range) + config.y_axis_padding

        if config.min_always_zero:
            min_y = 0

        return (min_y, max_y)
    
    @staticmethod
    def normal_range_as_franction(plot_values_list: list[PlotValues], min_y: float, max_y: float) -> tuple[float, float]:
        y_range = max_y - min_y
        lower_fraction = (plot_values_list[0].lower_range - min_y) / y_range
        upper_fraction = (plot_values_list[0].upper_range - min_y) / y_range

        return (lower_fraction, upper_fraction)
    
    @staticmethod
    def get_normal_range(plot_values_list: list[PlotValues]):
        upper_range = plot_values_list[0].upper_range
        lower_range = plot_values_list[0].lower_range

        return (lower_range, upper_range)

        
class PlotItemsSelector:
    @staticmethod
    def get_item_to_plot(choises) -> str:

        for index, name in enumerate(choises):
            print(f"{index + 1}: {name}")
        
        while True:
            ans = input("Enter the index of the item you would like to graph: ")
            try:
                ans = int(ans)
                item_name = choises[ans - 1]
            except (ValueError, IndexError):
                print(f"{ans} is not a valid index.")
                continue
            break
        
        return item_name
    
class PlotRenderer:
    def __init__(self, config: PlotConfig = PlotConfig()):
        self.config = config
        self.calculator = PlotValaueCalculator()

    def render(self, plot_values_list: list[PlotValues]):
        y_values = [result.value for result in plot_values_list]
        x_values = [result.date for result in plot_values_list]

        plt.plot(x_values, y_values,
                 marker=self.config.marker_stye, 
                 linestyle=self.config.line_style)
        
        self.add_value_labels(y_values)

        self.add_normal_range_shade(plot_values_list)

        min_y, max_y = self.calculator.calculate_y_limits(plot_values_list, self.config)

        plt.ylim(min_y, max_y)

        plt.ylabel(f"Values ({plot_values_list[0].units})")

        plt.xlabel("Dates")

        plt.xticks(rotation=45, ha="right")

        plt.title(plot_values_list[0].name)
        
        plt.tight_layout()

        plt.show()

    def add_value_labels(self, y_values: list[float]):
        for index, value in enumerate(y_values):
            plt.annotate(f"({value})",
                         (index, value),
                         textcoords="offset points",
                         xytext=self.config.value_label_offset,
                         ha="center")
                         
    def add_normal_range_shade(self, plot_values_list: list[PlotValues]):
        lower_range, upper_range = self.calculator.get_normal_range(plot_values_list)
        plt.axhspan(lower_range, upper_range, color=self.config.normal_range_color, alpha=self.config.normal_range_alpha)

    

def plot_graph(plot_values: tuple[tuple]):
    plot_value_list: list[PlotValues] = [PlotValues(*results) for results in plot_values]
    renderer = PlotRenderer()
    renderer.render(plot_value_list)



        




    

    