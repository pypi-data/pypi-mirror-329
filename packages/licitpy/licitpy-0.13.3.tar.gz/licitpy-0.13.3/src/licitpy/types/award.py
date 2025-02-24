from enum import Enum
from typing import List

from pydantic import BaseModel


class Method(Enum):
    MULTIPLE_WITHOUT_OC = "Adjudicación Múltiple sin Emisión de OC"


class ItemAwardStatus(Enum):
    NOT_AWARDED = "No Adjudicada"
    AWARDED = "Adjudicada"


class SupplierBid(BaseModel):
    supplier_name: str
    supplier_item_description: str
    supplier_bid_total_price: int
    supplier_awarded_quantity: int
    supplier_total_awarded_amount: int
    supplier_bid_result: ItemAwardStatus


class ItemAward(BaseModel):
    item_index: int
    item_name: str
    item_description: str
    item_onu: str
    item_quantity: int
    item_total_awarded_amount: int
    suppliers: List[SupplierBid]


class AwardResult(BaseModel):
    items: List[ItemAward]
    total_awarded_amount: int
