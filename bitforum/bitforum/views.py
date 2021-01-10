from django.shortcuts import render,redirect
from posts.models import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.db import models


def viewProfile(request,uid):
    user = User.objects.get(email=request.session['email'])
    following_count = FollowersFollowings.objects.filter(followerId=user.id)
    followers_count = FollowersFollowings.objects.filter(followingId=user.id)
    followed_topics = TopicFollower.objects.filter(followerId=user.id)
    userprofile=User.objects.get(id=uid)
    myPosts = Post.objects.filter(user_id=userprofile)

    postsToShow = []
    for i in myPosts:
        onePost = {}
        onePost['post'] = i
        onePost['upvote'] = len(Upvote.objects.filter(postId=i))
        onePost['downvote'] = len(Downvote.objects.filter(postId=i))
        onePost['comments'] = len(Comment.objects.filter(postId=i))
        topicListOfThatPost = []
        contains = Contains.objects.filter(postId=i)
        for j in contains:
            topicListOfThatPost.append(Topic.objects.get(id=j.topicId.id))
        onePost['topicsList'] = topicListOfThatPost
        postsToShow.append(onePost)



    people_you_may_know = []
    allUser = User.objects.all()
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


    people_you_may_know = people_you_may_know[0:4]

    return render(request,'user-profile.html',{'user': user,'followers_count': len(followers_count),
                   'following_count': len(following_count) + len(followed_topics),'userprofile':userprofile,'userPosts': postsToShow,'people':people_you_may_know})

def myProfile(request):
    user = User.objects.get(email=request.session['email'])
    allUser = User.objects.all()
    following_count = FollowersFollowings.objects.filter(followerId=user.id)
    followers_count = FollowersFollowings.objects.filter(followingId=user.id)
    followed_topics = TopicFollower.objects.filter(followerId=user.id)

    people_you_may_know = []
    alltopics = Topic.objects.all()
    topics = []
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

    myPosts = Post.objects.filter(user_id=user)

    postsToShow = []
    for i in myPosts:
        onePost = {}
        onePost['post'] = i
        onePost['upvote'] = len(Upvote.objects.filter(postId=i))
        onePost['downvote'] = len(Downvote.objects.filter(postId=i))
        onePost['comments'] = len(Comment.objects.filter(postId=i))
        topicListOfThatPost = []
        contains = Contains.objects.filter(postId=i)
        for j in contains:
            topicListOfThatPost.append(Topic.objects.get(id=j.topicId.id))
        onePost['topicsList'] = topicListOfThatPost
        postsToShow.append(onePost)

    topics_with_follower_count = []

    for topic in topics:
        topics_with_follower_count.append(
            {'t': topic.topic_name, 'count': str(len(TopicFollower.objects.filter(topicId=topic.id))) + " Followers"})

    people_you_may_know = people_you_may_know[0:4]

    return render(request, 'my-profile-feed.html',
                  {'newsFeedPosts': postsToShow, 'user': user, 'followers_count': len(followers_count),
                   'following_count': len(following_count) + len(followed_topics), 'people': people_you_may_know,
                   'suggested_topics': topics_with_follower_count, 'myfollowers': followers_count,
                   'myfollowing': following_count
                      , 'mytopics': followed_topics})

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


        # postsToShow = []
        # print("###")
        # oneUserPosts = Post.objects.filter(user_id=user)
        # for i in following_count:
        #     oneUserPosts = oneUserPosts | (Post.objects.filter(user_id = i.followingId))
        #
        # postsToShow.append(oneUserPosts)
        # print(postsToShow)
        # postsToShow = postsToShow[0]

        postsToShow = []

        for following in following_count:
            oneUserPosts = Post.objects.filter(user_id = following.followingId)

            for i in oneUserPosts:
                onePost = {}
                onePost['post'] = i
                onePost['upvote'] = len(Upvote.objects.filter(postId=i))
                onePost['downvote'] = len(Downvote.objects.filter(postId=i))
                onePost['comments'] = len(Comment.objects.filter(postId=i))
                topicListOfThatPost = []
                contains   = Contains.objects.filter(postId=i)
                for j in contains:
                    topicListOfThatPost.append(Topic.objects.get(id=j.topicId.id))
                onePost['topicsList'] = topicListOfThatPost
                postsToShow.append(onePost)

        myPosts = Post.objects.filter(user_id=user)
        for i in myPosts:
            onePost = {}
            onePost['post'] = i
            onePost['upvote'] = len(Upvote.objects.filter(postId=i))
            onePost['downvote'] = len(Downvote.objects.filter(postId=i))
            onePost['comments'] = len(Comment.objects.filter(postId=i))
            topicListOfThatPost = []
            contains = Contains.objects.filter(postId=i)
            for j in contains:
                topicListOfThatPost.append(Topic.objects.get(id=j.topicId.id))
            onePost['topicsList'] = topicListOfThatPost
            postsToShow.append(onePost)

        followedTopicList = []
        for topic in followed_topics:
            followedTopicList.append(Topic.objects.get(id=topic.topicId.id))


            # for i in oneTopicPosts:
            #     onePost = {}
            #     onePost['post'] = i
            #     onePost['upvote'] = len(Upvote.objects.filter(postId=i))
            #     onePost['downvote'] = len(Downvote.objects.filter(postId=i))
            #     onePost['comments'] = len(Comment.objects.filter(postId=i))
            #
            #     postsToShow.append(onePost)


        for p in Post.objects.raw("select id from posts_Post where id = (select postId_id from posts_contains where topicId_id = (select topicId_id from posts_topicfollower where followerId_id = %s)) ",[user.id]):
            onePost = {}
            onePost['post'] = p
            onePost['upvote'] = len(Upvote.objects.filter(postId=p))
            onePost['downvote'] = len(Downvote.objects.filter(postId=p))
            onePost['comments'] = len(Comment.objects.filter(postId=p))
            topicListOfThatPost = []
            contains = Contains.objects.filter(postId=p)
            for j in contains:
                topicListOfThatPost.append(Topic.objects.get(id=j.topicId.id))
            onePost['topicsList'] = topicListOfThatPost
            postsToShow.append(onePost)

        newList = {x['post']: x for x in postsToShow}.values()
        postsToShow = newList


        #postsToShow = postsToShow[0:10]

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

def deleteFollowing(request):
    # FollowersFollowings.objects.filter(id=fid).delete()
    # return redirect(home)
    if request.method == 'POST':
        id = request.POST.get('slug', None)
        FollowersFollowings.objects.filter(id=id).delete()
    ctx = {'message': 'Unfollowed User'}
    return HttpResponse(json.dumps(ctx), content_type='application/json')

def unfollowTopic(request):
    if request.method == 'POST':
        id = request.POST.get('slug', None)
        TopicFollower.objects.filter(id=id).delete()
    ctx = {'message': 'Unfollowed Topic'}
    return HttpResponse(json.dumps(ctx), content_type='application/json')

def removeFollower(request):
    if request.method == 'POST':
        id = request.POST.get('slug', None)
        FollowersFollowings.objects.filter(id=id).delete()
    ctx = {'message': 'removed Follower'}
    return HttpResponse(json.dumps(ctx), content_type='application/json')

def viewPost(request,pid):
    post = Post.objects.get(id=pid)
    post.no_of_views +=1
    post.save()
    user = User.objects.get(email=request.session['email'])
    commentsList = Comment.objects.filter(postId=pid)

    topicsList = Contains.objects.filter(postId=pid)
    print(topicsList)
    upvotesList = Upvote.objects.filter(postId=pid)
    downvotesList = Downvote.objects.filter(postId=pid)
    currentUser = User.objects.get(email=request.session['email'])

    checkUpvote = False
    checkDownvote = False

    try:
        x = Upvote.objects.get(postId=pid,userId=user)
        checkUpvote = True
    except Upvote.DoesNotExist:
        checkUpvote = False
    try:
        x = Downvote.objects.get(postId=pid,userId=user)
        checkDownvote = True
    except Downvote.DoesNotExist:
         checkDownvote = False


    return render(request,'post-view.html',{'currentUser':currentUser,'post':post,'topics':topicsList,'upvotesList':upvotesList,'upCount':len(upvotesList),'downvotesList':downvotesList,'downCount':len(downvotesList),'commentCount':len(commentsList),'comments':commentsList,'checkUp':checkUpvote,'checkDown':checkDownvote})

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


def doUpvote(request):
    if request.method == 'POST':
        postId = request.POST.get('slug', None)
        user = User.objects.get(email=request.session['email'])
        try:
            x = Upvote.objects.get(postId=postId,userId=user.id)
            ctx = {'message':1}
            # delete upvote
            x.delete()
        except Upvote.DoesNotExist:
        # Do Something
            ctx = {'message':0}
            # do upvote
            p = Post.objects.get(id=postId)
            Upvote(postId=p,userId=user).save()
        return HttpResponse(json.dumps(ctx), content_type='application/json')

def doDownvote(request):
    if request.method == 'POST':
        postId = request.POST.get('slug', None)
        user = User.objects.get(email=request.session['email'])
        try:
            x = Downvote.objects.get(postId=postId,userId=user.id)
            ctx = {'message':1}
            # delete upvote
            x.delete()
        except Downvote.DoesNotExist:
        # Do Something
            ctx = {'message':0}
            # do upvote
            p = Post.objects.get(id=postId)
            Downvote(postId=p,userId=user).save()
        return HttpResponse(json.dumps(ctx), content_type='application/json')