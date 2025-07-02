from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import ResultInfoSeries

def get_common_results(all_records: list[ResultInfoSeries]):
    name_sets = [{info.name for info in records.report_results} for records in all_records]
    common_names = set.intersection(*name_sets)
    print(common_names)


    

    