from django.contrib import admin

from django.utils.translation import gettext_lazy as _

from FAQs.models import Question, Answer

# admin.site.register(Question)
# admin.site.register(Answer)

class AnswerInline(admin.StackedInline):
    model = Answer
    can_delete = False
    verbose_name_plural = 'answer'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    ordering = ('order', )
    list_display = (
        'question', 'get_answer',
    )
    list_display_links = (
        'question', 'get_answer',
    )
    search_fields = ('question', )
    inlines = (AnswerInline, )

    def get_answer(self, obj):
        answer = obj.answer
        return answer
    get_answer.short_description = _("answer")
