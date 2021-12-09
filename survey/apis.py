import urllib
import os
import json
import mimetypes

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

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
            ).prefetch_related(
                'question',
                'question__sub_question'
            ).all()
        
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
            description = q['description'][0]
            order = q['order'][0]
            require = q['required'][0]
            is_multichoice = q['is_multichoice'][0]
            can_duplicate = q['can_duplicate'][0]
            subquestion_list = q['sub_question']
            
            question = Question(
                survey=survey,
                content=content,
                description=description,
                order=order,
                is_multichoice=is_multichoice,
                required=require,
                can_duplicate=can_duplicate
            )
            question.save()
            
            for sq in subquestion_list:
                sub_content = sq['sub_content'][0]
                if not sub_content:
                    break
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
            condition.add(Q(name__icontains=kw) | Q(univ__icontains=kw), Q.AND)
            
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
        print("지원 상황: ", request.data.get('data'))
        print("파일 : ", request.FILES)
        
        data = json.loads(request.data.get('data'))
        
        # 지원자 정보
        applier_phone = data.get('phone')[0]
        applier_name = data.get('name')[0]
        applier_birth = data.get('birth')[0]
        applier_gender = data.get('gender')[0]
        applier_univ = data.get('univ')[0]
        is_applied = data.get('is_applied')[0]
        
        # 지원서 정보
        survey_id = data.get('survey_id')[0]
        survey = Survey.objects.get(pk=survey_id)
        
        applier, flag = Applier.objects.get_or_create(
            name=applier_name,
            birth=applier_birth,
            phone=applier_phone,
            survey=survey
        )
        applier.gender=applier_gender
        applier.univ=applier_univ
        applier.is_applied=is_applied
        
        applier.save()
        applier_str = applier_name + "_"
        
        # 응답 정보
        answer_list = data.get('answers')
        
        for answer in answer_list:
            q_id = answer["question_id"][0]
            question = Question.objects.get(pk=q_id)
            ans = ", ".join(answer["answer"])
            answer, flag = Answer.objects.get_or_create(
                question=question,
                applier=applier,
                survey=survey
            )
            answer.answer=ans
            answer.save()
        
        # 파일 저장. 임시저장인 경우 파일 저장 안됨
        if not applier.is_applied:
            return Response(status=status.HTTP_201_CREATED)
        
        files = request.FILES.getlist('files')
        for file in files:
            applyfile = ApplyFile(
                apply_file=file,
                filename=applier_str+file.name,
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
        ).order_by('order')
        applierDf = createApplierDF(question_list)
        
        applier_query = Applier.objects.prefetch_related(
            'answer',
            'answer__question'
        ).filter(
            survey=survey,
            is_applied=True
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
            'answer__question',
            'applyfile'
        ).get(
            pk=applier_id,
            survey=survey
        )
        
        applier_data = ApplierSerializer(applier_query).data
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
        현재 설문지의 작성자와 로그인 되어있는 유저가 동일하면 다운로드 가능
        url로 전달받은 파일
        """
        file = get_object_or_404(ApplyFile, pk=kwargs['file_id'])
        url = file.apply_file.url[1:]
        file_url = urllib.parse.unquote(url)
            
        if os.path.exists(file_url):
            with open(file_url, 'rb') as f:
                quote_file_url = urllib.parse.quote(file.filename.encode('utf-8'))
                response = HttpResponse(
                    f.read(), content_type=mimetypes.guess_type(quote_file_url)[0]
                )
                response['Content-Disposition'] = 'attachment;filename*=utf-8\'\'%s' % quote_file_url
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
        
        if applier.is_favor:
            applier.is_favor = False
        else:
            applier.is_favor = True
        applier.save()
        
        return Response(status=status.HTTP_202_ACCEPTED)


class ApplierSelfCheckApi(PublicApiMixin, APIView):
    def post(self, request, *args, **kwargs):
        """
        지원자 자신의 정보를 모두 가져올 수 있다.
        if 지원서의 지원 종료 기간 이전 && 지원자가 임시저장한 경우:
            지원자의 모든 정보를 전달한다.
        else if 지원서의 지원 종료기간 이후 && 지원자가 제대로 지원을 한 경우:
            지원자의 합격 여부를 전달한다.
        """
        survey_id = kwargs["survey_id"]
        applier_name = request.data.get('name', '')[0]
        applier_phone = request.data.get('phone', '')[0]
        applier_birth = request.data.get('birth', '')[0]
        
        if not applier_name or not applier_phone or not applier_birth:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
        survey = Survey.objects.get(pk=survey_id)
        
        applier = Applier.objects.prefetch_related(
            'answer',
            'answer__question',
            'applyfile'
        ).filter(
            name=applier_name,
            phone=applier_phone,
            birth=applier_birth,
            survey=survey
        )
        
        if not applier.exists():
            return Response({
            "message": "지원자 정보를 찾을 수 없습니다."
        },status=status.HTTP_404_NOT_FOUND)
        applier = applier.first()
        
        from time import mktime, strptime
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        today = strptime(today, "%Y-%m-%d")
        due_date = strptime(survey.due_date, "%Y-%m-%d") 
        
        utc_today = mktime(today) * 1000
        utc_due = mktime(due_date) * 1000
        applier_data = {}
        applier_data["due_date"] = due_date
        
        if today <= due_date and not applier.is_applied:
            # 임시저장 정보 불러오기
            applier_data = ApplierSerializer(applier).data
            return Response(applier_data, status=status.HTTP_200_OK)
        elif today > due_date and applier.is_applied:
            # 지원 기간이 지나서 합격 여부 불러오기
            applier_data["is_picked"] = applier.is_picked
            return Response(applier_data, status=status.HTTP_200_OK)
        
        return Response({
            "message": "정보를 불러올 수 없습니다."
            },status=status.HTTP_403_FORBIDDEN)


class ApplierDuplicateCheck(PublicApiMixin, APIView):
    def post(self, request, *args, **kwargs):
        survey_id = kwargs["survey_id"]
        applier_name = request.data.get('name', '')[0]
        applier_phone = request.data.get('phone', '')[0]
        applier_birth = request.data.get('birth', '')[0]
    
        if not applier_name or not applier_phone or not applier_birth:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
        survey = Survey.objects.get(pk=survey_id)
        
        applier = Applier.objects.filter(
            name=applier_name,
            phone=applier_phone,
            birth=applier_birth,
            survey=survey
        )
        
        if not applier.exists():
            return Response({
            "message": "지원 가능합니다."
        },status=status.HTTP_200_OK)
        
        applier = applier.first()
        if not applier.is_applied:
            return Response({
                "message": "임시 저장된 지원서가 존재합니다."
            },status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "이미 지원하였습니다."
            },status=status.HTTP_403_FORBIDDEN)
