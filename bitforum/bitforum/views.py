from django.contrib.auth import authenticate
from django.shortcuts import render,redirect
from posts.models import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.db import models
from django.db.models import Q


def viewProfile(request,uid):
    if 'email' not in request.session:
        return redirect(login_signup_page)
    user = User.objects.get(email=request.session['email'])

    checkFollowingFlag = False
    checkFollowing = FollowersFollowings.objects.filter(followerId=user,followingId=User.objects.get(id=uid))
    if checkFollowing.exists():
        checkFollowingFlag = True


    if user.id == uid:
        return redirect(myProfile)

    userprofile = User.objects.get(id=uid)

    following_count = FollowersFollowings.objects.filter(followerId=userprofile.id)
    followers_count = FollowersFollowings.objects.filter(followingId=userprofile.id)
    followed_topics_2 = TopicFollower.objects.filter(followerId=userprofile.id)
    following_count_2 = FollowersFollowings.objects.filter(followerId=user.id)
    followers_count_2 = FollowersFollowings.objects.filter(followingId=user.id)
    followed_topics = TopicFollower.objects.filter(followerId=user.id)

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
        for temp in following_count_2:
            if temp.followingId.email == u.email:
                found = True
                break
        if found:
            continue
        else:
            people_you_may_know.append(u)


    people_you_may_know = people_you_may_know[0:4]

    postsToShow = postsToShow[::-1]


    for p in postsToShow:
        try:
            x = Upvote.objects.get(postId=p['post'].id, userId=user)
            p['checkUp'] = True
        except Upvote.DoesNotExist:
            p['checkUp'] = False
        try:
            x = Downvote.objects.get(postId=p['post'].id, userId=user)
            p['checkDown'] = True
        except Downvote.DoesNotExist:
            p['checkDown'] = False



    return render(request,'user-profile.html',{'user': user,'followers_count': len(followers_count),
                   'following_count': len(following_count) + len(followed_topics_2),'userprofile':userprofile,'userPosts': postsToShow,'people':people_you_may_know,'check_following_flag':checkFollowingFlag})

def myProfile(request):
    if 'email' not in request.session:
        return redirect(login_signup_page)
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

    postsToShow = postsToShow[::-1]

    for p in postsToShow:
        try:
            x = Upvote.objects.get(postId=p['post'].id, userId=user)
            p['checkUp'] = True
        except Upvote.DoesNotExist:
            p['checkUp'] = False
        try:
            x = Downvote.objects.get(postId=p['post'].id, userId=user)
            p['checkDown'] = True
        except Downvote.DoesNotExist:
            p['checkDown'] = False


    return render(request, 'my-profile-feed.html',
                  {'newsFeedPosts': postsToShow, 'user': user, 'followers_count': len(followers_count),
                   'following_count': len(following_count) + len(followed_topics), 'people': people_you_may_know,
                   'suggested_topics': topics_with_follower_count, 'myfollowers': followers_count,
                   'myfollowing': following_count
                      , 'mytopics': followed_topics})

def login_signup_page(request):
    return render(request,'sign-in.html')


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
        postsToShow = list(newList)


        postsToShow = sorted(postsToShow, key=lambda k: k['post'].date_time)
        postsToShow = postsToShow[::-1]

        for p in postsToShow:
            try:
                x = Upvote.objects.get(postId=p['post'].id, userId=user)
                p['checkUp'] = True
            except Upvote.DoesNotExist:
                p['checkUp'] = False
            try:
                x = Downvote.objects.get(postId=p['post'].id, userId=user)
                p['checkDown'] = True
            except Downvote.DoesNotExist:
                p['checkDown'] = False



        #postsToShow = postsToShow[0:10]

        topics = topics[0:4]
        topics_with_follower_count = []

        for topic in topics:
            topics_with_follower_count.append({'t':topic,'count':str(len(TopicFollower.objects.filter(topicId=topic.id)))+" Followers"})


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
    if 'email' not in request.session:
        return redirect(login_signup_page)
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

    image = PostImage.objects.filter(postId=pid)
    print(image)
    if image.exists():
        image = image[0]
        return render(request, 'post-view.html',
                      {'currentUser': currentUser, 'post': post, 'topics': topicsList, 'upvotesList': upvotesList,
                       'upCount': len(upvotesList), 'downvotesList': downvotesList, 'downCount': len(downvotesList),
                       'commentCount': len(commentsList), 'comments': commentsList, 'checkUp': checkUpvote,
                       'checkDown': checkDownvote,'PostImage':image})
    else:
        return render(request,'post-view.html',{'currentUser':currentUser,'post':post,'topics':topicsList,'upvotesList':upvotesList,'upCount':len(upvotesList),'downvotesList':downvotesList,'downCount':len(downvotesList),'commentCount':len(commentsList),'comments':commentsList,'checkUp':checkUpvote,'checkDown':checkDownvote,'PostImage':False})


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
            # for notification
            recieving_user = User.objects.get(id=User.objects.get(email=Post.objects.get(id=postId).user_id).id)
            sending_user = user
            type = "UP"
            Notification(reciever_id=recieving_user, sender_id=sending_user, postId=Post.objects.get(id=postId),
            type=type).save()
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

            # for notification
            recieving_user = User.objects.get(id=User.objects.get(email=Post.objects.get(id=postId).user_id).id)
            sending_user = user
            type = "DOWN"
            Notification(reciever_id=recieving_user, sender_id=sending_user, postId=Post.objects.get(id=postId),
            type=type).save()
        return HttpResponse(json.dumps(ctx), content_type='application/json')


def checkLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        # email = request.POST['email']
        # password = request.POST['password']

        user = User.objects.filter(email=email, password=password)
        if user.exists():
            request.session['email'] = email
            ctx = {'message': 1}

        else:
            ctx = {'message': 0}

        return HttpResponse(json.dumps(ctx))

def signup(request):
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repeatPassword = request.POST['repeat-password']
        profilePic = request.FILES['profile_pic']
        print(profilePic)
        user = User.objects.filter(email=email)

        if user.exists():
            return render(request,'sign-in.html',{'check':1})
        else:

            usr = User(name=username, email=email, password=password,profile_pic=profilePic)
            usr.save()
            request.session['email'] = email

            return redirect(home)
def followajax(request):
    if request.method == 'POST':
        followid = request.POST.get('slug', None)
        print(followid)
        user = User.objects.get(email=request.session['email'])

        temp=FollowersFollowings.objects.filter(followerId=user,followingId=User.objects.get(id=followid))
        if temp.exists():
            temp.delete()
            ctx={'message':0}
        else:
            usr = FollowersFollowings(followerId=user,followingId =User.objects.get(id=followid))
            usr.save()
            ctx = {'message': 1}
            # for notification
            recieving_user = User.objects.get(id=followid)
            sending_user = user
            type = "FOLLOW"
            Notification(reciever_id=recieving_user, sender_id=sending_user,
                         type=type).save()



        return HttpResponse(json.dumps(ctx), content_type='application/json')



def followTopicAjax(request):
    if request.method == 'POST':
        topicId = request.POST.get('slug', None)
        print(topicId)
        user = User.objects.get(email=request.session['email'])
        topic = Topic.objects.get(id=topicId)
        temp = TopicFollower.objects.filter(topicId=topic,followerId=user)
        if temp.exists():
            temp.delete()
            ctx = {'message': 0}
        else:
            usr = TopicFollower(topicId=topic, followerId=user)
            usr.save()
            ctx = {'message': 1}

        return HttpResponse(json.dumps(ctx), content_type='application/json')

def unfollowUserBtnAjax(request):
    if request.method == 'POST':
        userId = request.POST.get('slug', None)

        suser = User.objects.get(email=request.session['email'])

        FollowersFollowings.objects.get(followerId=suser,followingId=User.objects.get(id=userId)).delete()
        ctx = {'message':1}

        return HttpResponse(json.dumps(ctx), content_type='application/json')

def followUserBtnAjax(request):
    if request.method == 'POST':
        userId = request.POST.get('slug', None)

        suser = User.objects.get(email=request.session['email'])

        FollowersFollowings(followerId=suser, followingId=User.objects.get(id=userId)).save()
        ctx = {'message': 1}

        # for notification
        recieving_user = User.objects.get(id=userId)
        sending_user = suser
        type = "FOLLOW"
        Notification(reciever_id=recieving_user, sender_id=sending_user,
        type=type).save()

        return HttpResponse(json.dumps(ctx), content_type='application/json')


def postComment(request,pid):
    if request.method == 'POST':
        post = Post.objects.get(id=pid)
        text = request.POST['comment']


        user = User.objects.get(email=request.session['email'])

        Comment(userId=user,postId=post,content=text).save()

        commentsList = Comment.objects.filter(postId=pid)

        topicsList = Contains.objects.filter(postId=pid)
        print(topicsList)
        upvotesList = Upvote.objects.filter(postId=pid)
        downvotesList = Downvote.objects.filter(postId=pid)
        currentUser = User.objects.get(email=request.session['email'])

        checkUpvote = False
        checkDownvote = False

        try:
            x = Upvote.objects.get(postId=pid, userId=user)
            checkUpvote = True
        except Upvote.DoesNotExist:
            checkUpvote = False
        try:
            x = Downvote.objects.get(postId=pid, userId=user)
            checkDownvote = True
        except Downvote.DoesNotExist:
            checkDownvote = False

        #for notification
        recieving_user = User.objects.get(id=User.objects.get(email=Post.objects.get(id=pid).user_id).id)
        sending_user = user
        type="COMMENT"
        Notification(reciever_id=recieving_user,sender_id=sending_user,postId=Post.objects.get(id=pid),type=type).save()

        return render(request,'post-view.html',{'currentUser':currentUser,'post':post,'topics':topicsList,'upvotesList':upvotesList,'upCount':len(upvotesList),'downvotesList':downvotesList,'downCount':len(downvotesList),'commentCount':len(commentsList),'comments':commentsList,'checkUp':checkUpvote,'checkDown':checkDownvote})


def downComment(request):
    if request.method == 'POST':
        commentId = request.POST.get('slug', None)
        c=Comment.objects.get(id=commentId)
        c.no_of_down +=1
        c.save()
        ctx = {'message': 1}
    return HttpResponse(json.dumps(ctx), content_type='application/json')


def upComment(request):
    if request.method == 'POST':
        commentId = request.POST.get('slug', None)
        c=Comment.objects.get(id=commentId)
        c.no_of_up +=1
        c.save()
        ctx= {'message':1}
    return HttpResponse(json.dumps(ctx), content_type='application/json')


def makePost(request):
    if request.method == 'POST':
        user= User.objects.get(email=request.session['email'])
        title = request.POST['title']
        content = request.POST['content']
        topics = request.POST['topics']
        topicsList = topics.split(',')
        p = Post(title=title, content=content, user_id=user)
        p.save()
        for topic in topicsList:
            topic=topic.strip()
            topic=topic.upper()
            if Topic.objects.filter(topic_name=topic).exists():
                Contains(postId=p,topicId=Topic.objects.get(topic_name=topic)).save()
                continue
            else:
                x=Topic(topic_name=topic)
                x.save()
                Contains(postId=p,topicId=x).save()
        try:
            image = request.FILES['image']
            PostImage(image=image, postId=p).save()
        except:
            pass

    return redirect(home)

def fetchNotification(request):
    if request.method == 'GET':
        user = User.objects.get(email=request.session['email'])
        notifications = Notification.objects.filter(reciever_id=user,seen=False).values('sender_id','reciever_id','type','postId')
        if notifications.exists():
            data = Notification.objects.filter(reciever_id=user,seen=False).values('sender_id','reciever_id','type','postId').exclude(sender_id=user)
            querySet=[]
            for i in data:
                i['profile_id'] = i['sender_id']
                i['sender_id'] = User.objects.get(id=i["sender_id"]).name
                i['reciever_id'] = User.objects.get(id=i["reciever_id"]).name

                querySet.append(i)

            ctx = {'message':1,'data':querySet}
        else:
            ctx = {'message':0}



    return HttpResponse(json.dumps(ctx), content_type='application/json')

def mark_all_as_read(request):
    if request.method == "GET":
        notifications = Notification.objects.filter(reciever_id=User.objects.get(email=request.session["email"]))
        for notification in notifications:
            notification.seen=True
            notification.save()

        ctx={'message':1}
    return HttpResponse(json.dumps(ctx),content_type='application/json')


def deletePost(request):
    if request.method=="POST":
        post_id = request.POST.get('slug', None)
        print(post_id)
        p = Post.objects.filter(id=post_id)
        print(p)
        p.delete()
        ctx = {'message':1}
    return HttpResponse(json.dumps(ctx),content_type='application/json')

def saveEditProfile(request):
    if request.method == 'POST':
        u = User.objects.get(email=request.session['email'])
        try:
            name = request.POST['name']
            u.name = name
        except:
            pass
        try:
            status = request.POST['status']
            u.status = status
        except:
            pass
        try:
            profilePic = request.FILES['profile_pic']
            u.profile_pic = profilePic
        except:
            pass

        u.save()

        return redirect(myProfile)
def search(request):
    user = User.objects.get(email=request.session['email'])
    if request.method == 'POST':
        search = request.POST['search']
        searchUser = User.objects.filter(Q(name__contains=search)|Q(status__contains=search)|Q(email__contains=search))
        searchPosts = Post.objects.filter(
            Q(title__contains=search) | Q(content__contains=search))

        print(searchUser)
        print(searchPosts)
        if searchUser or searchPosts:
            return render(request, 'search-page.html', {'currentUser': user, 'userSearched': searchUser,'postsSearched':searchPosts})
        else:
            return render(request, 'search-page.html', {'currentUser': user})


