from typing import Dict, List, Optional

from pydantic import HttpUrl

from licitpy.downloader.award import AwardDownloader
from licitpy.parsers.award import AwardParser
from licitpy.services.base import BaseServices
from licitpy.types.attachments import Attachment
from licitpy.types.award import AwardResult, Method


class AwardServices(BaseServices):

    def __init__(
        self,
        downloader: Optional[AwardDownloader] = None,
        parser: Optional[AwardParser] = None,
    ):
        super().__init__()

        self.downloader = downloader or AwardDownloader()
        self.parser = parser or AwardParser()

    def get_html(self, url: HttpUrl) -> str:
        """
        Get the HTML content of a award given its URL.
        """

        return self.downloader.get_html_from_url(url)

    def get_url(self, html: str) -> HttpUrl:
        """
        Get the URL of a purchase order given its code.
        """
        return self.parser.get_url_from_html(html)

    def get_method(self, html: str) -> Method:
        """
        Get the method of a purchase order given its code.
        """
        return self.parser.get_method_from_html(html)

    def get_award_amount(self, html: str) -> int:
        """
        Field : Monto Neto Adjudicado

        Get the amount of an award given its HTML content.
        """

        return self.parser.get_award_amount_from_html(html)

    def get_estimated_amount(self, html: str) -> int:
        """
        Field: Monto Neto Estimado del Contrato

        Get the estimated amount of an award given its HTML content.
        """
        return self.parser.get_estimated_amount_from_html(html)

    def get_attachments_from_url(self, url: HttpUrl) -> List[Attachment]:
        """
        Get the attachments from the URL.
        """

        html = self.downloader.get_html_from_url(url)
        return self.get_attachments(url, html)

    def get_results(self, html: str) -> AwardResult:
        """
        Get the results of an award given its HTML content.
        """
        return self.parser.get_results_from_html(html)
