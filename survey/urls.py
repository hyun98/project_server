from django.urls import path, include

from survey.apis import *

app_name = "survey"

applier_urlpatterns = [
    path('applierfavor/<int:applier_id>', ApplierFavorApi.as_view()),
    path('applier/<int:applier_id>', ApplierDetailApi.as_view()),
    path('applier', ApplierListApi.as_view()),
]

urlpatterns = [
    path('', SurveyListApi.as_view()),
    path('<int:survey_id>', SurveyDetailApi.as_view()),
    path('<int:survey_id>/', include(applier_urlpatterns)),
]
