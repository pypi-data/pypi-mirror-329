import re
from typing import Dict, List

from pydantic import HttpUrl

from licitpy.parsers.base import BaseParser
from licitpy.types.award import (
    AwardResult,
    ItemAward,
    ItemAwardStatus,
    Method,
    SupplierBid,
)
from licitpy.utils.amounts import amount_to_int


class AwardParser(BaseParser):

    def get_url_from_html(self, html: str) -> HttpUrl:
        """
        Get the URL of an award given its HTML content.
        """

        href = self.get_href_by_element_id(html, "imgAdjudicacion")
        match = re.search(r"qs=(.*)$", href)

        if not match:
            raise ValueError("Awarded query string not found")

        qs = match.group(1)
        url = f"https://www.mercadopublico.cl/Procurement/Modules/RFB/StepsProcessAward/PreviewAwardAct.aspx?qs={qs}"

        return HttpUrl(url)

    def get_method_from_html(self, html: str) -> Method:
        """
        Get the method of an award given its HTML content.
        """

        return Method(self.get_text_by_element_id(html, "lblAwardTypeShow"))

    def get_award_amount_from_html(self, html: str) -> int:
        """
        Get the amount of an award given its HTML content.
        """

        amount = self.get_text_by_element_id(html, "lblAmountShow")
        return amount_to_int(amount)

    def get_estimated_amount_from_html(self, html: str) -> int:
        """
        Get the estimated amount of an award given its HTML content.
        """

        amount = self.get_text_by_element_id(html, "lblEstimatedAmountShow")
        return amount_to_int(amount)

    def get_codes_from_html(self, html: str) -> List[str]:
        """
        We obtain the code of the awarded bidding items
        """

        codes = re.findall(r'id="grdItemOC_ctl(\d{2})_ucAward__lblNumber"', html)
        return codes

    def get_total_of_items(self, codes: List[str]) -> int:
        """
        We obtain the total number of awarded items
        """
        return len(codes)

    def get_suppliers_codes_from_item(self, html: str, code: str) -> List[str]:
        """
        We obtain the codes of the suppliers that participated for an item
        """

        pattern = (
            r'id="grdItemOC_ctl'
            + code
            + '_ucAward_gvLines_ctl(\d{2})_gvLines_lblOrganization"'
        )

        return re.findall(pattern, html)

    def get_results_from_html(self, html: str) -> AwardResult:
        """
        Get the results of an award given its HTML content.
        """

        codes = self.get_codes_from_html(html)

        table_codes = {
            code: self.get_suppliers_codes_from_item(html, code) for code in codes
        }

        # {
        # '02': ['02', '03', '04', '05', '06', '07'],
        # '03': ['02', '03', '04', '05', '06', '07'],
        # '04': ['02', '03', '04', '05', '06', '07'],
        # '05': ['02', '03', '04', '05', '06', '07'],
        # '06': ['02', '03', '04', '05', '06', '07'],
        # '07': ['02', '03', '04', '05', '06', '07'],
        # '08': ['02', '03', '04', '05', '06', '07'],
        # '09': ['02', '03', '04', '05', '06', '07']
        # }

        items: List[ItemAward] = []

        for item_code, suppliers_code in table_codes.items():

            suppliers: List[SupplierBid] = []

            for supplier_code in suppliers_code:

                supplier_name = self.get_text_by_element_id(
                    html,
                    f"grdItemOC_ctl{item_code}_ucAward_gvLines_ctl{supplier_code}_gvLines_lblOrganization",
                )

                supplier_item_description = self.get_text_by_element_id(
                    html,
                    f"grdItemOC_ctl{item_code}_ucAward_gvLines_ctl{supplier_code}_gvLines_lblSupplierComment",
                )

                supplier_bid_total_price = self.get_text_by_element_id(
                    html,
                    f"grdItemOC_ctl{item_code}_ucAward_gvLines_ctl{supplier_code}_gvLines_lblTotalNetPrice",
                )

                supplier_awarded_quantity = self.get_text_by_element_id(
                    html,
                    f"grdItemOC_ctl{item_code}_ucAward_gvLines_ctl{supplier_code}_gvLines_txtAwardedQuantity",
                )

                supplier_total_awarded_amount = self.get_text_by_element_id(
                    html,
                    f"grdItemOC_ctl{item_code}_ucAward_gvLines_ctl{supplier_code}_gvLines_lblTotalNetAward",
                )

                supplier_bid_result = ItemAwardStatus(
                    self.get_text_by_element_id(
                        html,
                        f"grdItemOC_ctl{item_code}_ucAward_gvLines_ctl{supplier_code}_gvLines_lblIsSelected",
                    )
                )

                suppliers.append(
                    SupplierBid(
                        **{
                            "supplier_name": supplier_name,
                            "supplier_item_description": supplier_item_description,
                            "supplier_bid_total_price": supplier_bid_total_price,
                            "supplier_awarded_quantity": supplier_awarded_quantity,
                            "supplier_total_awarded_amount": supplier_total_awarded_amount,
                            "supplier_bid_result": supplier_bid_result,
                        }
                    )
                )

            item_index = self.get_text_by_element_id(
                html, f"grdItemOC_ctl{item_code}_ucAward__lblNumber"
            )

            item_onu = self.get_text_by_element_id(
                html, f"grdItemOC_ctl{item_code}_ucAward_lblCodeonu"
            )

            item_name = self.get_text_by_element_id(
                html, f"grdItemOC_ctl{item_code}_ucAward__LblSchemaTittle"
            )

            item_description = self.get_text_by_element_id(
                html, f"grdItemOC_ctl{item_code}_ucAward_lblDescription"
            )

            item_quantity = self.get_text_by_element_id(
                html, f"grdItemOC_ctl{item_code}_ucAward__LblRBICuantityNumber"
            )

            item_total_awarded_amount = amount_to_int(
                self.get_text_by_element_id(
                    html, f"grdItemOC_ctl{item_code}_ucAward_lblTotalLine"
                )
            )

            items.append(
                ItemAward(
                    **{
                        "item_index": item_index,
                        "item_onu": item_onu,
                        "item_name": item_name,
                        "item_description": item_description,
                        "item_quantity": item_quantity,
                        "item_total_awarded_amount": item_total_awarded_amount,
                        "suppliers": suppliers,
                    }
                )
            )

        total_awarded_amount = amount_to_int(
            self.get_text_by_element_id(html, "lblAmountTotalDetail")
        )

        return AwardResult(items=items, total_awarded_amount=total_awarded_amount)
