from django.shortcuts import render

# Create your views here.

def view_post(request,id):
    return render(request,'forum-post-view.html')
