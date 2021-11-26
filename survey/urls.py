from django.urls import path, include

from rest_framework.routers import DefaultRouter

from survey.apis import *

app_name = "survey"


router = DefaultRouter()
router.register("", SurveyApi)

urlpatterns = [
    path('',include(router.urls)),
]
