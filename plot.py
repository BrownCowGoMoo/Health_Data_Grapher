
from __future__ import annotations
from functools import reduce
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import ResultInfoSeries

def get_common_results(all_records: list[ResultInfoSeries]):
    

    common_names = [{info.name for info in records.report_results} for records in all_records]
    print(common_names)

    

    