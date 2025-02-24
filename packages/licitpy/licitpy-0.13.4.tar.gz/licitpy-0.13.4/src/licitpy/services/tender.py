from datetime import datetime
from typing import List, Optional, Tuple
from zoneinfo import ZoneInfo

from pydantic import HttpUrl

from licitpy.downloader.tender import TenderDownloader
from licitpy.entities.award import Award
from licitpy.entities.purchase_orders import PurchaseOrders
from licitpy.parsers.base import ElementNotFoundException
from licitpy.parsers.tender import TenderParser
from licitpy.services.base import BaseServices
from licitpy.types.attachments import Attachment
from licitpy.types.tender.open_contract import OpenContract
from licitpy.types.tender.status import Status
from licitpy.types.tender.tender import (
    Item,
    Question,
    Region,
    Renewal,
    Subcontracting,
    TenderFromSource,
    Tier,
)


class TenderServices(BaseServices):

    def __init__(
        self,
        downloader: Optional[TenderDownloader] = None,
        parser: Optional[TenderParser] = None,
    ):

        super().__init__()

        self.downloader: TenderDownloader = downloader or TenderDownloader()
        self.parser: TenderParser = parser or TenderParser()

    def get_basics(self, code: str) -> Tuple[Status, datetime, Region, datetime]:

        html = self.get_html_from_code(code)

        status = self.get_status(html)
        opening_date = self.get_opening_date_from_html(html)

        try:
            region = self.get_region_from_html(html)
        except ElementNotFoundException:
            data = self.get_ocds_data(code)

            if data is None:
                raise ValueError(f"No OCDS data found for tender {code}")

            region = self.get_region(data)

        closing_date = self.get_closing_date_from_html(html)

        return status, opening_date, region, closing_date

    def get_status(self, html: str) -> Status:

        status_from_html = self.parser.get_tender_status_from_html(html)
        return Status(status_from_html.name)

    def get_ocds_data(self, code: str) -> OpenContract | None:
        """
        Get the Open Contract Data (OCDS) from the tender code.
        """

        return self.downloader.get_tender_ocds_data_from_api(code)

    def get_url(self, code: str) -> HttpUrl:
        """
        Get the URL from the tender code.
        """

        return self.downloader.get_tender_url_from_code(code)

    def get_title(self, data: OpenContract) -> str:
        """
        Get the title from the Open Contract (OCDS) data.
        """

        return self.parser.get_tender_title_from_tender_ocds_data(data)

    def get_opening_date(self, data: OpenContract) -> datetime:
        """
        Get the opening date from the Open Contract (OCDS) data.
        """

        return self.parser.get_tender_opening_date_from_tender_ocds_data(data)

    def get_opening_date_from_html(self, html: str) -> datetime:
        """
        Get the opening date from the HTML.
        """

        return self.parser.get_opening_date_from_html(html)

    def get_html(self, url: HttpUrl) -> str:
        """
        Get the HTML from the URL.
        """

        return self.downloader.get_html_from_url(url)

    def get_tenders_from_sources(self, year: int, month: int) -> List[TenderFromSource]:
        """
        We retrieve the tenders code from both the API (OCDS) and the CSV (Massive Download).
        """

        return self.downloader.get_consolidated_tender_data(year, month)

    def get_tier(self, code: str) -> Tier:
        """
        Get the budget tier from the tender code.
        """

        return self.parser.get_tender_tier(code)

    def get_description(self, data: OpenContract) -> str:
        """
        Get the description from the Open Contract (OCDS) data.
        """

        return self.parser.get_tender_description_from_tender_ocds_data(data)

    def get_region(self, data: OpenContract) -> Region:
        """
        Get the region from the Open Contract (OCDS) data.
        """

        return self.parser.get_tender_region_from_tender_ocds_data(data)

    def get_region_from_html(self, html: str) -> Region:
        """
        Get the region from the HTML.
        """

        return self.parser.get_tender_region_from_html(html)

    def get_closing_date(self, data: OpenContract) -> datetime:
        """
        Get the closing date from the Open Contract (OCDS) data.
        """

        closing_date = self.parser.get_closing_date_from_tender_ocds_data(data)

        if closing_date is not None:
            return closing_date

        # If the closing date is not available in the OCDS data, we retrieve it from the HTML.
        code = self.parser.get_tender_code_from_tender_ocds_data(data)
        html = self.get_html_from_code(code)

        # Get the closing date from the HTML
        return self.get_closing_date_from_html(html)

    def get_closing_date_from_html(self, html: str) -> datetime:
        """
        Get the closing date from the HTML.
        """

        return self.parser.get_closing_date_from_html(html)

    def get_code_from_ocds_data(self, data: OpenContract) -> str:
        """
        Get the tender code from the Open Contract (OCDS) data.
        """

        return self.parser.get_tender_code_from_tender_ocds_data(data)

    def is_open(self, closing_date: datetime) -> bool:
        """
        Check if the tender is still open.
        """

        if not closing_date:
            return False

        now_utc = datetime.now(tz=ZoneInfo("America/Santiago"))

        return now_utc < closing_date

    def get_html_from_code(self, code: str) -> str:
        """
        Get the HTML from the tender code.
        """

        url = self.get_url(code)

        return self.get_html(url)

    def get_html_from_ocds_data(self, data: OpenContract) -> str:
        """
        Get the HTML from the tender code in the Open Contract data.
        """

        code = self.parser.get_tender_code_from_tender_ocds_data(data)

        return self.get_html_from_code(code)

    def get_attachment_url(self, html: str) -> HttpUrl:
        """
        Get the attachment URL from the HTML.
        """

        return self.parser.get_attachment_url_from_html(html)

    def get_attachments_from_url(self, url: HttpUrl) -> List[Attachment]:
        """
        Get the attachments from the URL.
        """

        html = self.downloader.get_html_from_url(url)
        return self.get_attachments(url, html)

    def get_signed_base_from_attachments(
        self, attachments: List[Attachment]
    ) -> Attachment:
        """
        Get the signed base from the attachments.
        """

        signed_bases = [
            attachment
            for attachment in attachments
            if "Anexo Resolucion Electronica (Firmada)" in attachment.type
        ]

        if not signed_bases:
            raise ValueError("No signed base found in attachments.")

        return signed_bases[0]

    def get_tender_purchase_order_url(self, html: str) -> HttpUrl:
        """
        Get the purchase order URL from the HTML.
        """

        return self.parser.get_tender_purchase_order_url(html)

    def get_tender_purchase_orders(self, html: str) -> PurchaseOrders:
        """
        Get the purchase orders from the HTML.
        """

        url = self.get_tender_purchase_order_url(html)

        html = self.downloader.get_html_from_url(url)
        codes = self.parser.get_purchase_orders_codes_from_html(html)

        # Create the purchase orders from the codes obtained from the HTML of the tender.
        return PurchaseOrders.from_tender(codes)

    def get_questions_url(self, html: str) -> HttpUrl:
        """
        Get the questions URL from the HTML.
        """

        return self.parser.get_questions_url(html)

    def get_questions(self, url: HttpUrl) -> List[Question]:
        """
        Get the questions from the URL.
        """

        html = self.downloader.get_html_from_url(url)
        code = self.parser.get_question_code(html)

        return self.downloader.get_tender_questions(code)

    def get_items(self, html: str) -> List[Item]:
        """
        Get the items from the HTML.
        """

        codes = self.parser.get_item_codes_from_html(html)

        return [self.parser.get_item_from_code(html, code) for code in codes]

    def has_signed_base(self, html: str) -> bool:
        """
        Check if the tender has a signed base.
        """

        return self.parser.has_signed_base(html)

    def allow_subcontracting(self, html: str) -> Subcontracting:
        """
        Check if the tender allows subcontracting.
        """

        return self.parser.allow_subcontracting(html)

    def is_renewable(self, html: str) -> Renewal:
        """
        Check if the tender allows renewal.
        """

        return self.parser.is_renewable(html)

    def get_tender_award(self, html: str) -> Award:
        """
        Get the award from the tender html.
        """

        return Award(html)
