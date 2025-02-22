from typing import Dict, List, Optional

from pydantic import HttpUrl

from licitpy.services.award import AwardServices
from licitpy.types.attachments import Attachment
from licitpy.types.award import AwardResult, Method


class Award:
    def __init__(
        self,
        tender_html: str,
        services: Optional[AwardServices] = None,
    ):
        self.tender_html: str = tender_html
        self._url: Optional[HttpUrl] = None
        self._method: Optional[Method] = None
        self._html: Optional[str] = None
        self._award_amount: Optional[int] = None
        self._estimated_amount: Optional[int] = None
        self._attachments: Optional[List[Attachment]] = None
        self._results: Optional[AwardResult] = None

        self.services = services or AwardServices()

    @property
    def url(self) -> HttpUrl:
        if self._url is None:
            self._url = self.services.get_url(self.tender_html)
        return self._url

    @property
    def html(self) -> str:
        if self._html is None:
            self._html = self.services.get_html(self.url)
        return self._html

    @property
    def method(self) -> Method:
        if self._method is None:
            self._method = self.services.get_method(self.html)
        return self._method

    @property
    def award_amount(self) -> int:
        if self._award_amount is None:
            self._award_amount = self.services.get_award_amount(self.html)
        return self._award_amount

    @property
    def estimated_amount(self) -> int:
        if self._estimated_amount is None:
            self._estimated_amount = self.services.get_estimated_amount(self.html)
        return self._estimated_amount

    @property
    def attachments(self) -> List[Attachment]:
        if self._attachments is None:
            self._attachments = self.services.get_attachments_from_url(self.url)
        return self._attachments

    @property
    def results(self) -> AwardResult:
        if self._results is None:
            self._results = self.services.get_results(self.html)
        return self._results
