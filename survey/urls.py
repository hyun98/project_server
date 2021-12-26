from django.urls import path, include

from survey.apis import (
    SurveyApi,
    SurveyDetailApi,
    ApplyApi,
    ApplierListApi,
    ApplierDetailApi,
    ApplierFavorApi,
    ApplierCSVApi,
    ApplierFileDownloadApi,
    ApplierSelfCheckApi,
    ApplierDuplicateCheck,
)
from survey.views import *

app_name = "survey"

applier_urlpatterns = [
    path('applier', ApplyApi.as_view(), name='apply'),
    path('applierlist', ApplierListApi.as_view(), name='applierlist'),
    path('applier/<int:applier_id>', ApplierDetailApi.as_view(), name='applier'),
    path('applierfavor/<int:applier_id>', ApplierFavorApi.as_view(), name='applierfavor'),
    
    path('appliercsv', ApplierCSVApi.as_view(), name='appliercsv'),
    path('applierfile/<int:file_id>', ApplierFileDownloadApi.as_view(), name='applierfile'),
    path('applierselfcheck', ApplierSelfCheckApi.as_view(), name='applierselfcheck'),
    path('duplicate', ApplierDuplicateCheck.as_view(), name="check_duplicate"),
    
]

urlpatterns = [
    path('', SurveyApi.as_view(), name='survey'),
    path('<int:survey_id>', SurveyDetailApi.as_view(), name='surveydetail'),
    path('<int:survey_id>/', include(applier_urlpatterns)),
    
    
    path('applierlist', ApplierListView.as_view(), name="applierlist"),
    path('applierdetail/<int:pk>', ApplierDetail, name="applierdetail")
]
