from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(newPost)
admin.site.register(likePost)
admin.site.register(UserFollowing)