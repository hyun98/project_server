from django.urls import path

from FAQs.apis import FAQslistAPI


urlpatterns = [
    path('', FAQslistAPI.as_view(), name="FAQs_list"),
    
]
