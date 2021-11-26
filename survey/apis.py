from rest_framework import viewsets
from rest_framework.views import Response, status

from django.db import transaction

from api.mixins import PublicApiMixin
from survey.serializers import *
from survey.models import *


class SurveyApi(PublicApiMixin, viewsets.ModelViewSet):
    queryset = Survey.objects.select_related(
            'creator'
        ).\
        prefetch_related(
            'question',
            'question__sub_question'
        ).\
        all()
    
    serializer_class = SurveySerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        return super().destroy(request, *args, **kwargs)
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        if not request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        title = request.data.get('title', '')[0]
        description = request.data.get('description', '')[0]
        start_date = request.data.get('start_date', '')[0]
        due_date = request.data.get('due_date', '')[0]
        creator = request.user
        
        question_list = request.data.get('question', '')
        
        survey = Survey(
            title=title,
            description=description,
            start_date=start_date,
            due_date=due_date,
            creator=creator
        )
        survey.save()
        
        for q in question_list:
            content = q['content'][0]
            order = q['order'][0]
            is_multichoice = q['is_multichoice'][0]
            can_duplicate = q['can_duplicate'][0]
            subquestion_list = q['sub_question']
            
            question = Question(
                survey=survey,
                content=content,
                order=order,
                is_multichoice=is_multichoice,
                can_duplicate=can_duplicate
            )
            question.save()
            
            for sq in subquestion_list:
                sub_content = sq['sub_content'][0]
                can_select = sq['can_select'][0]
                
                SubQuestion(
                    top_question=question,
                    sub_content=sub_content,
                    can_select=can_select
                ).save()
            
        return Response(status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    
class ApplyApi(PublicApiMixin, viewsets.ModelViewSet):
    
    def retrieve(self, request, *args, **kwargs):
        """
        지원서 하나 확인
        ** 지원서를 만든 계정만 지원서를 볼 수 있음 **
        0. 지원서 종류 확인 -> 지원서 id 받아야함
        1. 지원자 이름, 생년월일, 휴대폰 번호를 가지고 지원자 id 추려냄
        2. 해당 지원서에서 지원자의 응답을 추려서 반환
        
        """
        survey_id = request.data.get('survey_id')[0]
        applier_phone = request.data.get('phone')[0]
        applier_name = request.data.get('name')[0]
        applier_birth = request.data.get('birth')[0]
        
        survey = Survey.objects.get(pk=survey_id)
        
        if not survey.has_permission(request.user):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        applier = Applier.objects.filter(
            name=applier_name,
            phone=applier_phone,
            birth=applier_birth
        )
        
        if not applier.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        applier = applier.first()
        
        answer_list = Answer.objects.select_related(
                'question'
            ).\
            filter(
                survey=survey,
                applier=applier
            )
        
        
        
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
        
    
    def list(self, request, *args, **kwargs):
        """
        지원서 전체 리스트로 확인
        ** 지원서를 만든 계정만 지원서를 볼 수 있음 **
        지원 종류 | 지원자 이름 | 지원자 생년월일 | 지원자 학교 | 지원자 번호
        위 정보 반환
        """
        
        
        
        return super().list(request, *args, **kwargs)
    
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        지원하기
        # 지원서 제출 시 server 동작
        1. 지원자 정보 저장 -> 지원자 id 생성
        2. question에 대응하는 answer 저장 -> 각 answer 마다 대응된 question_id 저장
        3. sub_question이 있는 경우 -> 
            sub_question에서 선택하거나 적은 정보들을 모두 text로 answer에 저장.
        """
        
        # 지원자 정보
        applier_phone = request.data.get('phone')[0]
        applier_name = request.data.get('name')[0]
        applier_birth = request.data.get('birth')[0]
        applier_gender = request.data.get('gender')[0]
        
        # 지원서 정보
        survey_id = request.data.get('survey_id')[0]
        
        applier = Applier(
            name=applier_name,
            birth=applier_birth,
            phone=applier_phone,
            gender=applier_gender,
            survey=survey_id
        )
        applier.save()
        
        # 응답 정보
        answer_list = request.data.get('answers')
        
        for answer in answer_list:
            q_id = answer["question_id"][0]
            ans = ", ".join(answer["answer"])
            Answer(
                answer=ans,
                question=q_id,
                applier=applier
            ).save()
        
        return Response(status=status.HTTP_201_CREATED)
    
