from dataclasses import dataclass, field
from datetime import datetime
import re
from files import Pdf

@dataclass
class ResultInfo:
    name: str
    flag: str
    value: float
    lower_range: float
    upper_range: float
    units: str

@dataclass
class ResultInfoSeries:
    report_name: str
    report_results: list[ResultInfo] = field(default_factory=list)

resultRE = re.compile(r"(?P<name>[\w\s]+?)(?P<flag>HI|LO)?\s(?P<value>\d+\.?\d*)\s(?P<lower_range>\d+\.?\d*)\s*-\s*(?P<upper_range>\d+\.?\d*)\s(?P<units>.+)")

def parse_results(chosen_files: list[Pdf]):
    all_series: list[ResultInfoSeries] = []
    for file in chosen_files:
        series = ResultInfoSeries(file.name)
        for line in file.text:
            match = resultRE.search(line)
            if not match:
                continue
            name, flag, value, lower_range, upper_range, units = match.groups()
            try:
                value = float(value)
                lower_range = float(lower_range)
                upper_range = float(upper_range)
            except ValueError:
                print("value error")
            info = ResultInfo(name, flag, value, lower_range, upper_range, units)
            series.report_results.append(info)
    all_series.append(series)
    return all_series

