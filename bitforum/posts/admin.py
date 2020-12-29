from django.contrib import admin

# Register your models here.

from .models import User,Post,Contains,Topic,Upvote

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Contains)
admin.site.register(Topic)
admin.site.register(Upvote)