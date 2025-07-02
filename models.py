from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
@dataclass
class Pdf:
    """
    Dataclass to hold pdf file information.

    Attributes:
        path: Path to the file
        name_w_ext: File name with extension
        name: File name without extension
        text: A list containg each line of text in the file
    """
    path: str 
    name_w_ext: str
    name: str
    text: list[str] = field(default_factory=list)

@dataclass
class ResultInfo:
    """
    Dataclass to hold parsed result values

    Attrubutes:
        name: Name of the result
        flag: Flag from the result ('HI' or 'LO')
        value: Result value
        lower_range: Lower healthy range for value
        upper_range: Upper healthy range for value
        units: value Units
    """
    name: str
    flag: str
    value: float
    lower_range: float
    upper_range: float
    units: str

@dataclass
class ResultInfoSeries:
    """
    Dataclass to hold the report name and the list of all values parsed

    Attributes:
        report_name: Name of the report
        report_date: Date of the report (defaults to None)
        report_results: List of all result info objects associated with the report
    """
    report_name: str
    report_date: Optional[datetime] = None
    report_results: list[ResultInfo] = field(default_factory=list)