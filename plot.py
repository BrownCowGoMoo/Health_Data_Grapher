from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime

from models import PlotConfig

import matplotlib as plt

if TYPE_CHECKING:
    from models import ResultInfoSeries, ResultInfo

class PlotCalculator:
    @staticmethod
    def calculate_y_limits(data: list[ResultInfoSeries], config: PlotConfig, ans_name: str):
        y_values = [result.value for series in data for result in series.report_results if result.name == ans_name]
        print(y_values)

class PlotItemsSelector:
    @staticmethod
    def get_item_to_plot(choises) -> str:

        for index, name in enumerate(choises):
            print(f"{index + 1}: {name}")
        
        while True:
            ans = input("Enter the index of the item you would like to graph: ")

            try:
                ans = int(ans)
                item_name = choises[ans]
            except (ValueError, IndexError):
                print(f"{ans} is not a valid index.")
                continue
            break
        return item_name

def sort_data_by_date(all_chose_records: list[ResultInfoSeries]):
    sorted_records_date: list[ResultInfoSeries] = sorted(all_chose_records, key=lambda r: r.report_date)
    return sorted_records_date
        




    

    