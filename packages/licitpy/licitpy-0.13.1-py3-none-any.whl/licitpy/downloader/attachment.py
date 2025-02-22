import secrets
from typing import Optional

from pydantic import HttpUrl
from requests_cache import disabled

from licitpy.downloader.base import BaseDownloader
from licitpy.parsers.attachment import AttachmentParser
from licitpy.types.attachments import Attachment


class AttachmentDownloader(BaseDownloader):

    def __init__(
        self,
        parser: Optional[AttachmentParser] = None,
    ) -> None:

        super().__init__()

        self.parser: AttachmentParser = parser or AttachmentParser()

    def download_attachment_from_url(self, url: HttpUrl, attachment: Attachment) -> str:
        """
        Downloads an attachment from a URL using a POST request with the attachment ID.
        """

        file_code = attachment.id
        file_size = attachment.size
        file_name = attachment.name

        search_x = str(secrets.randbelow(30) + 1)
        search_y = str(secrets.randbelow(30) + 1)

        with disabled():

            # Fetch the HTML content of the page to extract the __VIEWSTATE
            # this request should be made without the cache
            html = self.get_html_from_url(url)

            response = self.session.post(
                str(url),
                data={
                    "__EVENTTARGET": "",
                    "__EVENTARGUMENT": "",
                    "__VIEWSTATE": self.parser.get_view_state(html),
                    "__VIEWSTATEGENERATOR": "13285B56",
                    # Random parameters that simulate the button click
                    f"DWNL$grdId$ctl{file_code}$search.x": search_x,
                    f"DWNL$grdId$ctl{file_code}$search.y": search_y,
                    "DWNL$ctl10": "",
                },
                timeout=(5, 30),
                stream=True,
            )

        return self.download_file_base64(response, file_size, file_name)

    def download_attachment(self, url: HttpUrl, attachment: Attachment) -> str:
        """
        Downloads an attachment from a URL using a POST request with the attachment ID.
        """

        return self.download_attachment_from_url(url, attachment)
