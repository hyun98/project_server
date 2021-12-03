import urllib
import os
import mimetypes

from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.views import Response, status, APIView
from rest_framework.exceptions import NotFound

from django.db import transaction
from django.db.models import Q
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404

from api.mixins import ApiAuthMixin, PublicApiMixin
from survey.serializers import *
from survey.models import *
from survey.services import createApplierDF, addApplierDF


class SurveyApi(ApiAuthMixin, APIView):
    def get(self, request, *args, **kwargs):
        """
        현재 만들어진 지원/설문지 리스트 출력
        """
        queryset = Survey.objects.select_related(
                'creator'
            ).\
            prefetch_related(
                'question',
                'question__sub_question'
            ).\
            all()
        
        serializer = SurveySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
        지원서 생성
        """
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
        

class SurveyDetailApi(PublicApiMixin, APIView):
    def get(self, request, *args, **kwargs):
        """
        id에 맞는 survey 선택
        """
        survey_id = kwargs["survey_id"]
        object = Survey.objects.get(pk=survey_id)
        serializer = SurveySerializer(object)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        """
        id에 맞는 survey 삭제
        """
        survey_id = kwargs["survey_id"]
        
        if not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        survey = Survey.objects.get(pk=survey_id)
        survey.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApplyApi(PublicApiMixin, APIView):
    parser_classes = (FileUploadParser, MultiPartParser, )
    
    def get(self, request, *args, **kwargs):
        """
        지원자 전체 리스트로 확인
        ** 지원서를 만든 계정만 지원서를 볼 수 있음 **
        지원자 이름 | 지원자 생년월일 | 지원자 성별 | 지원자 휴대폰 번호 | 지원 시간 | 관심 | 뽑혔는지
        위 정보 반환
        """
        kw = request.GET.get("kw", '')
        survey_id = kwargs['survey_id']
        survey = Survey.objects.get(pk=survey_id)
        
        if not survey.has_permission(request.user):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        condition = Q(survey=survey)
        condition.add(Q(is_applied=True), Q.AND)
        
        if kw:
            condition.add(Q(name__icontains=kw) | Q(univ__icontains=kw))
            
        applier_query = Applier.objects.filter(
            condition
        )
        serializer = ApplierListSerializer(applier_query, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
        지원하기
        # 지원서 제출 시 server 동작
        1. 지원자 정보 저장 -> 지원자 id 생성
        2. question에 대응하는 answer 저장 -> 각 answer 마다 대응된 question_id 저장
        3. sub_question이 있는 경우 -> 
            sub_question에서 선택하거나 적은 정보들을 모두 text로 answer에 저장.
        """
        print("지원 상황: ", request.data)
        
        # 지원자 정보
        applier_phone = request.data.get('phone')[0]
        applier_name = request.data.get('name')[0]
        applier_birth = request.data.get('birth')[0]
        applier_gender = request.data.get('gender')[0]
        applier_univ = request.data.get('univ')[0]
        is_applied = request.data.get('is_applied')[0]
        
        # 지원서 정보
        survey_id = request.data.get('survey_id')[0]
        survey = Survey.objects.get(pk=survey_id)
        
        applier = Applier(
            name=applier_name,
            birth=applier_birth,
            phone=applier_phone,
            gender=applier_gender,
            univ=applier_univ,
            is_applied=is_applied,
            survey=survey
        )
        applier.save()
        
        # 응답 정보
        answer_list = request.data.get('answers')
        
        for answer in answer_list:
            q_id = answer["question_id"][0]
            question = Question.objects.get(pk=q_id)
            ans = ", ".join(answer["answer"])
            Answer(
                answer=ans,
                question=question,
                applier=applier,
                survey=survey
            ).save()
        
        # 파일 저장
        files = request.data.get('applyfiles')
        
        for file in files:
            print("file", file)
            applyfile = ApplyFile(
                apply_file=file,
                filename=file.name,
                applier=applier
            )
            applyfile.save()
        
        return Response(status=status.HTTP_201_CREATED)


class ApplierCSVApi(PublicApiMixin, APIView):
    def get(self, request, *args, **kwargs):
        """
        survey/{설문지번호}/appliercsv
        해당 설문지 응답 리스트 csv파일로 다운로드
        """
        survey_id = kwargs["survey_id"]
        survey = Survey.objects.get(pk=survey_id)
        
        question_list = Question.objects.filter(
            survey=survey
        ).\
        order_by('order')
        applierDf = createApplierDF(question_list)
        
        applier_query = Applier.objects.prefetch_related(
            'answer',
            'answer__question'
        ).\
        filter(
            survey=survey
        ).order_by('apply_date')
        applierDf = addApplierDF(applier_query, applierDf)
        
        response = HttpResponse(content_type='text/csv', charset="utf-8")
        filename = "{}.csv".format("".join(survey.title.split()))
        filename = urllib.parse.quote(filename.encode('utf-8'))
        response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(filename)
        applierDf.to_csv(path_or_buf=response)
        return response


class ApplierDetailApi(PublicApiMixin, APIView):
    def get(self, request, *args, **kwargs):
        """
        ** 지원서를 만든 계정만 지원서를 볼 수 있음 **
        관리자가 지원서 하나 확인
        0. 지원서 종류 확인 -> 지원서 id 받아야함
        1. 지원자 id url로 받음
        2. 해당 지원서에서 지원자의 응답을 추려서 반환
        """
        applier_id = kwargs["applier_id"]
        survey_id = kwargs["survey_id"]
        
        survey = Survey.objects.get(pk=survey_id)
        
        if not survey.has_permission(request.user):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        applier_query = Applier.objects.prefetch_related(
            'answer',
            'applyfile'
        ).\
        filter(
            pk=applier_id,
            survey=survey
        )
        
        applier_data = ApplierSerializer(applier_query, many=True).data
        return Response(applier_data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        """
        해당 지원자 합/불
        """
        applier_id = kwargs["applier_id"]
        survey_id = kwargs["survey_id"]
        survey = Survey.objects.get(id=survey_id)
        applier = Applier.objects.get(
            pk=applier_id,
            survey=survey
        )
        
        if applier.is_picked:
            applier.is_picked = False
        else:
            applier.is_picked = True
        applier.save()
        
        return Response(status=status.HTTP_202_ACCEPTED)


class ApplierFileDownloadApi(PublicApiMixin, APIView):
    def get(self, request, *args, **kwargs):
        """
        
        """
        file = get_object_or_404(ApplyFile, pk=kwargs['file_id'])
        url = file.apply_file.url[1:]
        file_url = urllib.parse.unquote(url)
            
        if os.path.exists(file_url):
            with open(file_url, 'rb') as f:
                quote_file_url = urllib.parse.quote(file.filename.encode('utf-8'))
                response = HttpResponse(
                    f.read(), content_type=mimetypes.guess_type(file_url)[0]
                )
                response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
                return response
        else:
            raise NotFound


class ApplierFavorApi(PublicApiMixin, APIView):
    def post(self, request, *args, **kwargs):
        """
        해당 지원자 관심 선택/해제
        """
        applier_id = kwargs["applier_id"]
        survey_id = kwargs["survey_id"]
        survey = Survey.objects.get(id=survey_id)
        applier = Applier.objects.get(
            pk=applier_id,
            survey=survey
        )
        
        if applier.is_picked:
            applier.is_favor = False
        else:
            applier.is_favor = True
        applier.save()
        
        return Response(status=status.HTTP_202_ACCEPTED)
    

class ApplierSelfCheckApi(PublicApiMixin, APIView):
    def get(self, request, *args, **kwargs):
        survey_id = kwargs["survey_id"]
        applier_name = request.data.get('name', '')[0]
        applier_phone = request.data.get('phone', '')[0]
        applier_birth = request.data.get('birth', '')[0]
        
        if not applier_name or not applier_phone or not applier_birth:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
        survey = Survey.objects.get(pk=survey_id)
        
        applier = Applier.objects.prefetch_related(
            'question',
            'answer'
            'applyfile'
        ).\
        filter(
            name=applier_name,
            phone=applier_phone,
            birth=applier_birth,
            survey=survey
        )
        
        if not applier.exists():
            return Response({
            "message": "지원자 정보를 찾을 수 없습니다."
        },status=status.HTTP_404_NOT_FOUND)
        
        applier_data = ApplierSerializer(applier).data
        applier_data["due_date"] = survey.due_date
        return Response(applier_data, status=status.HTTP_200_OK)
    