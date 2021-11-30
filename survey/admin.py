from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from survey.models import *

admin.site.register(Question)
admin.site.register(SubQuestion)
admin.site.register(ApplyFile)
admin.site.register(Applier)
admin.site.register(Answer)

class QuestionInline(admin.StackedInline):
    model = Question
    can_delete = True
    verbose_name_plural = "question"
    
class SubQuestionInline(admin.StackedInline):
    model = SubQuestion
    can_delete = True
    verbose_name_plural = "subquestion"
    
    
@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    ordering = ('-created_date', )
    list_display = (
        'title', 'description', 'start_date', 'due_date',
        'created_date', 'get_creator'
    )
    list_display_links = (
        'title', 'description', 'start_date', 'due_date',
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