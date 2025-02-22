import logging
from abc import ABC, abstractmethod
from datetime import date

from licitpy.entities.purchase_order import PurchaseOrder
from licitpy.entities.tender import Tender
from licitpy.entities.tenders import Tenders
from licitpy.types.tender.status import Status


class BaseSource(ABC):

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def get_monthly_tenders(self, start_date: date, end_date: date) -> Tenders:
        pass  # pragma: no cover

    @abstractmethod
    def get_tender(self, code: str) -> Tender:
        pass  # pragma: no cover

    @abstractmethod
    def get_purchase_order(self, code: str) -> PurchaseOrder:
        pass  # pragma: no cover

    @abstractmethod
    def get_tenders_by_status(self, status: Status) -> Tenders:
        pass  # pragma: no cover
