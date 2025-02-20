from pyppeteer.page import Page

from myapp.pyppeteerTask.dto import PdfContentMetaInfo
from myapp.utils import first_letter_lowercase, is_empty


def package_response_body(responseBody) -> dict:
    if responseBody is None:
        return {
            'code': 500,
            'message': "数据处理异常"
        }

    if type(responseBody) == dict:
        if 'code' in responseBody:
            return {
                'code': 200,
                'data': responseBody
            }
        return responseBody

    return {
        'code': 500,
        'message': responseBody
    }


def patch_response_body_result(op: dict) -> str | dict:
    if op.get('code') == 500:
        return op.get('message')
    elif op.get('code') == 200:
        return op.get('data')
    else:
        return op


async def normalize_meta_info(metaInfo: PdfContentMetaInfo, page: Page):
    metaInfo = metaInfo.__copy__()
    book_js_meta_info = {
        "information": {}
    }
    if page is not None:
        ret = await page.evaluate("window.bookJsMetaInfo")
        if ret is not None:
            book_js_meta_info = ret

    keys = ['Author', 'Subject', 'Keywords']
    keys_lowercase = []

    if metaInfo is not None:
        information = metaInfo.information or {}
        for key in keys:
            if type(metaInfo[key]) is str:
                if metaInfo[key]:
                    key_lowercase = first_letter_lowercase(key)
                    keys_lowercase.append(key_lowercase)
                    information[key_lowercase] = metaInfo[key]
                    del metaInfo[key]

        del metaInfo.title
        metaInfo.information = information
        book_js_meta_info = metaInfo
    for e in keys_lowercase:
        if is_empty(book_js_meta_info.information[e]):
            del book_js_meta_info.information[e]

    return book_js_meta_info



