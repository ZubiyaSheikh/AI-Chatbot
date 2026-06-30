from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # Chat API
    path("chat/", views.chat, name="chat"),
    path("new-chat/", views.new_chat, name="new_chat"),
]