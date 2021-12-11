from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.db import transaction

from api.mixins import PublicApiMixin, ApiAuthMixin
from reservations.models import Reservation
from reservations.serializers import ReservationCreateSerializer

# ApiAuthMixin으로 교체 필요
# class ReserveCountApi(PublicApiMixin, APIView):
#     def get(self, request, *args, **kwargs):
#         month = kwargs['month']
        


# ApiAuthMixin으로 교체 필요
class ReserveApi(ApiAuthMixin, APIView):
    def get(self, request, *args, **kwargs):
        """
        선택한 date에 예약되어있는 예약 리스트 반환
        """
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


class ReserveCreateApi(PublicApiMixin, APIView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
        예약하기 기능
        title, start_time, end_time, floor, 로그인 필수
        """
        serializer = ReservationCreateSerializer(
            data=request.data,
            context={
                'request': self.request,
                'reserve_date': kwargs['date'],
            }
        )
        if not serializer.is_valid(raise_exception=True):
            return Response({
                "message": "Request Body Error"
                }, status=status.HTTP_409_CONFLICT)

        reservation = serializer.save()
        
        return Response({
            "message": "Reservation completed"
        }, status=status.HTTP_201_CREATED)
        
    