from django.urls import path, include

from survey.apis import *

app_name = "survey"

applier_urlpatterns = [
    path('applier', ApplyApi.as_view()),
    path('applier/<int:applier_id>', ApplierDetailApi.as_view()),
    path('applierfavor/<int:applier_id>', ApplierFavorApi.as_view()),
    
    path('appliercsv', ApplierCSVApi.as_view()),
    path('applierfile/<int:file_id>', ApplierFileDownloadApi.as_view()),
    path('applierselfcheck', ApplierSelfCheckApi.as_view()),
    
]

urlpatterns = [
    
    path('', SurveyApi.as_view()),
    path('file', filetest.as_view()),
    path('<int:survey_id>', SurveyDetailApi.as_view()),
    path('<int:survey_id>/', include(applier_urlpatterns)),
]
