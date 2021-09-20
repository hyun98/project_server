from django.urls import path

from activity.apis import ActivityReadApi, ActivityDetailApi, ActivityDetailImageApi, ActivityFilesApi

# startwith : activity/
urlpatterns = [
    path('', ActivityReadApi.as_view()),
    path('<int:id>/', ActivityDetailApi.as_view()),
    path('detail/<int:detail_id>/', ActivityDetailImageApi.as_view()),
    path('file/<int:detail_id>', ActivityFilesApi.as_view()),
    
]
