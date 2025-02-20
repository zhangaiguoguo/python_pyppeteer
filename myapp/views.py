import base64
import json
import os
from functools import wraps
from django.http import JsonResponse, HttpResponse
import asyncio
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .pyppeteerTask.controller import open_url_browser, PushTaskContent
from .pyppeteerTask.setting import SAVE_PDF_PATH
from .utils import patch_encoded_path


def csrf_exempt_view(cls):
    @wraps(cls)
    class WrappedView(cls):
        @method_decorator(csrf_exempt, name='dispatch')
        def dispatch(self, *args, **kwargs):
            return super().dispatch(*args, **kwargs)

    return WrappedView


class PdfTransformCy(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    async def post(self, request, *args, **kwargs):
        body_data = json.loads(request.body.decode('utf-8'))
        content = await asyncio.create_task(
            open_url_browser(PushTaskContent(url=body_data.get('url'), fillContent=body_data.get('fillContent'),
                                             options=body_data.get('options'))))
        if content is None:
            return JsonResponse({'statue': 'error', 'message': "参数异常"}, status=500)

        return JsonResponse({"fileId": patch_encoded_path(content['file_id']), "fileName": content['file_name'],
                             # "content":  "data:application/pdf;base64," + base64.b64encode(content[
                             # 'file_flow']).decode( 'utf-8' )
                             })


class PdfTransformSl(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    async def post(self, request, *args, **kwargs):
        body_data = json.loads(request.body.decode('utf-8'))
        content = await asyncio.create_task(
            open_url_browser(PushTaskContent(url=body_data.get('url'), fillContent={
                list: body_data.get('list')
            },
                                             options={})))
        if content is None:
            return JsonResponse({'statue': 'error', 'message': "参数异常"}, status=500)

        return JsonResponse({"fileId": patch_encoded_path(content['file_id']), "fileName": content['file_name']})


class PdfView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    async def get(self, request, file_id, *args, **kwargs):
        file_path = os.path.join(SAVE_PDF_PATH, file_id)
        if not os.path.isfile(file_path):
            return JsonResponse({'statue': 'error', 'message': f'系统中不存在的文件 -> {file_id}'})
        with open(file_path, 'rb') as ff:
            file_flow = ff.read()
            return HttpResponse(file_flow, headers={'Content-Type': 'application/pdf'})


class PdfDelete(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    async def delete(self, request, file_id, *args, **kwargs):
        file_path = os.path.join(SAVE_PDF_PATH, file_id)
        if not os.path.isfile(file_path):
            return JsonResponse({'statue': 'error', 'message': f'系统中不存在的文件 -> {file_id}'})

        os.remove(file_path)

        return JsonResponse({'code': 200})
