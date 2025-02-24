from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from typing import List, Optional, Tuple

from dateutil.relativedelta import relativedelta
from tqdm import tqdm

from licitpy.entities.purchase_order import PurchaseOrder
from licitpy.entities.purchase_orders import PurchaseOrders
from licitpy.entities.tender import Tender
from licitpy.entities.tenders import Tenders
from licitpy.services.purchase_order import PurchaseOrderServices
from licitpy.services.tender import TenderServices
from licitpy.sources.base import BaseSource
from licitpy.types.purchase_order import PurchaseOrderFromCSV
from licitpy.types.tender.status import Status
from licitpy.types.tender.tender import TenderFromSource


class Local(BaseSource):
    def __init__(
        self,
        tender_services: Optional[TenderServices] = None,
        purchase_order_services: Optional[PurchaseOrderServices] = None,
    ) -> None:

        self.tender_services = tender_services or TenderServices()

        self.purchase_order_services = (
            purchase_order_services or PurchaseOrderServices()
        )

    def get_monthly_tenders(self, start_date: date, end_date: date) -> Tenders:

        # 1) We get the range of months between the start and end dates (yyyy, mm)
        year_month: List[Tuple[int, int]] = []
        current_date = start_date

        while current_date <= end_date:

            # [(yyyy, mm), (yyyy, mm), ...]
            year_month.append((current_date.year, current_date.month))
            current_date += relativedelta(months=1)

        # 2) We retrieve the tenders from the sources (CSV files and API (OCDS))
        tenders_from_source: List[TenderFromSource] = []

        for year, month in year_month:
            tenders_from_source += self.tender_services.get_tenders_from_sources(
                year, month
            )

        # Filtering tenders that are internal QA tests from Mercado Publico.
        # eg: 500977-191-LS24 : Nombre Unidad : MpOperaciones
        tenders_from_source = [
            tender
            for tender in tenders_from_source
            if not tender.code.startswith("500977-")
        ]

        tenders: List[Tender] = []
        total = len(tenders_from_source)

        # 3) We verify the status of the tenders
        # We use the html of the tender to verify the status

        # for tender in tqdm(tenders_from_source, desc="Verifying tender status"):

        #     status, opening_date, region, closing_date = (
        #         self.tender_services.get_basics(tender.code)
        #     )

        #     tenders.append(
        #         Tender(
        #             tender.code,
        #             status=status,
        #             opening_date=opening_date,
        #             region=region,
        #             closing_date=closing_date,
        #             services=self.tender_services,
        #         )
        #     )

        with ThreadPoolExecutor(max_workers=32) as executor:

            futures_to_tender = {
                executor.submit(self.tender_services.get_basics, tender.code): tender
                for tender in tenders_from_source
            }

            for future in tqdm(
                as_completed(futures_to_tender),
                total=total,
                desc="Verifying tender status",
            ):

                tender = futures_to_tender[future]
                status, opening_date, region, closing_date = future.result()

                tenders.append(
                    Tender(
                        tender.code,
                        status=status,
                        opening_date=opening_date,
                        region=region,
                        closing_date=closing_date,
                        services=self.tender_services,
                    )
                )

        # 4) We retrieve only the tenders that fall within the requested date range
        return Tenders(
            [
                tender
                for tender in tenders
                if tender.opening_date
                and start_date <= tender.opening_date.date() <= end_date
            ]
        )

    def get_tender(self, code: str) -> Tender:
        return Tender(code)

    def get_monthly_purchase_orders(
        self, start_date: date, end_date: date
    ) -> PurchaseOrders:

        year_month: List[Tuple[int, int]] = []

        current_date = start_date
        while current_date <= end_date:

            year_month.append((current_date.year, current_date.month))
            current_date += relativedelta(months=1)

        purchase_orders: List[PurchaseOrderFromCSV] = []

        for year, month in year_month:

            purchase_orders += self.purchase_order_services.get_purchase_orders(
                year, month
            )

        return PurchaseOrders(
            [
                PurchaseOrder(
                    purchase_order.Codigo,
                    status=purchase_order.Estado,
                    title=purchase_order.Nombre,
                    issue_date=purchase_order.FechaEnvio,
                    region=purchase_order.RegionUnidadCompra,
                    commune=purchase_order.CiudadUnidadCompra,
                    services=self.purchase_order_services,
                )
                for purchase_order in purchase_orders
                if start_date <= purchase_order.FechaEnvio <= end_date
            ]
        )

    def get_purchase_order(self, code: str) -> PurchaseOrder:
        return PurchaseOrder.create(code)

    def get_tenders_by_status(self, status: Status) -> Tenders:
        return Tenders([])
