from django.urls import path, include


v1_patterns = [
    path('auth/', include(('auth.urls', 'auth'))),
    path('users/', include(('users.urls', 'users'))),
    path('board/', include(('boards.urls', 'boards'))),
    path('activity/', include(('activity.urls', 'activity'))),
    path('FAQs/', include(('FAQs.urls', 'FAQs'))),
    path('reservations/', include(('reservations.urls', 'reservations'))),
    
]

sotonggori = [
    path('', include(('sotongapp.urls', 'sotongapp'))),
]

urlpatterns = [
    path('v1/', include((v1_patterns, 'v1'))),
    path('sotong/', include(sotonggori, 'sotong')),
    
    path('', include('swagger.urls')),
    path('summernote/', include('django_summernote.urls')),
]
