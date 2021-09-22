from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


from api.mixins import PublicApiMixin, ApiAuthMixin
from reservations.models import Reservation


# ApiAuthMixin으로 교체 필요
# class ReserveCountApi(PublicApiMixin, APIView):
#     def get(self, request, *args, **kwargs):
#         month = kwargs['month']
        


# ApiAuthMixin으로 교체 필요
class ReserveApi(PublicApiMixin, APIView):
    def get(self, request, *args, **kwargs):
        date = kwargs['date']
        
        reserve_list = Reservation.objects.filter(reserve_date=date)
        
        data_list = []
        
        for rev in reserve_list:
            info = {
                "year": rev.reserve_date.year,
                "month": rev.reserve_date.month,
                "day": rev.reserve_date.day,
                "booker": rev.booker.profile.nickname,
                "title": rev.title,
                "starttime": rev.start_time,
                "endtime": rev.end_time,
                "description": rev.description,
                "floor": rev.floor,
            }
            
            data_list.append(info)
        
        return Response({
            "data":data_list,
            
        }, status=status.HTTP_200_OK)
        
    
    def post(self, request, *args, **kwargs):
        date = request.data.get('date')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        title = request.date.get('title', '')
        description = request
        
        
        
        
    # def post(self, request, *args, **kwagrs):
        
        
    