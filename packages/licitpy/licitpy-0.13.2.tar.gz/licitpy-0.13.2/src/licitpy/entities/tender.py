from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import HttpUrl

from licitpy.entities.award import Award
from licitpy.entities.purchase_orders import PurchaseOrders
from licitpy.services.tender import TenderServices
from licitpy.types.attachments import Attachment
from licitpy.types.geography import Region
from licitpy.types.tender.open_contract import OpenContract
from licitpy.types.tender.status import Status
from licitpy.types.tender.tender import Item, Question, Renewal, Subcontracting, Tier
from licitpy.utils.validators import is_valid_public_market_code


class Tender:

    def __init__(
        self,
        code: str,
        region: Optional[Region] = None,
        status: Optional[Status] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        opening_date: Optional[datetime] = None,
        closing_date: Optional[datetime] = None,
        services: Optional[TenderServices] = None,
    ):

        if not is_valid_public_market_code(code):
            raise ValueError(f"Invalid public market code: {code}")

        self.code: str = code

        self._url: Optional[HttpUrl] = None
        self._html: Optional[str] = None

        self._region: Optional[Region] = region
        self._status: Optional[Status] = status
        self._title: Optional[str] = title
        self._description: Optional[str] = description

        self._opening_date: Optional[datetime] = opening_date
        self._closing_date: Optional[datetime] = closing_date

        self._tier: Optional[Tier] = None
        self._ocds: Optional[OpenContract] = None
        self._questions_url: Optional[HttpUrl] = None
        self._attachment_url: Optional[HttpUrl] = None
        self._signed_base: Optional[Attachment] = None
        self._questions: Optional[List[Question]] = None
        self._attachments: Optional[List[Attachment]] = None
        self._purchase_orders: Optional[PurchaseOrders] = None
        self._has_signed_base: Optional[bool] = None
        self._items: Optional[List[Item]] = None
        self._allow_subcontracting: Optional[Subcontracting] = None
        self._is_renewable: Optional[Renewal] = None
        self._award: Optional[Award] = None

        self.services = services or TenderServices()

    @property
    def ocds(self) -> OpenContract | None:
        if self._ocds is None:
            self._ocds = self.services.get_ocds_data(self.code)
        return self._ocds

    @property
    def url(self) -> HttpUrl:
        if self._url is None:
            self._url = self.services.get_url(self.code)

        return self._url

    @property
    def html(self) -> str:
        if self._html is None:
            self._html = self.services.get_html(self.url)
        return self._html

    @property
    def opening_date(self) -> datetime | None:
        if self._opening_date is None and self.ocds:
            self._opening_date = self.services.get_opening_date(self.ocds)
        return self._opening_date

    @property
    def closing_date(self) -> datetime | None:
        if self._closing_date is None and self.ocds:
            self._closing_date = self.services.get_closing_date(self.ocds)
        return self._closing_date

    @property
    def is_open(self) -> bool | None:
        if self.closing_date is None:
            return None

        return self.services.is_open(self.closing_date)

    @property
    def status(self) -> Status | None:
        if self._status is None and self.ocds:
            self._status = self.services.get_status(self.html)
        return self._status

    @property
    def title(self) -> str | None:
        if self._title is None and self.ocds:
            self._title = self.services.get_title(self.ocds)
        return self._title

    @property
    def tier(self) -> Tier:
        if self._tier is None:
            self._tier = self.services.get_tier(self.code)
        return self._tier

    @property
    def description(self) -> str | None:
        if self._description is None and self.ocds:
            self._description = self.services.get_description(self.ocds)
        return self._description

    @property
    def region(self) -> Region | None:
        if self._region is None and self.ocds:
            self._region = self.services.get_region(self.ocds)
        return self._region

    @property
    def attachment_url(self) -> HttpUrl:
        if self._attachment_url is None:
            self._attachment_url = self.services.get_attachment_url(self.html)
        return self._attachment_url

    @property
    def attachments(self) -> List[Attachment]:
        if self._attachments is None:
            self._attachments = self.services.get_attachments_from_url(
                self.attachment_url
            )
        return self._attachments

    @property
    def has_signed_base(self) -> bool:
        if self._has_signed_base is None:
            self._has_signed_base = self.services.has_signed_base(self.html)

        return self._has_signed_base

    @property
    def signed_base(self) -> Attachment:
        if self._signed_base is None:
            self._signed_base = self.services.get_signed_base_from_attachments(
                self.attachments
            )
        return self._signed_base

    @property
    def purchase_orders(self) -> PurchaseOrders:
        if self._purchase_orders is None:
            self._purchase_orders = self.services.get_tender_purchase_orders(self.html)
        return self._purchase_orders

    @property
    def questions_url(self) -> HttpUrl:
        if self._questions_url is None:
            self._questions_url = self.services.get_questions_url(self.html)
        return self._questions_url

    @property
    def questions(self) -> List[Question]:
        if self._questions is None:
            self._questions = self.services.get_questions(self.questions_url)
        return self._questions

    @property
    def items(self) -> List[Item]:
        if self._items is None:
            self._items = self.services.get_items(self.html)

        return self._items

    @property
    def subcontracting(self) -> Subcontracting:
        if self._allow_subcontracting is None:
            self._allow_subcontracting = self.services.allow_subcontracting(self.html)

        return self._allow_subcontracting

    @property
    def is_renewable(self) -> Renewal:
        if self._is_renewable is None:
            self._is_renewable = self.services.is_renewable(self.html)

        return self._is_renewable

    @property
    def award(self) -> Award:
        if self._award is None:
            self._award = self.services.get_tender_award(self.html)
        return self._award
