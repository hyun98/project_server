import datetime
from uuid import uuid4

from django.db import models
from django.conf import settings



class Survey(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    description = models.TextField(default="", null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="survey")
    
    class Meta:
        verbose_name = '지원/설문'
        verbose_name_plural = '지원/설문'
        ordering = ['-start_date', ]
    
    def __str__(self):
        return self.title
    
    def has_permission(self, user):
        return True if self.creator == user else False


class Question(models.Model):
    content = models.TextField(default="", null=True, blank=True)
    order = models.PositiveIntegerField(null=True, blank=True)
    is_multichoice = models.BooleanField(default=False)
    can_duplicate = models.BooleanField(default=False)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="question")
    
    def __str__(self):
        return self.content


class SubQuestion(models.Model):
    sub_content = models.CharField(max_length=128, null=True, blank=True)
    can_select = models.BooleanField(default=False)
    top_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="sub_question")
    
    def __str__(self):
        return self.sub_content
    
    
class Applier(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True)
    birth = models.CharField(max_length=32, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    is_applied = models.BooleanField(default=False)
    is_picked = models.BooleanField(default=False)
    is_favor = models.BooleanField(default=False)
    
    apply_date = models.DateTimeField(auto_now_add=True)
    
    GENDER_CHOICE = (
        ("M", "남자"),
        ("F", "여자")
    )
    gender = models.CharField(max_length=8, choices=GENDER_CHOICE)
    
    survey = models.ForeignKey(Survey, null=True, on_delete=models.SET_NULL, related_name="applier")
    
    class Meta:
        verbose_name = '지원자'
        verbose_name_plural = '지원자'
        ordering = ['-apply_date']
    
    def __str__(self):
        return self.name
    

class Answer(models.Model):
    answer = models.TextField(default="", null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answer")
    applier = models.ForeignKey(Applier, on_delete=models.CASCADE, related_name="answer")
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="answer")
    
    def __str__(self):
        return self.answer


def get_file_path(instance, filename):
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    return '/'.join(['upload_file_apply/', ymd_path, uuid_name])


class ApplyFile(models.Model):
    apply_file = models.FileField(upload_to=get_file_path, null=True, blank=True, verbose_name='파일')
    filename = models.CharField(max_length=128, null=True, verbose_name='첨부파일명')
    
    applier = models.ForeignKey(Applier, on_delete=models.CASCADE, related_name="applyfile")
    
    class Meta:
        verbose_name = '지원서 첨부파일'
        verbose_name_plural = '지원서 첨부파일'
    
    def __str__(self):
        return self.filename
