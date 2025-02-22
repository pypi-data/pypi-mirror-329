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

        year_month: List[Tuple[int, int]] = []

        current_date = start_date
        while current_date <= end_date:

            # [(2024, 12)]
            year_month.append((current_date.year, current_date.month))
            current_date += relativedelta(months=1)

        # The get_tenders service obtains information from both the API (OCDS) and the CSV (Massive Download).
        tenders_from_source: List[TenderFromSource] = []

        # We retrieve tenders from both sources (API and CSV) for the requested date ranges
        for year, month in year_month:
            tenders_from_source += self.tender_services.get_tenders_from_sources(
                year, month
            )

        # We retrieve only the tenders that fall within the requested date range
        tenders_within_dates: List[TenderFromSource] = [
            tender_from_source
            for tender_from_source in tenders_from_source
            if start_date <= tender_from_source.opening_date.date() <= end_date
        ]

        tenders: List[Tender] = []

        # We verify the status of the tenders in parallel
        with ThreadPoolExecutor(max_workers=16) as executor:

            futures_to_tender = {
                executor.submit(
                    self.tender_services.verify_status,
                    tender.status,
                    tender.closing_date,
                    tender.code,
                ): tender
                for tender in tenders_within_dates
            }

            for future in tqdm(
                as_completed(futures_to_tender),
                total=len(tenders_within_dates),
                desc="Verifying tender status",
            ):

                tender = futures_to_tender[future]
                verified_status = future.result()

                tenders.append(
                    Tender(
                        tender.code,
                        region=tender.region,
                        status=verified_status,
                        closing_date=tender.closing_date,
                        opening_date=tender.opening_date,
                        services=self.tender_services,
                    )
                )

        return Tenders(tenders)

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
