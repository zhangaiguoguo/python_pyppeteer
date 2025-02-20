import copy
from typing import Dict


class PushTaskContent:
    url: str
    fillContent: any
    options: any

    def __init__(self, url: str, fillContent: any, options: any):
        self.url = url
        self.fillContent = fillContent
        self.options = options

    def __copy__(self):
        return copy.copy(self.__dict__)


class PdfContentMetaInfo:
    def __init__(self, title: str, Author: str, Keywords: str, Subject: str, information: Dict):
        self.Author = Author
        self.title = title
        self.Keywords = Keywords
        self.Subject = Subject
        self.information = information

    def __copy__(self):
        return copy.copy(self.__dict__)


class PdfContent:
    def __init__(self, pageUrl: str, html: str, pageSize: str, paperHeight: str, paperWidth: str, timeout: int,
                 metaInfo: PdfContentMetaInfo):
        self.html = html
        self.pageUrl = pageUrl
        self.pageSize = pageSize
        self.paperHeight = paperHeight
        self.paperWidth = paperWidth
        self.timeout = timeout
        self.metaInfo = metaInfo

    def __copy__(self):
        return copy.copy(self.__dict__)


class ResponseBodyDto:
    def __init__(self, file_id: str, file_name: str):
        self.file_id = file_id
        self.file_name = file_name
