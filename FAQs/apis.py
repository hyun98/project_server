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
        QA_list = Question.objects.select_related(
            'answer'
        ).all()
        
        data_list = []
        
        for qa in QA_list:
            temp = {
                'question': qa.question,
                'answer': qa.answer.answer
            }
            data_list.append(temp)
        data = {"faqs": data_list}
        return Response(data, status=status.HTTP_200_OK)
        