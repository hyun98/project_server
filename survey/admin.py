from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from survey.models import *

admin.site.register(Survey) 
admin.site.register(Question)
admin.site.register(SubQuestion)
admin.site.register(SurveyFile)