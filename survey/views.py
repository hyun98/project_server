from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.db.models import Q
from django.conf import settings

from survey.models import *


def ApplierList(request, pw):
    if pw != settings.SURVEY_PW:
        return Http404
    return render(request, 'applierlist.html')


class ApplierListView(ListView):
    model = Applier
    context_object_name = 'applier_list'
    template_name = 'applierlist.html'
    
    def get_queryset(self):
        kw = self.request.GET.get('kw', '')
        pw = self.request.GET.get('pw', '')
        if pw != settings.SURVEY_PW:
            return Applier.objects.none()
        
        Applier_queryset = Applier.objects.order_by('name')
        if kw:
            Applier_queryset = Applier_queryset.filter(
                (Q(name__contains=kw) | Q(univ__contains=kw)),
                is_picked=True
            ).distinct()
            
            return Applier_queryset
        else:
            Applier_queryset = Applier_queryset.filter(
                is_picked=True
            )
            return Applier_queryset


def ApplierDetail(request, pk):
    if request.method != 'POST':
        return HttpResponse("403 Forbidden")
    
    applier = Applier.objects.get(pk=pk)
    survey = applier.survey
    
    questions = Question.objects.filter(survey=survey).order_by('order')
    
    context = {
        'applier': applier,
        'qalist': [], 
        'files': []
    }
    for q in questions:
        answer = Answer.objects.get(question=q, applier=applier, survey=survey)
        temp = {
            'q': q.content,
            'qd': q.description,
            'answer': answer.answer
        }
        context['qalist'].append(temp)
    
    files = ApplyFile.objects.filter(applier=applier)
    for f in files:
        temp = {
            'name': f.filename,
            'url': f.apply_file.url
        }
        context['files'].append(temp)
    
    return render(request, 'applierdetail.html', context=context)
