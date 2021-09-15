from django.db import models


class Question(models.Model):
    question = models.TextField(null=True)
    order = models.PositiveIntegerField(default=0, null=True)
    
    class Meta:
        verbose_name = '자주 묻는 질문'
        verbose_name_plural = '자주 묻는 질문들'
        ordering = ['order', ]
        
    def __str__(self):
        return self.question


class Answer(models.Model):
    answer = models.TextField(null=True)
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name="answer")
   
    def __str__(self):
        return self.answer