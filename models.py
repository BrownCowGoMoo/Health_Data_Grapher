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

@dataclass
class PlotValues(ResultInfo):
    """
    Dataclass to hold values of results to plot

    Attributes:
        name: Name of the result
        flag: Flag from the result ('HI' or 'LO')
        value: Result value
        lower_range: Lower healthy range for value
        upper_range: Upper healthy range for value
        units: value Units
        file_name: Name of the file the result was taken from
        date: a date as a string (format: YYYY-MM-DD HH-MM-SS)
    """
    file_name: str
    date: str

    @property
    def get_normal_range(self):
        """ Gets the normal range """
        if not self.upper_range or not self.lower_range:
            return (0, 0)
        return (self.lower_range, self.upper_range)
    
@dataclass
class PlotConfig:
    """
    Attributes:
        marker_style: Style of matplotlib markers (default = 'o')
        line_style: Style of lines in matplotlib (default = '-')
        normal_range_color: Color to display the normal range for a result (default = 'green')
        normal_range_alpha: Amount of transperency for normal_range (default 0.2)
        y_axis_padding: Amount of y-axis padding from highest and lowest value (default = 0)
        min_always_zero: Boolean value, determines if the min value for the y axis is set to 0 (default = True)
        value_label: boolean value, dermines use of value labels (default = True)
        value_label_offset: Offset for the value label (default = (0, 10))
    """
    # Visual stye
    marker_stye: str = "o"
    line_style: str = "-"

    # Normal range Visuals
    normal_range_color: str = "green"
    normal_range_alpha: float = 0.2

    # Axis config
    y_axis_padding: int = 10
    min_always_zero: bool = True

    # Annotations
    value_label: bool = True
    value_label_offset: tuple[int, int] = (0,10)