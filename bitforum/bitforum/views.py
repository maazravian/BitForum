from django.shortcuts import render,redirect
from posts.models import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.db import models


def viewProfile(request,uid):
    return render(request,'user-profile.html')

def profileTest(request):
    user = User.objects.all()
    dict = {'name':user[0].name,'profile_pic':user[0].profile_pic}
    return render(request,'my-profile-feed.html', {'user':dict})

def login_signup_page(request):
    return render(request,'sign-in.html')

def checkLogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(email = email,password=password)
        if user.exists():
            request.session['email'] = email
            return redirect(home)
        else:
            return render(request,'sign-in.html',{'ucheck':'error'})

# def checkLoginAjax(request):
#
#     u = request.POST.get('email',None)
#     print(u)
#
#     return JsonResponse({'error':'error'})

def home(request):
    from django.conf import settings
    print(settings.MEDIA_URL)
    if 'email' in request.session:
        user = User.objects.get(email=request.session['email'])

        followers_count = FollowersFollowings.objects.filter(followingId=user.id)
        following_count = FollowersFollowings.objects.filter(followerId=user.id)

        followed_topics = TopicFollower.objects.filter(followerId=user.id)

        print(followed_topics)
        allUser = User.objects.all()

        people_you_may_know = []
        topics = []

        alltopics = Topic.objects.all()

        for t in alltopics:
            found = False
            for temp in followed_topics:
                if temp.topicId.topic_name == t.topic_name:
                    found = True
                    break
            if found:
                continue
            else:
                topics.append(t)



        for u in allUser:
            found = False
            if u.email == user.email:
                continue
            for temp in following_count:
                if temp.followingId.email == u.email:
                    found = True
                    break
            if found:
                continue
            else:
                people_you_may_know.append(u)



        people_you_may_know=people_you_may_know[0:4]
        # print(people_you_may_know)


        postsToShow = []
        print("###")
        oneUserPosts = Post.objects.filter(user_id=user)
        for i in following_count:
            oneUserPosts = oneUserPosts | (Post.objects.filter(user_id = i.followingId))

        postsToShow.append(oneUserPosts)
        print(postsToShow)
        postsToShow = postsToShow[0]


        topics = topics[0:4]
        topics_with_follower_count = []

        for topic in topics:
            topics_with_follower_count.append({'t':topic.topic_name,'count':str(len(TopicFollower.objects.filter(topicId=topic.id)))+" Followers"})


        return render(request,'news-feed.html',{'newsFeedPosts':postsToShow,'user':user,'followers_count':len(followers_count),'following_count':len(following_count)+len(followed_topics),'people':people_you_may_know,'suggested_topics':topics_with_follower_count,'myfollowers':followers_count,'myfollowing':following_count
                                                ,'mytopics':followed_topics})
    else:
        return redirect(login_signup_page)


def logout(request):
    del request.session['email']
    return redirect(login_signup_page)

def deleteFollowing(request,fid):
    FollowersFollowings.objects.filter(id=fid).delete()
    return redirect(home)

def unfollowTopic(request,tid):
    TopicFollower.objects.filter(id=tid).delete()
    return redirect(home)

def removeFollower(request,fid):
    FollowersFollowings.objects.filter(id=fid).delete()
    return redirect(home)

def viewPost(request,pid):
    post = Post.objects.get(id=pid)
    post.no_of_views +=1
    post.save()
    commentsList = Comment.objects.filter(postId=pid)

    topicsList = Contains.objects.filter(postId=pid)
    print(topicsList)
    upvotesList = Upvote.objects.filter(postId=pid)
    downvotesList = Downvote.objects.filter(postId=pid)
    currentUser = User.objects.get(email=request.session['email'])

    return render(request,'post-view.html',{'currentUser':currentUser,'post':post,'topics':topicsList,'upvotesList':upvotesList,'upCount':len(upvotesList),'downvotesList':downvotesList,'downCount':len(downvotesList),'commentCount':len(commentsList),'comments':commentsList})

def signup(request):
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repeatPassword = request.POST['repeat-password']
        profilePic = request.FILES['profile_pic']
        print(profilePic)
        user = User.objects.filter(email = email)

        if user.exists():
            print(profilePic)
            return redirect(login_signup_page)
        else:
            # profilePic = profilePic.replace(' ','%20')
            usr = User(name=username, email=email, password=password,profile_pic=profilePic)
            usr.save()
            request.session['email'] = email
            return redirect(home)

