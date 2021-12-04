from django.urls import path

from logapp.apis import getLogApi, getLogTextApi

urlpatterns = [
    path('getlog', getLogApi.as_view()),
    path('showlog', getLogTextApi.as_view()),
    
]
