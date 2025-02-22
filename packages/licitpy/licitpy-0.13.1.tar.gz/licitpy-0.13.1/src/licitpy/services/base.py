from typing import List

from pydantic import HttpUrl

from licitpy.services.common.attachment import AttachmentServices
from licitpy.types.attachments import Attachment


class BaseServices:
    def __init__(self) -> None:
        self.attachment_services = AttachmentServices()

    def get_attachments(self, url: HttpUrl, html: str) -> List[Attachment]:
        return self.attachment_services.get_attachments(url, html)
