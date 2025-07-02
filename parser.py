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
            if series.report_date is None:
                maybe_date = parse_date(line)
                if maybe_date:
                    series.report_date = maybe_date
            if not info:
                continue
            series.report_results.append(info)
        all_series.append(series)
    return all_series
            

def parse_results(line: str) -> ResultInfo | None:
    """
    Parses the given line for name, flag, value, lower_range, upper_range, and units.

    Args:
        line: str = line from a pdf file
    
    Returns:
        info: ResultInfo = ResultInfo object
    """
    resultRE = re.compile(r"(?P<name>[\w\s]+?)(?P<flag>HI|LO)?\s(?P<value>\d+\.?\d*)\s(?P<lower_range>\d+\.?\d*)\s*-\s*(?P<upper_range>\d+\.?\d*)\s(?P<units>.+)")

    match = resultRE.search(line)
    if not match:
        return None
    
    results = match.groups()

    striped_results = tuple(item.strip() if isinstance(item, str) else item for item in results)

    name, flag, value, lower_range, upper_range, units = striped_results
    try:
        value = float(value)
        lower_range = float(lower_range)
        upper_range = float(upper_range)
    except ValueError:
        print("value error")
    info = ResultInfo(name, flag, value, lower_range, upper_range, units)

    return info 

def parse_date(line: str):

    dateRE = re.compile(r"Reported on: ((?P<month>[a-zA-Z]{3}) (?P<day>[1-3]\d|0?\d) (?P<year>\d{4}) (?P<hour>\d{2}):(?P<minute>\d{2}))")

    match = dateRE.search(line)
    if not match:
        return None
    
    return datetime.strptime(match.group(1), "%b %d %Y %H:%M")
    
 

