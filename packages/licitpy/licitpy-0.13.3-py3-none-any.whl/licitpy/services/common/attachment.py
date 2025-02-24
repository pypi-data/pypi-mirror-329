from functools import partial
from typing import List, Optional

from pydantic import HttpUrl

from licitpy.downloader.attachment import AttachmentDownloader
from licitpy.parsers.attachment import AttachmentParser
from licitpy.types.attachments import Attachment


class AttachmentServices:

    def __init__(
        self,
        downloader: Optional[AttachmentDownloader] = None,
        parser: Optional[AttachmentParser] = None,
    ):

        self.downloader: AttachmentDownloader = downloader or AttachmentDownloader()
        self.parser: AttachmentParser = parser or AttachmentParser()

    def get_attachments(self, url: HttpUrl, html: str) -> List[Attachment]:

        attachments: List[Attachment] = self.parser.get_attachments(html)

        for attachment in attachments:

            download_attachment_fn = partial(
                self.downloader.download_attachment, url, attachment
            )

            attachment._download_fn = download_attachment_fn

        return attachments
