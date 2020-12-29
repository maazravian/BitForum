from django.shortcuts import render

def profileTest(request):
    return render(request,'my-profile-feed.html')

def loginTest(request):
    return render(request,'sign-in.html')

def userTest(request):
    return render(request,'user-profile.html')

