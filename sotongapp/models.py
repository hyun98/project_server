from django.db import models


class Organ(models.Model):
    name = models.CharField(help_text="기관명", max_length=30)
    urlname = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Information(models.Model):
    temp = models.FloatField(help_text="온도")
    day = models.DateField(help_text="날짜")
    time = models.TimeField(help_text="시간")
    organ = models.ForeignKey(Organ, on_delete=models.CASCADE, related_name='organ')

    def __str__(self):
        return str(self.time)