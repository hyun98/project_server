from api.mixins import PublicApiMixin
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from activity.models import Activity, ActivityDetail, ActivityDetailImage


class ActivityReadApi(PublicApiMixin, APIView):
    def get(self, request, *args, **kwargs):
        data_list = []
        
        activity_list = Activity.objects.all()
        
        for activity in activity_list:
            title = activity.title
            description = activity.description
            thumbnail = activity.thumbnail.url
            date = activity.date
            
            parse_year = int(str(date)[:4])
            parse_month = int(str(date)[5:7])
            
            temp = {
                'id': activity.id,
                'title': title,
                'description': description,
                'thumbnail': thumbnail,
                'year': parse_year,
                'month': parse_month,
            }
            
            data_list.append(temp)
            
        data = {
            'data': data_list
        }
        
        return Response(data, status=status.HTTP_200_OK)
    

class ActivityDetailApi(PublicApiMixin, APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        activity = get_object_or_404(Activity, id=id)
        
        activity_detail_list = ActivityDetail.objects.filter(activity__id=id)
        
        data_list = []
        
        for detail in activity_detail_list:
            
            temp = {
                'id': detail.id,
                'title': detail.title,
                'image': detail.image.url,
                
            }
            
            data_list.append(temp)
            
        data = {
            'data': data_list,
            'description': activity.description,
        }
        
        return Response(data, status=status.HTTP_200_OK)
            
        
class ActivityDetailImageApi(PublicApiMixin, APIView):
    def get(self, request, *args, **kwargs):
        detail_id = kwargs['detail_id']
        activity_detail = get_object_or_404(ActivityDetail, id=detail_id)
        
        activity_detail_image_list = ActivityDetailImage.objects.filter(
            activity_detail__id=detail_id
        )
        image_list = []
        for image in activity_detail_image_list:
            image_list.append(image.image.url)
        
        data = {
            "images": image_list,
            "description": activity_detail.description,
        }
        
        return Response(data, status=status.HTTP_200_OK)

        