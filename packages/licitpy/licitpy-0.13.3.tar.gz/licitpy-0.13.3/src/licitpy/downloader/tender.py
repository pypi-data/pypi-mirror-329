from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Set

import pandas
from pydantic import HttpUrl, ValidationError
from requests_cache import CachedSession
from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed
from tqdm import tqdm

from licitpy.downloader.base import BaseDownloader
from licitpy.parsers.tender import TenderParser
from licitpy.types.download import MassiveDownloadSource
from licitpy.types.tender.open_contract import OpenContract
from licitpy.types.tender.tender import (
    Question,
    QuestionAnswer,
    TenderFromAPI,
    TenderFromCSV,
    TenderFromSource,
)


class TenderDownloader(BaseDownloader):

    def __init__(
        self,
        parser: Optional[TenderParser] = None,
    ) -> None:

        super().__init__()

        self.parser: TenderParser = parser or TenderParser()

    def get_tenders_codes_from_api(
        self, year: int, month: int, skip: int = 0, limit: int | None = None
    ) -> List[TenderFromAPI]:
        """
        Retrieves tender codes from the API for a given year and month.
        """

        # Check if limit is set to 0 or a negative number; if so, return an empty list
        if limit is not None and limit <= 0:
            return []

        # Define the base URL for the API endpoint to fetch tender data
        base_url = "https://api.mercadopublico.cl/APISOCDS/OCDS/listaOCDSAgnoMes"

        # Format the URL for the first request, retrieving up to 1000 records
        url = f"{base_url}/{year}/{month:02}/{skip}/1000"

        # Perform the initial API request and parse the JSON response
        records = self.session.get(url).json()

        # Retrieve the total available records for the given month and year
        total = records["pagination"]["total"]

        # If limit is None, set it to total to fetch all available records
        if limit is None:
            limit = total

        progress_bar = tqdm(
            total=total,
            desc=f"Downloading {year}-{month:02} from OCDS API",
            unit="records",
            bar_format="{l_bar}{bar} {n_fmt}/{total_fmt} {unit}",
        )

        progress_bar.update(len(records["data"]))

        # Extract tender codes from the first batch of data
        tenders = [
            TenderFromAPI(code=str(tender["urlTender"]).split("/")[-1])
            for tender in records["data"]
        ]

        # If the limit is within the first 1000 records, return the filtered tender list
        if limit <= 1000:
            return tenders[:limit]

        # Loop through additional records in blocks of 1000 to fetch the required amount
        for skip in range(1000, total, 1000):

            # If enough records are retrieved, exit the loop
            if len(tenders) >= limit:
                break

            # Format the URL for subsequent requests, always fetching 1000 records per request
            url = f"{base_url}/{year}/{month:02}/{skip}/1000"

            # Perform the API request and parse the JSON response
            records = self.session.get(url).json()

            # Append tender codes from the current batch to the tenders list
            tenders.extend(
                TenderFromAPI(code=str(tender["urlTender"]).split("/")[-1])
                for tender in records["data"]
            )

            progress_bar.update(len(records["data"]))

        # Return the exact number of requested records, sliced to the limit
        return tenders[:limit]

    def get_tenders_from_csv(
        self, year: int, month: int, limit: int | None = None
    ) -> List[TenderFromCSV]:
        """
        Retrieves tenders from the CSV for a given year and month.
        """

        columns: List[str] = ["CodigoExterno", "FechaPublicacion", "Estado"]
        dates_columns = ["FechaPublicacion"]

        df: pandas.DataFrame = self.get_massive_csv_from_zip(
            year, month, columns, dates_columns, MassiveDownloadSource.TENDERS
        )

        # Validate that each 'CodigoExterno' has a unique 'FechaPublicacion'
        if any(df.groupby("CodigoExterno")["FechaPublicacion"].nunique() > 1):
            raise ValueError("Inconsistent publication dates found")

        # Drop duplicate records based on the 'code' column, keeping the first occurrence
        df = df.drop_duplicates(subset="CodigoExterno", keep="first")

        # Reset the index of the DataFrame after sorting
        df.reset_index(drop=True, inplace=True)

        # If limit is None, set it to the total number of records in the DataFrame
        if limit is None:
            limit = df.shape[0]

        tenders = [
            TenderFromCSV(
                CodigoExterno=tender["CodigoExterno"], Estado=tender["Estado"]
            )
            for tender in df.to_dict(orient="records")
        ]

        return tenders[:limit]

    def get_tender_ocds_data_from_api(self, code: str) -> OpenContract | None:
        """
        Retrieves OCDS data for a given tender code from the API.
        """

        url = f"https://apis.mercadopublico.cl/OCDS/data/record/{code}"

        response = self.session.get(url)
        data = response.json()

        if "records" not in data and isinstance(self.session, CachedSession):

            with self.session.cache_disabled():

                response = self.session.get(url, timeout=30)
                data = response.json()

                # https://apis.mercadopublico.cl/OCDS/data/record/1725-41-LE25

                # {
                #     "status": 404,
                #     "detail": "No se encontraron resultados."
                # }

                if "records" not in data:
                    return None

                self.session.cache.save_response(response)

        return OpenContract(**data)

    # def get_tender_ocds_data_from_codes(
    #     self, tenders: List[TenderDataConsolidated], max_workers: int = 16
    # ) -> Dict[str, OpenContract]:
    #     """
    #     Retrieves OCDS data for a list of tenders from the API.
    #     """

    #     data_tenders: Dict[str, OpenContract] = {}
    #     total = len(tenders)

    #     with ThreadPoolExecutor(max_workers=max_workers) as executor:

    #         futures = {
    #             executor.submit(self.get_tender_ocds_data_from_api, tender.code): tender
    #             for tender in tenders
    #         }

    #         for future in tqdm(
    #             as_completed(futures),
    #             total=total,
    #             desc="Downloading OCDS data",
    #             mininterval=0.1,
    #             smoothing=0,
    #         ):

    #             tender = futures[future]

    #             try:
    #                 data = future.result()
    #             except Exception as e:

    #                 raise Exception(
    #                     f"Failed to download OCDS data for tender {tender.code}"
    #                 ) from e

    #             if data is None:
    #                 continue

    #             data_tenders[tender.code] = data

    #     return data_tenders

    def get_consolidated_tender_data(
        self, year: int, month: int
    ) -> List[TenderFromSource]:

        # Get only the tender codes from the API (OCDS)
        tenders_codes_from_api = self.get_tenders_codes_from_api(year, month)

        # Get the tenders from the CSV
        tenders_from_csv = self.get_tenders_from_csv(year, month)

        # Consolidate the tenders from the CSV and the API
        tenders_consolidated = [
            TenderFromSource(code=csv_tender.CodigoExterno)
            for csv_tender in tenders_from_csv
        ] + [
            TenderFromSource(code=api_tender.code)
            for api_tender in tenders_codes_from_api
        ]

        # Remove duplicates by converting to a dictionary and back to a list
        return list({tender.code: tender for tender in tenders_consolidated}.values())

    # @retry(
    #     stop=stop_after_attempt(3),
    #     wait=wait_fixed(3),
    # )
    def get_tender_url_from_code(self, code: str) -> HttpUrl:
        """
        Generates the tender URL from a given tender code.

        Args:
            code (str): The tender code.

        Returns:
            HttpUrl: The URL pointing to the tender's details page.
        """

        base_url = "https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx"

        query = (
            self.session.head(f"{base_url}?idlicitacion={code}", timeout=30)
            .headers["Location"]
            .split("qs=")[1]
            .strip()
        )

        return HttpUrl(f"{base_url}?qs={query}")

    def get_tender_questions(self, code: str) -> List[Question]:
        questions = self.session.get(
            "https://www.mercadopublico.cl/Foros/Modules/FNormal/servicesPub.aspx",
            data={"opt": "101", "RFBCode": code},
        ).json()

        # eg: Tender : 750301-54-L124
        # [
        #     {
        #         "idP": 1,
        #         "Numero": 6105959,
        #         "Descripcion": "Buenos días\n¿Se puede participar por línea?",
        #         "FechaHora": "05-11-2024 13:08:52",
        #         "Estado": 8,
        #         "RespuestaPublicada": {
        #             "idR": 5581150,
        #             "Descripcion": "SE PUEDE OFERTAR POR LÍNEA SEGÚN LO ESTABLECIDO EN LAS PRESENTES BASES.",
        #             "EstadoR": 4,
        #             "FechaHora": "07-11-2024 12:00:01"
        #         }
        #     }
        # ]

        return [
            Question(
                id=question["Numero"],
                text=str(question["Descripcion"])
                .replace("\n", " ")
                .lower()
                .capitalize(),
                created_at=question["FechaHora"],
                answer=QuestionAnswer(
                    id=question["RespuestaPublicada"]["idR"],
                    text=str(question["RespuestaPublicada"]["Descripcion"])
                    .replace("\n", " ")
                    .lower()
                    .capitalize(),
                    created_at=question["RespuestaPublicada"]["FechaHora"],
                ),
            )
            for question in questions
        ]
