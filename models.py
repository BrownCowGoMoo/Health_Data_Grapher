from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
@dataclass
class Pdf:
    """
    Dataclass to hold pdf file information.

    Attributes:
        path: str = path to the file
        name_w_ext: str = file name with extension
        name: str = file name without extension
        text: list[str] = A list containg each line of text in the file
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
        name: str = Name of the result
        flag: str = flag from the result 'HI' or 'LO'
        value: float = result value
        lower_range: float = lower healthy range for value
        upper_range: float = upper healthy range for value
        units: str = value units
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
        report_name: str = name of the report
        report_results: list[ResultInfo] = list of all result info objects associated with the report
    """
    report_name: str
    report_date: Optional[datetime] = None
    report_results: list[ResultInfo] = field(default_factory=list)