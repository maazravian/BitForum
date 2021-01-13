"""bitforum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from posts import urls
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('admin',admin.site.urls),
    path('myProfile',myProfile),
    path('login',login_signup_page),
    path('checkLogin',checkLogin,name='checkLogin'),
    path('',home),
    path('logout', logout),
    path('deleteFollowing', deleteFollowing,name='deleteFollowing'),
    path('unfollowTopic', unfollowTopic,name='unfollowTopic'),
    path('removeFollower', removeFollower, name='removeFollower'),
    path('post/<int:pid>', viewPost, name='viewPost'),
    path('signup', signup,name='signup'),
    path('viewProfile/<int:uid>',viewProfile,name='viewProfile'),
    path('doUpvote',doUpvote,name='doUpvote'),
    path('doDownvote',doDownvote,name='doDownvote'),
    path('followAjax',followajax,name='followAjax'),
    path('followTopicAjax',followTopicAjax,name='followTopicAjax'),
    path('unfollowUserBtnAjax',unfollowUserBtnAjax,name='unfollowUserBtnAjax'),
    path('followUserBtnAjax',followUserBtnAjax,name='followUserBtnAjax'),
    path('postComment/<int:pid>',postComment,name='postComment'),
    path('downComment',downComment,name='downComment'),
    path('upComment',upComment,name='upComment'),
    path('makePost',makePost,name='makePost'),
    path('fetchNotification',fetchNotification,name='fetchNotification'),
    path('mark_all_as_read',mark_all_as_read,name='mark_all_as_read'),
    #path('checkLoginAjax',checkLoginAjax,name='checkLoginAjax')
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
