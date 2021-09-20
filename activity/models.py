from uuid import uuid4
from datetime import datetime

from django.db import models


def get_file_path(instance, filename):
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    return '/'.join(['activity_detail_file/', ymd_path, uuid_name])


class Activity(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    date = models.DateField(auto_now_add=False, auto_now=False)
    thumbnail = models.ImageField(upload_to='activity_thumbnail/', null=True, blank=True)
    
    class Meta:
        verbose_name = '활동 내역'
        verbose_name_plural = '활동 내역 모음'
        ordering = ['-date', ]
        
    def __str__(self):
        return self.title


class ActivityDetail(models.Model):
    title = models.CharField(max_length=128)
    image = models.ImageField(upload_to='activity_detail', null=True, blank=True)
    activity_file = models.FileField(upload_to=get_file_path, null=True, blank=True, verbose_name='활동파일')
    description = models.TextField()

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    class Meta:
        verbose_name = '활동 세부사항'
        verbose_name_plural = '활동 세부 모음'
        
    def __str__(self):
        return self.title
    

class ActivityDetailImage(models.Model):
    image = models.ImageField(upload_to='activity_detail', null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0, null=True)
    activity_detail = models.ForeignKey(ActivityDetail, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = '활동 사진'
        verbose_name_plural = '활동 사진 모음'
        ordering = ['order', ]
        
    