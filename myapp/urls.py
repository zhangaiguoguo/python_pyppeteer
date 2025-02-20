from django.urls import path
from .views import PdfTransformCy, PdfView, PdfTransformSl, PdfDelete

urlpatterns = [
    path('cyapp/generate/hiprint/template/toPdf/', PdfTransformCy.as_view(), name=PdfTransformCy.__name__),
    path('cyapp/generate/hiprint/template/toPdf', PdfTransformCy.as_view(), name=PdfTransformCy.__name__),
    path('generate/hiprint/template/toPdf/', PdfTransformSl.as_view(), name=PdfTransformSl.__name__),
    path('generate/hiprint/template/toPdf', PdfTransformSl.as_view(), name=PdfTransformSl.__name__),
    path('view/file/pdf/<str:file_id>/', PdfView.as_view(), name=PdfView.__name__),
    path('delete/file/pdf/<str:file_id>/', PdfDelete.as_view(), name=PdfDelete.__name__),
]
