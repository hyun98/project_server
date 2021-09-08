from django.urls import path

from activity.apis import ActivityReadApi, ActivityDetailApi, ActivityDetailImageApi


urlpatterns = [
    path('', ActivityReadApi.as_view()),
    path('<int:id>/', ActivityDetailApi.as_view()),
    path('detail/<int:detail_id>/', ActivityDetailImageApi.as_view()),
    
]
