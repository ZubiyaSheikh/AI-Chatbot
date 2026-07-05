from django.contrib import admin

# Register your models here.
from .models import Chat, Message, Bookmark

admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(Bookmark)