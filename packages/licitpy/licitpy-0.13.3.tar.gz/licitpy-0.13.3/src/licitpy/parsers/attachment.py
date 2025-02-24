import re
from typing import List

from lxml.html import HtmlElement

from licitpy.parsers.base import BaseParser
from licitpy.types.attachments import Attachment, FileType


class AttachmentParser(BaseParser):

    def _get_table_attachments(self, html: str) -> HtmlElement:
        """
        Get the table containing the attachments from the HTML content.
        """

        table = self.get_html_element_by_id(html, "DWNL_grdId")

        if not table:
            raise ValueError("Table with ID 'DWNL_grdId' not found")

        return table[0]

    def _get_table_attachments_rows(self, table: HtmlElement) -> List[HtmlElement]:
        """
        Get the rows of the table containing the attachments.
        """

        rows = table.xpath("tr[@class]")

        if not rows:
            raise ValueError("No rows found in the table")

        return rows

    def _parse_size_attachment(self, td: HtmlElement) -> int:
        """
        Parse the size of an attachment from the HTML content.
        """

        size_text: str = td.xpath("span/text()")[0]
        match = re.match(r"(\d+)\s*Kb", size_text.strip())

        if not match:
            raise ValueError(f"Invalid size format: {size_text}")

        size_kb = int(match.group(1))

        return size_kb * 1024

    def _extract_attachment_id(self, td: HtmlElement) -> str:
        """
        Extract the attachment ID from the HTML content.
        """

        input_id = td.xpath("input/@id")

        if not input_id:
            raise ValueError("No input ID found in the first column")

        match = re.search(r"ctl(\d+)", input_id[0])

        if not match:
            raise ValueError("No match found for attachment ID")

        return match.group(1)

    def _extract_content_from_attachment_row(self, td: HtmlElement) -> str | None:
        """
        Extract the content from an attachment row in the HTML content.
        """

        content = td.xpath("span/text()")

        if content:
            return content[0]

        return None

    def get_attachments(self, html: str) -> List[Attachment]:
        """
        Get the attachments of a tender from the HTML content.
        """

        table = self._get_table_attachments(html)
        rows: List[HtmlElement] = self._get_table_attachments_rows(table)

        attachments: List[Attachment] = []

        for tr in rows:
            td: List[HtmlElement] = tr.xpath("td")

            attachment_id: str = self._extract_attachment_id(td[0])
            name = self._extract_content_from_attachment_row(td[1])
            attachment_type = self._extract_content_from_attachment_row(td[2])

            description = self._extract_content_from_attachment_row(td[3])

            size: int = self._parse_size_attachment(td[4])
            upload_date = self._extract_content_from_attachment_row(td[5])

            if not name:
                raise ValueError("Attachment name not found")

            # Bases_686617-1-L124.pdf
            file_type = FileType(name.split(".")[-1].lower().strip())

            attachment = Attachment(
                **{
                    "id": attachment_id,
                    "name": name,
                    "type": attachment_type,
                    "description": description,
                    "size": size,
                    "upload_date": upload_date,
                    "file_type": file_type,
                }
            )

            attachments.append(attachment)

        return attachments
