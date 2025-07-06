from datetime import datetime
from typing import Optional
import re

def parse_reports(chosen_files: list[dict]) -> list[dict]:
    """
    Parses each file-dict's text into a report dict.

    Returns:
        all_series: list of report-dicts with keys:
            report_name: str
            report_date: datetime or None
            report_results: list of result-dicts
    """
    all_series = []

    for f in chosen_files:
        series = {
            "report_name": f["name"],
            "report_date": None,
            "report_results": []
        }
        for line in f["text"]:
            # try date
            if series["report_date"] is None:
                maybe_date = parse_date(line)
                if maybe_date:
                    series["report_date"] = maybe_date

            # try result
            info = parse_results(line)
            if info:
                series["report_results"].append(info)

        all_series.append(series)

    return all_series

def parse_results(line: str) -> Optional[dict]:
    """
    Parses the given line for name, flag, value, ranges, units.
    Returns a dict or None.
    """
    resultRE = re.compile(
        r"(?P<name>[\w\s]+?)(?P<flag>HI|LO)?\s"
        r"(?P<value>\d+\.?\d*)\s"
        r"(?P<lower_range>\d+\.?\d*)\s*-\s*"
        r"(?P<upper_range>\d+\.?\d*)\s"
        r"(?P<units>.+)"
    )

    match = resultRE.search(line)
    if not match:
        return None

    gd = match.groupdict()
    try:
        return {
            "name": gd["name"].strip(),
            "flag": (gd["flag"] or "").strip(),
            "value": float(gd["value"]),
            "lower_range": float(gd["lower_range"]),
            "upper_range": float(gd["upper_range"]),
            "units": gd["units"].strip()
        }
    except ValueError:
        print("value error")
        return None

def parse_date(line: str) -> Optional[datetime]:
    """
    Parses a line for a date string like "Reported on: Jan 02 2025 14:30".
    Returns a datetime or None.
    """
    dateRE = re.compile(
        r"Reported on: ((?P<month>[A-Za-z]{3}) "
        r"(?P<day>[1-3]\d|0?\d) (?P<year>\d{4}) "
        r"(?P<hour>\d{2}):(?P<minute>\d{2}))"
    )
    match = dateRE.search(line)
    if not match:
        return None
    return datetime.strptime(match.group(1), "%b %d %Y %H:%M")