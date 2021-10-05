from django.urls import path, include


v1_patterns = [
    path('auth/', include('auth.urls')),
    path('users/', include('users.urls')),
    path('board/', include('boards.urls')),
    path('activity/', include('activity.urls')),
    path('FAQs/', include('FAQs.urls')),
    path('reservations/', include('reservations.urls')),
    
]

sotonggori = [
    path('', include('sotongapp.urls')),
]

urlpatterns = [
    path('v1/', include(v1_patterns)),
    path('sotong/', include(sotonggori)),
    
    path('', include('swagger.urls')),
    path('summernote/', include('django_summernote.urls')),
]
