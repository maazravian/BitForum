from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Contains)
admin.site.register(Topic)
admin.site.register(Upvote)
admin.site.register(FollowersFollowings)
admin.site.register(Downvote)
admin.site.register(TopicFollower)
admin.site.register(Comment)