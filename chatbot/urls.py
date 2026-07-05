from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # Chat API
    path("chat/", views.chat, name="chat"),
    path("new-chat/", views.new_chat, name="new_chat"),
    path("chat/<int:chat_id>/", views.open_chat, name="open_chat"),
    path(
    "bookmark/",views.toggle_bookmark, name="toggle_bookmark"),
    path("bookmarks/", views.bookmarks, name="bookmarks"),
    path("logout/", views.logout_view, name="logout"),
]