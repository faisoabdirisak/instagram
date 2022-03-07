from django.contrib import admin
from .models import Profile
from .models import Photo, Comment

admin.site.register(Profile)
admin.site.register(Photo)
admin.site.register(Comment)