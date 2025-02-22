from datetime import date
from typing import Union

from licitpy.entities.tender import Tender
from licitpy.entities.tenders import Tenders
from licitpy.sources import API, Local
from licitpy.types.search import TimeRange
from licitpy.types.tender.status import Status
from licitpy.utils.date import determine_date_range


class TendersClient:
    def __init__(self, source: Union[API, Local]) -> None:
        self.source = source

    def from_date(
        self,
        start_date: str | date | None = None,
        end_date: str | date | None = None,
        time_range: TimeRange = TimeRange.THIS_MONTH,
    ) -> Tenders:
        """
        Retrieves tenders from a specific date range.
        """

        start_date, end_date = determine_date_range(start_date, end_date, time_range)

        return self.source.get_monthly_tenders(start_date, end_date)

    def from_code(self, code: str) -> Tender:
        """
        Retrieves a tender by its code.
        """

        return self.source.get_tender(code)

    def from_status(self, status: Status) -> Tenders:
        """
        Retrieves tenders by their status.
        """

        return self.source.get_tenders_by_status(status)
