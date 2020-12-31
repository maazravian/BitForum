from django.shortcuts import render,redirect
from posts.models import *
from django.shortcuts import get_object_or_404


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
            return redirect(login_signup_page)


def home(request):

    if 'email' in request.session:
        user = User.objects.get(email=request.session['email'])

        followers_count = FollowersFollowings.objects.filter(followingId=user.id)
        following_count = FollowersFollowings.objects.filter(followerId=user.id)

        allUser = User.objects.all()
        people_you_may_know = []


        for u in allUser:
            if u.email == request.session['email']:
                continue
            else:
                people_you_may_know.append(u)


        people_you_may_know=people_you_may_know[0:4]
        print(people_you_may_know)

        topics = Topic.objects.all()
        topics=topics[0:4]
        print(topics)


        return render(request,'news-feed.html',{'user':user,'followers_count':len(followers_count),'following_count':len(following_count),'people':people_you_may_know,'suggested_topics':topics})
    else:
        return redirect(login_signup_page)


def logout(request):
    del request.session['email']
    return redirect(login_signup_page)