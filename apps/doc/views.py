import requests
from . import models

from django.shortcuts import render
from django.http import FileResponse, Http404
from django.utils.encoding import escape_uri_path
from django.views import View
from my_news import settings




def doc(request):
    """
    """
    docs = models.Doc.objects.defer('author', 'create_time', 'update_time', 'is_delete').filter(is_delete=False)
    return render(request, 'doc/docDownload.html',context={
        'docs':docs
    })


class DocDownload(View):

    def get(self, request, doc_id):
        doc_file = models.Doc.objects.only('file_url').filter(is_delete=False, id=doc_id).first()
        if doc_file:
            doc_file_url = doc_file.file_url  #media/流畅的python.pdf
            doc_url = settings.DOC_DOWNLOAD_URL + doc_file_url
            res = FileResponse(requests.get(doc_url))

            #获取后缀
            ex_name = doc_url.split('.')[-1] #获取ptf

            if not ex_name:
                raise Http404('文件名异常')
            else:
                ex_name = ex_name.lower()

            if ex_name == "pdf":
                res["Content-type"] = "application/pdf"
            elif ex_name == "zip":
                res["Content-type"] = "application/zip"
            elif ex_name == "doc":
                res["Content-type"] = "application/msword"
            elif ex_name == "xls":
                res["Content-type"] = "application/vnd.ms-excel"
            elif ex_name == "docx":
                res["Content-type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            elif ex_name == "ppt":
                res["Content-type"] = "application/vnd.ms-powerpoint"
            elif ex_name == "pptx":
                res["Content-type"] = "application/vnd.openxmlformats-officedocument.presentationml.presentation"

            else:
                raise Http404("文档格式不正确！")

            doc_filename = escape_uri_path(doc_url.split('/')[-1])
            # 设置为inline，会直接打开
            res["Content-Disposition"] = "attachment; filename*=UTF-8''{}".format(doc_filename)
            return res

        else:
            raise Http404("文档不存在！")
