
from django.urls import path, include

from reservations.apis import ReserveApi, ReserveCreateApi


#start ~/reservations 


urlpatterns = [
    path('', ReserveCreateApi.as_view(), name="reservation"),
    path('<str:date>', ReserveApi.as_view(), name="reservation"),
    
]
