from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from survey.models import *

admin.site.register(SubQuestion)
admin.site.register(Answer)


class QuestionInline(admin.StackedInline):
    model = Question
    can_delete = True
    verbose_name_plural = "question"
    
class SubQuestionInline(admin.StackedInline):
    model = SubQuestion
    can_delete = True
    verbose_name_plural = "subquestion"

class AnswerInline(admin.StackedInline):
    model = Answer
    can_delete = False
    verbose_name_plural = "answer"
    
class ApplyFileInline(admin.StackedInline):
    model = ApplyFile
    can_delete = False
    verbose_name_plural = "applyfile"
    
    
@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    ordering = ('-created_date', )
    list_display = (
        'id', 'title', 'description', 'start_date', 'due_date',
        'created_date', 'get_creator'
    )
    list_display_links = (
        'id', 'title', 'description', 'start_date', 'due_date',
        'created_date', 'get_creator'
    )
    search_fields = ('title', 'description', 'creator__profile__nickname', )
    list_filter = ('start_date', 'due_date', 'creator', )
    
    list_select_related = [
        'creator',
        'creator__profile',
    ]
    inlines = (QuestionInline, )
    
    def get_creator(self, obj):
        creator = obj.creator.profile.nickname
        return creator
    get_creator.short_description = _("creator")
    
    
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    ordering = ('-survey__start_date', 'order')
    list_display = (
        'id', 'content', 'description', 'order', 'is_multichoice',
        'required', 'can_duplicate'
    )
    list_display_links = (
        'id', 'content', 'description', 'order', 'is_multichoice',
        'required', 'can_duplicate'
    )
    search_fields = ('content', 'description', )
    
    list_select_related = [
        'survey',
    ]

    inlines = (SubQuestionInline, )
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related(
            'sub_question'
        )

@admin.register(Applier)
class ApplierAdmin(admin.ModelAdmin):
    ordering = ('-apply_date', 'name')
    list_display = (
        'id', 'get_survey', 'apply_date', 'name', 'birth', 'phone', 'univ', 'gender',
        'is_picked', 'is_favor', 'is_applied', 
    )
    list_display_links = (
        'id', 'get_survey', 'apply_date', 'name', 'birth', 'phone', 'univ', 'gender',
        'is_picked', 'is_favor', 'is_applied', 
    )
    search_fields = ('name', 'univ', 'phone',)
    list_filter = ('univ', 'is_picked', 'is_favor', 'is_applied')
    
    list_select_related = [
        'survey',
    ]

    inlines = (AnswerInline, ApplyFileInline, )
    
    def get_survey(self, obj):
        try:
            survey = obj.survey.title
        except:
            survey = ''
        return survey
    get_survey.short_description = _("survey")
    

@admin.register(ApplyFile)
class ApplyFileAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'get_apply_date', 'get_applier', 'filename',
    )
    list_display_links = (
        'get_apply_date', 'get_applier', 'filename',
    )
    search_fields = ('applier__name', 'applier__survey__title')
    list_filter = ('applier', )
    
    list_select_related = [
        'applier',
        'applier__survey'
    ]

    def get_applier(self, obj):
        applier = obj.applier.name
        return applier
    get_applier.short_description = _("applier")
    
    def get_apply_date(self, obj):
        apply_date = obj.applier.apply_date
        return apply_date
    get_apply_date.short_description = _("apply_date")
    