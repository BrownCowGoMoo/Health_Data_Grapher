from dataclasses import dataclass, field
from datetime import datetime
import re

from models import Pdf, ResultInfo, ResultInfoSeries


def parse_reports(chosen_files: list[Pdf]) -> list[ResultInfoSeries]:
    all_series: list[ResultInfoSeries] = []

    for file in chosen_files:
        series = ResultInfoSeries(file.name)
        for line in file.text:
            info = parse_results(line)
            if not info:
                continue
            series.report_results.append(info)
        all_series.append(series)
    return all_series
            

def parse_results(line: str) -> ResultInfo:
    """
    Parses the wanted results from each chosen file, converts info to proper types.

    Args:
        chosen_files: list[Pdf] = list of pdf objects of chosen files
    
    Returns:
        all_series: list[ResultInfoSeries] = List of all Result info Series objects.
    """
    resultRE = re.compile(r"(?P<name>[\w\s]+?)(?P<flag>HI|LO)?\s(?P<value>\d+\.?\d*)\s(?P<lower_range>\d+\.?\d*)\s*-\s*(?P<upper_range>\d+\.?\d*)\s(?P<units>.+)")

    match = resultRE.search(line)
    if not match:
        return None
    name, flag, value, lower_range, upper_range, units = match.groups()
    try:
        value = float(value)
        lower_range = float(lower_range)
        upper_range = float(upper_range)
    except ValueError:
        print("value error")
    info = ResultInfo(name, flag, value, lower_range, upper_range, units)

    return info 
 

