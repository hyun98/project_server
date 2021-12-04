import os
import logging

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import FileResponse
from django.http.response import Http404
from django.conf import settings

from api.mixins import PublicApiMixin

BASE_DIR = settings.BASE_DIR
logger = logging.getLogger('project')


class getLogApi(PublicApiMixin, APIView):
    def get(self, request):
        file_path = os.path.join(BASE_DIR, 'logs/projectlog.log')

        try:
            return FileResponse(open(file_path, 'rb'))
        except:
            raise Http404()


class getLogTextApi(PublicApiMixin, APIView):
    def get(self, request, *args, **kwargs):
        logger.info("call getLogTextApi")
        
        file_path = os.path.join(BASE_DIR, 'logs/projectlog.log')
        logfile = open(file_path, 'r')
        log = ""
        for line in logfile:
            log = log + line + "\n"
        logfile.close()
        
        data = {'log': log}
        
        return Response(data, status=status.HTTP_200_OK)
