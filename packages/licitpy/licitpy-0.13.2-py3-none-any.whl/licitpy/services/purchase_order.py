from datetime import date
from typing import List, Optional

from pydantic import HttpUrl

from licitpy.downloader.purchase_order import PurchaseOrderDownloader
from licitpy.parsers.purchase_order import PurchaseOrderParser
from licitpy.services.base import BaseServices
from licitpy.types.geography import Commune, Region
from licitpy.types.purchase_order import PurchaseOrderFromCSV, Status


class PurchaseOrderServices(BaseServices):

    def __init__(
        self,
        downloader: Optional[PurchaseOrderDownloader] = None,
        parser: Optional[PurchaseOrderParser] = None,
    ):
        super().__init__()

        self.downloader = downloader or PurchaseOrderDownloader()
        self.parser = parser or PurchaseOrderParser()

    def get_url(self, code: str) -> HttpUrl:
        """
        Get the URL of a purchase order given its code.
        """

        return self.parser.get_url_from_code(code)

    def get_html(self, url: HttpUrl) -> str:
        """
        Get the HTML content of a purchase order given its URL.
        """

        return self.downloader.get_html_from_url(url)

    def get_status(self, html: str) -> Status:
        """
        Get the status of a purchase order based on its HTML content.
        """

        return self.parser.get_purchase_order_status(html)

    def get_title(self, html: str) -> str:
        """
        Get the title of a purchase order based on its HTML content.
        """

        return self.parser.get_purchase_order_title_from_html(html)

    def get_purchase_orders(self, year: int, month: int) -> List[PurchaseOrderFromCSV]:
        """
        Get the purchase orders of a given year and month.
        """

        return self.downloader.get_purchase_orders(year, month)

    def get_issue_date(self, html: str) -> date:
        """
        Get the issue date of a purchase order based on its HTML content.
        """

        return self.parser.get_purchase_order_issue_date_from_html(html)

    def get_tender_code(self, html: str) -> str | None:
        """
        Get the tender code of a purchase order based on its HTML content.
        """

        return self.parser.get_purchase_order_tender_code_from_html(html)

    def get_commune(self, html: str) -> Commune:
        """
        Get the commune of a purchase order based on its HTML content.
        """

        return self.parser.get_purchase_order_commune_from_html(html)

    def get_region(self, commune: Commune) -> Region:
        """
        Get the region of a purchase order based on its commune.
        """

        return self.parser.get_purchase_order_region_from_html(commune)
