from django.urls import path
from . import views

urlpatterns = [
    path("chat_api/", views.business_assistant, name="business_assistant"),
    path('get_conversation/',views.get_conversation, name='get_conversation'),
    
]
