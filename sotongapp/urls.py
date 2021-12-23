from django.urls import path
from django.urls.conf import include
from rest_framework import routers
from sotongapp.apis import AllUserCount, GetOrganName,\
    GetVisitorView, InfoViewSet, SaveTempDataApi, makeSampleData

app_name = 'sotongapp'

router = routers.DefaultRouter()
router.register(r'info', InfoViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('save/', SaveTempDataApi.as_view()),
    path('usercnt/', AllUserCount),
    path('organ/<str:urlname>', GetOrganName),
    path('visitor/<str:urlname>', GetVisitorView.as_view()),
    path('sampledata/<str:pw>', makeSampleData.as_view()),

]
