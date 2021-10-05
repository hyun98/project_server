from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.mixins import PublicApiMixin
from FAQs.models import Answer, Question



class FAQslistAPI(PublicApiMixin, APIView):
    def get(self, request, *args, **kwargs):
        """
        FAQ 리스트 반환
        question : answer
        """
        QA_list = Question.objects.all()
        
        data_list = []
        
        for qa in QA_list:
            answer = Answer.objects.get(question=qa)
            temp = {
                'question': qa.question,
                'answer': answer.answer
            }
            
            data_list.append(temp)
            
        return Response(data_list, status=status.HTTP_200_OK)
        
        