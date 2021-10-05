import datetime
from uuid import uuid4

from django.db import models
from django.conf import settings
from django.utils import timezone


User = settings.AUTH_USER_MODEL


def get_file_path(instance, filename):
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    return '/'.join(['reservation_file/', ymd_path, uuid_name])


class Reservation(models.Model):
    title = models.CharField(max_length=128, null=True, blank=False)
    description = models.TextField(default='', null=True, blank=True)
    floor = models.IntegerField(default=1, blank=False)
    
    start_time = models.TimeField(null=True, blank=False)
    end_time = models.TimeField(null=True, blank=False)
    
    # reservation_file = models.FileField(
    #     upload_to=get_file_path, null=True, blank=True, verbose_name='예약파일')
    
    reserve_date = models.DateField(blank=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(auto_now=True)
    
    booker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservation')
    
    
    class Meta:
        verbose_name = '예약 현황'
        verbose_name_plural = '예약 현황 모음'
        ordering = ['reserve_date', ]
        
    def __str__(self):
        return self.title
    