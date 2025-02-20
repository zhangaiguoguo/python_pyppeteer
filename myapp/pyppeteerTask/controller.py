import asyncio
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from pyppeteer import launch
from pyppeteer.browser import Browser
from pyppeteer.page import Page

from .dto import PushTaskContent, PdfContent
from .utils import package_response_body, patch_response_body_result
from .setting import start_parm, MAX_OPEN_BROWSER_COUNT, SAVE_PDF_PATH, node_browser_page_inject_setting
from ..utils import make_file_info

thread_pool = ThreadPoolExecutor(max_workers=MAX_OPEN_BROWSER_COUNT)


class PyppeteerTaskController:
    browser: Browser = None
    launch_options = start_parm
    await_promise: threading.Event = None
    result_content = None

    def __init__(self, launch_options):
        self.launch_options = launch_options or self.launch_options
        self.await_promise = threading.Event()

    async def start_browser(self, promise: threading.Event, asyncHandler, **kwargs):
        try:
            self.browser = self.browser or await launch(**self.launch_options)
            self.result_content = await asyncHandler(**kwargs)
            await asyncio.sleep(0.3)
            return self.result_content
        finally:
            promise.set()

    async def open_url_page(self, options):
        response_send_event = asyncio.Event()

        await_browser_response_result = None

        def await_browser_response_result_handler(content):
            nonlocal response_send_event, await_browser_response_result
            if type(content) is str:
                content = json.loads(content.encode('utf-8'))
            await_browser_response_result = handler_result(page, content)
            response_send_event.set()

        page = await self.browser.newPage()

        await page.setJavaScriptEnabled(enabled=True)
        # await asyncio.sleep(1)
        await page.evaluateOnNewDocument('''
            (options,pageConsoleReturnResponseRef) => {
            console.log(options)
                options = typeof options === "object" ? options : JSON.parse(options)
                window.nodeBrowserInjectState = {
                    fillContent: options.fillContent,
                    options: options.options
                }
                window.nodeBrowserPageInjectSetting = {
                    key:pageConsoleReturnResponseRef
                }
            }
        ''', json.dumps({'url': options['url'], 'options': options['options'], 'fillContent': options['fillContent']},
                        indent=4), node_browser_page_inject_setting['pageConsoleReturnResponseRef'])

        await page.goto(options['url'], time=100)  # 页面跳转

        page.on("error", lambda: await_browser_response_result_handler("页面加载失败"))

        await page.exposeFunction('responseSend', await_browser_response_result_handler)

        await response_send_event.wait()

        await asyncio.sleep(0.3)

        response_result = await_browser_response_result or {}

        return await self.open_html_page(response_result['data'], page)

    async def open_html_page(self, options, page: Page = None):
        # 创建一个新页面
        page = page or await self.browser.newPage()

        page_url = options['pageUrl']

        if page_url == "":
            page_url = await page.evaluate('''
                (htmlContent) => URL.createObjectURL(new Blob([htmlContent], {
                    type: 'text/html'
                })
            ''', options['html'])
        else:
            if page_url[0:5] == "data:":
                page_url = await page.evaluate('''
                    (dataUrl) => {
                        const arr = dataUrl.split(',');
                        const mime = arr[0].match(/:(.*?);/)[1];
                        const bstr = decodeURIComponent(escape(atob(arr[1])));
                        return URL.createObjectURL(new Blob([bstr], {
                            type: mime
                        }));
                    }
                ''', page_url)

        # 导航到目标网页
        await page.goto(url=page_url, timeout=options['timeout'])

        await page.setUserAgent(
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 '
            'Safari/537.36')

        await page.emulateMedia('screen')

        file_info = make_file_info(SAVE_PDF_PATH, '.pdf')

        pdf_option = {
            "format": options['pageSize'],
            "scale": 1,
            "printBackground": True,
            "width": options['paperWidth'],
            "height": options['paperHeight'],
            "path": file_info['full_path']
        }

        file_flow = await page.pdf(pdf_option)
        file_info['file_flow'] = file_flow
        return file_info

    def submit_thread_pool(self, asyncHandler, **kwargs: Any) -> threading.Event:
        promise = self.await_promise or threading.Event()
        self.await_promise = promise
        flag = False
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.start_browser(promise, asyncHandler, **kwargs))
            flag = True
        except Exception as e:
            try:
                if not flag:
                    asyncio.run(self.start_browser(promise, asyncHandler, **kwargs))
                else:
                    raise ValueError(e)
            except Exception as e:
                raise ValueError("参数不正确! -> ", e)
        finally:
            return promise

    def get_to_url_page_content(self, options: PushTaskContent):
        thread_pool.submit(self.submit_thread_pool, self.open_url_page, options=options.__copy__())
        while True:
            if self.await_promise is not None:
                self.await_promise.wait()
                break

    def get_to_html_page_content(self, options: PdfContent):
        thread_pool.submit(self.submit_thread_pool, self.open_html_page, options=options.__copy__())
        while True:
            if self.await_promise is not None:
                self.await_promise.wait()
                break

    def __enter__(self):
        return self

    async def __aenter__(self):
        return self

    async def exit(self):
        try:
            if self.browser is not None:
                await self.browser.close()
        except Exception as e:
            print("browser close :", e)

        finally:
            try:
                if self.await_promise is not None:
                    self.await_promise.set()
            except Exception as e:
                print("await_promise close :", e)

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.exit())
        except Exception as e:
            asyncio.run(self.exit())

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.exit()


def handler_result(page: Page, content):
    content = package_response_body(content)
    result = patch_response_body_result(content)
    if content.get('code') == 500:
        raise ValueError(result)

    return result


async def open_url_browser(content: PushTaskContent):
    async with PyppeteerTaskController(start_parm) as instance:
        await asyncio.sleep(0.5)
        instance.get_to_url_page_content(options=content)
        return instance.result_content


async def open_html_browser(content: PdfContent):
    async with PyppeteerTaskController(start_parm) as instance:
        await asyncio.sleep(0.5)
        instance.get_to_html_page_content(options=content)
        return instance.result_content
