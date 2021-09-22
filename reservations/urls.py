
from django.urls import path, include

from reservations.apis import ReserveApi


#start ~/reservations 


urlpatterns = [
    path('<str:date>', ReserveApi.as_view(), name="reservation"),
    
]
