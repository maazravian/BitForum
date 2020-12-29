from django.shortcuts import render,redirect
from posts.models import User
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
            return redirect(profileTest)
        else:
            return redirect(login_signup_page)



