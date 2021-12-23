from datetime import datetime
from django.conf.urls import url

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from api.mixins import PublicApiMixin

from sotongapp.models import Organ, Information
from sotongapp.serializer import InfoSerializer
from sotongapp.utils import get_maxvnum_avgnum


class SaveTempDataApi(PublicApiMixin, APIView):
    def post(self, request, *args, **kwargs):
        """
        아두이노에서 date, time, temp 값을 받아서
        데이터베이스에 저장한다.
        """
        organ = get_object_or_404(Organ, urlname=request.data.get('organ', ''))
        day = request.data.get('date', '')
        time = request.data.get('time', '')
        temp = request.data.get('temp', '')
        
        day = datetime.strptime(day, "%Y-%m-%d")
        time = datetime.strptime(time, "%H:%M:%S")
        temp = round(float(temp), 2)
        info = Information(organ=organ, temp=temp, day=day, time=time)
        info.save()
        
        return Response({
            "message": "Success get data",
        }, status=status.HTTP_200_OK)


### fake ###
from random import randrange, uniform

def randDate():
    date = ['2021']
    while(True):
        month = randrange(9, 13)
        day = randrange(1, 31)
        if month == 9 and day < 27:
            continue
        elif month == 12 and day > 22:
            continue
        else:
            date.append(str(month))
            date.append(str(day))
            break
        
    return '-'.join(date)

def randTime():
    t = []
    h = randrange(9, 18)
    m = randrange(0, 60)
    s = randrange(0, 60)
    t.append(str(h))
    t.append(str(m))
    t.append(str(s))
    
    return ':'.join(t)

def randTemp():
    temp = round(float(uniform(35, 37)),2)
    return temp

def makedata(cnt, name):
    for _ in range(cnt):
        organ = get_object_or_404(Organ, urlname=name)
        day = randDate()
        time = randTime()
        temp = randTemp()
        
        day = datetime.strptime(day, "%Y-%m-%d")
        time = datetime.strptime(time, "%H:%M:%S")
        info = Information(organ=organ, temp=temp, day=day, time=time)
        info.save()

class makeSampleData(PublicApiMixin, APIView):
    def get(self, request, *args, **kwargs):
        if kwargs['pw'] != '0404':
            return Response(status=status.HTTP_404_NOT_FOUND)
        urlnames = ["project", 'bobel', 'ksu', 'vitamin', 'hyouth', 'volteer', 'deunsol']
        cnts = [285, 197, 84, 217, 176, 91, 87]
        for i in range(7):
            makedata(cnt=cnts[i], name=urlnames[i])
        
        return Response(status=status.HTTP_200_OK)


def AllUserCount(request):
    cnt = Information.objects.count()
    data = {
        'count': cnt
    }
    return JsonResponse(data)


class InfoViewSet(viewsets.ModelViewSet):
    queryset = Information.objects.order_by('-day', '-time')
    serializer_class = InfoSerializer
    permission_classes = ()
    authentication_classes = ()

    def get_queryset(self):
        return super().get_queryset().filter(organ__urlname=self.request.GET['search'])


def GetOrganName(request, urlname):
    organ = get_object_or_404(Organ, urlname=urlname)
    data = {
        "name": organ.name
    }
    return JsonResponse(data)


class GetVisitorView(PublicApiMixin, APIView):
    def get(self, request, urlname):
        """
        선택한 기관의 전체 사용자 수, 오늘 사용자 수,
        평균 사용자 수, 하루 최대 사용자 수를 제공한다.
        """
        organ = get_object_or_404(Organ, urlname=urlname)
        totaluser = Information.objects.filter(organ=organ).count()
        todayuser = Information.objects.filter(
            Q(day=datetime.today()) &
            Q(organ=organ)
        ).count()
        avguser, maxuser = get_maxvnum_avgnum(totaluser, organ)
        
        data = {
            "totaluser": totaluser,
            "todayuser": todayuser,
            "avguser": avguser,
            "maxuser": maxuser
        }
        
        return Response(data)
    