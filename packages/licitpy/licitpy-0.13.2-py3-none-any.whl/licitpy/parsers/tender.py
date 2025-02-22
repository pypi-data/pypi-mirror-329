import re
from datetime import datetime
from typing import List
from zoneinfo import ZoneInfo

from lxml.html import HtmlElement
from pydantic import HttpUrl

from licitpy.parsers.base import BaseParser
from licitpy.types.geography import Region
from licitpy.types.tender.open_contract import OpenContract, PartyRoleEnum
from licitpy.types.tender.status import StatusFromImage, StatusFromOpenContract
from licitpy.types.tender.tender import Item, Renewal, Subcontracting, Tier, Unit


class TenderParser(BaseParser):

    def get_tender_opening_date_from_tender_ocds_data(
        self, data: OpenContract
    ) -> datetime:

        # The date comes as if it were UTC, but it is actually America/Santiago
        # - 2024-11-06T11:40:34Z -> 2024-11-06 11:40:34-03:00

        tender = data.records[0].compiledRelease.tender

        # "startDate": "2024-10-25T15:31:00Z",
        start_date = tender.tenderPeriod.startDate

        return datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=ZoneInfo("America/Santiago")
        )

    def get_closing_date_from_eligibility(self, html: str) -> datetime:
        # Extract the closing date for the eligibility phase (idoneidad técnica).
        # This date marks the final deadline for all participants to submit their initial technical eligibility documents.
        # After this point, only participants who meet the technical requirements can proceed.

        # Example date format from the HTML: "16-12-2024 12:00:00"
        closing_date = self.get_text_by_element_id(html, "lblFicha3CierreIdoneidad")

        # Parse the extracted date string into a datetime object, ensuring the correct format and time zone.
        return datetime.strptime(closing_date, "%d-%m-%Y %H:%M:%S").replace(
            tzinfo=ZoneInfo(
                "America/Santiago"
            )  # Set the time zone to Chile's local time.
        )

    def get_closing_date_from_html(self, html: str) -> datetime:
        # Check if the eligibility closing date (idoneidad técnica) exists in the HTML.
        # If lblFicha3CierreIdoneidad exists, it indicates that the process includes an eligibility phase.
        # In such cases, the usual closing date element (lblFicha3Cierre) contains a string like
        # "10 días a partir de la notificación 12:00" instead of a concrete date.
        if self.has_element_id(html, "lblFicha3CierreIdoneidad"):
            # Extract and return the eligibility closing date as the definitive closing date.
            # The eligibility phase defines the last moment when anyone can participate.
            return self.get_closing_date_from_eligibility(html)

        # If lblFicha3CierreIdoneidad does not exist, assume lblFicha3Cierre contains a concrete closing date.
        # Example: "11-11-2024 15:00:00"
        closing_date = self.get_text_by_element_id(html, "lblFicha3Cierre")

        # Parse the extracted date string into a datetime object, ensuring the correct format and time zone.
        return datetime.strptime(closing_date, "%d-%m-%Y %H:%M:%S").replace(
            tzinfo=ZoneInfo(
                "America/Santiago"
            )  # Set the time zone to Chile's local time.
        )

    def get_closing_date_from_tender_ocds_data(
        self, data: OpenContract
    ) -> datetime | None:
        """
        Get the closing date of a tender from its OCDS data.
        """

        tender = data.records[0].compiledRelease.tender

        # eg: "endDate": "2024-10-25T15:30:00Z",
        end_date = tender.tenderPeriod.endDate

        if end_date is None:
            return None

        return datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=ZoneInfo("America/Santiago")
        )

    def get_tender_status_from_tender_ocds_data(
        self, data: OpenContract
    ) -> StatusFromOpenContract:
        """
        Get the status of a tender from its OCDS data.
        """
        tender = data.records[0].compiledRelease.tender

        return tender.status

    def get_tender_title_from_tender_ocds_data(self, data: OpenContract) -> str:
        """
        Get the title of a tender from its OCDS data.
        """

        tender = data.records[0].compiledRelease.tender

        return tender.title

    def get_tender_description_from_tender_ocds_data(self, data: OpenContract) -> str:
        """
        Get the description of a tender from its OCDS data.
        """

        tender = data.records[0].compiledRelease.tender

        return tender.description

    def get_tender_region_from_tender_ocds_data(self, data: OpenContract) -> Region:
        """
        Retrieves the region of a tender from its OCDS data.
        """

        # Find the participants in the tender
        parties = data.records[0].compiledRelease.parties

        # Filter the participants who have the role of procuringEntity,
        # which represents the buying entity.
        procuring_entities = [
            party for party in parties if PartyRoleEnum.PROCURING_ENTITY in party.roles
        ]

        # If there is not exactly one entity with the role of procuringEntity, raise an error.
        if len(procuring_entities) != 1:
            raise ValueError(
                "There must be exactly one entity with the role of procuringEntity."
            )

        # Retrieve the address of the procuring entity.
        address = procuring_entities[0].address

        # If the address or region is missing, raise an error.
        if address is None or address.region is None:
            raise ValueError(
                "The address or region is missing for the procuring entity."
            )

        return address.region

    def get_tender_region_from_html(self, html: str) -> Region:
        """
        Get the region of a tender from its HTML content.
        """

        region = self.get_text_by_element_id(html, "lblFicha2Region")

        return Region(region)

    def get_tender_tier(self, code: str) -> Tier:
        """
        Get the budget tier of a tender based on its code.
        """

        return Tier(code.split("-")[-1:][0][:2])

    def get_tender_status_from_html(self, html: str) -> StatusFromImage:
        """
        Get the status of a tender based on its HTML content.
        """
        status = self.get_src_by_element_id(html, "imgEstado")

        return StatusFromImage(status.split("/")[-1].replace(".png", ""))

    def get_tender_code_from_tender_ocds_data(self, data: OpenContract) -> str:
        """
        Get the code of a tender from its OCDS data.
        """

        return str(data.uri).split("/")[-1].strip()

    def get_attachment_url_from_html(self, html: str) -> HttpUrl:
        """
        Get the URL of an attachment from the HTML content.
        """

        attachment_url = self.get_on_click_by_element_id(html, "imgAdjuntos")

        url_match = re.search(r"ViewAttachment\.aspx\?enc=(.*)','", attachment_url)

        if not url_match:
            raise ValueError("Attachment URL hash not found")

        enc: str = url_match.group(1)
        url = f"https://www.mercadopublico.cl/Procurement/Modules/Attachment/ViewAttachment.aspx?enc={enc}"

        return HttpUrl(url)

    def get_tender_purchase_order_url(self, html: str) -> HttpUrl:
        """
        Get the URL of the purchase orders of a tender from the HTML content.
        """

        purchase_order_popup = self.get_href_by_element_id(html, "imgOrdenCompra")

        if not purchase_order_popup:
            raise ValueError("Purchase orders not found")

        match = re.search(r"qs=(.*)$", purchase_order_popup)

        if not match:
            raise ValueError("Purchase Order query string not found")

        qs = match.group(1)
        url = f"https://www.mercadopublico.cl/Procurement/Modules/RFB/PopUpListOC.aspx?qs={qs}"

        return HttpUrl(url)

    def get_purchase_orders_codes_from_html(self, html: str) -> List[str]:
        """
        Extract the purchase order codes from the HTML content.
        """

        codes = re.findall(r'id="(rptSearchOCDetail_ctl\d{2}_lkNumOC)"', html)

        return [self.get_text_by_element_id(html, xpath) for xpath in codes]

    def get_questions_url(self, html: str) -> HttpUrl:
        """
        Get the URL of the questions of a tender from the HTML content.
        """

        href = self.get_href_by_element_id(html, "imgPreguntasLicitacion")
        match = re.search(r"qs=(.*)$", href)

        if not match:
            raise ValueError("Questions query string not found")

        qs = match.group(1)
        url = f"https://www.mercadopublico.cl/Foros/Modules/FNormal/PopUps/PublicView.aspx?qs={qs}"

        return HttpUrl(url)

    def get_question_code(self, html: str) -> str:
        """
        Get the code of a question from the HTML content.
        """

        return self.get_value_by_element_id(html, "h_intRBFCode")

    def get_item_codes_from_html(self, html: str) -> List[str]:
        """
        Extract numerical codes from 'id' attributes in the HTML
        that match the pattern 'grvProducto_ctlXX_lblNumero'.

        We do this to identify the total number of
        products or services included in the tender.

        Args:
            html (str): The HTML content as a string.

        Returns:
            List[str]: A list of numerical codes (e.g., ['02', '03', '04']).
        """

        html_element: HtmlElement = self.get_html_element(html)

        # [
        #     "grvProducto_ctl02_lblNumero",
        #     "grvProducto_ctl03_lblNumero",
        #     "grvProducto_ctl04_lblNumero",
        #     "grvProducto_ctl05_lblNumero",
        #     "grvProducto_ctl06_lblNumero",
        #     "grvProducto_ctl07_lblNumero",
        #     "grvProducto_ctl08_lblNumero",
        # ]

        elements = html_element.xpath(
            "//@id[starts-with(., 'grvProducto_ctl') and contains(., '_lblNumero')]"
        )

        # ['02', '03', '04', '05', '06', '07', '08']
        return [
            match.group(1)
            for element in elements
            if (match := re.search(r"ctl(\d+)_lblNumero", element))
        ]

    def get_item_from_code(self, html: str, code: str) -> Item:
        """
        Get the item of a tender from its HTML content and code.
        """

        base_id = f"grvProducto_ctl{code}_lbl"

        index = self.get_text_by_element_id(html, f"{base_id}Numero")
        title = self.get_text_by_element_id(html, f"{base_id}Producto")
        category = self.get_text_by_element_id(html, f"{base_id}Categoria")
        description = self.get_text_by_element_id(html, f"{base_id}Descripcion")
        quantity = self.get_text_by_element_id(html, f"{base_id}Cantidad")
        unit = self.get_text_by_element_id(html, f"{base_id}Unidad")

        return Item(
            index=int(index),
            title=title,
            category=int(category),
            description=description,
            quantity=int(quantity),
            unit=Unit(unit),
        )

    def has_signed_base(self, html: str) -> bool:
        """
        Check if the tender has a signed base document.
        """

        if self.has_element_id(html, "descargar_pdf_baseFirmada"):
            return True

        return False

    def allow_subcontracting(self, html: str) -> Subcontracting:
        """
        Check if the tender allows subcontracting.
        """

        # Because the element does not exist, we return None because we do not know if it is allowed or not.
        if not self.has_element_id(html, "lblFicha7Subcontratacion"):
            return Subcontracting.UNKNOWN

        # No permite subcontratación
        # Se permite subcontratación
        text = self.get_text_by_element_id(html, "lblFicha7Subcontratacion")

        return Subcontracting(text)

    def is_renewable(self, html: str) -> Renewal:
        """
        Check if the tender allows renewal.
        """

        if not self.has_element_id(html, "lblFicha7ContratoRenovacion"):
            return Renewal.UNKNOWN

        text = self.get_text_by_element_id(html, "lblFicha7ContratoRenovacion")

        return Renewal(text)

    def get_opening_date_from_html(self, html: str) -> datetime:
        """
        Get the opening date of a tender from its HTML content.
        """

        opening_date = self.get_text_by_element_id(html, "lblFicha3Publicacion")

        # eg: 06-08-2024 9:11:02
        return datetime.strptime(opening_date, "%d-%m-%Y %H:%M:%S").replace(
            tzinfo=ZoneInfo("America/Santiago")
        )
