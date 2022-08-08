from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse 
from django.shortcuts import render
from django.template import loader

def index(request):
    return render(request,'index.html')

def search(request):
    input1=request.GET.get("input1")
    input2=request.GET.get("input2")
    input3=request.GET.get("input3")
    name=request.GET.get("name")
    print(1)
    if(input1==input2==input3==name==None):pass
    else:
        print(input1)
        print(input2)
        print(input3)
        print(name)
    print(2)
    return render(request,'search.html')

def search_ok(request):
    return HttpResponseRedirect(reverse('search'))

def review(request):
    return render(request,'review.html')

def rwrite(request):
    return render(request,'rwrite.html')

def map(request):
    return render(request,'map.html')

def login(request):
    return render(request,'login.html')

def signup(request):
    return render(request,'signup.html')

def healthinfo(request):
    return render(request,'healthinfo.html')

def event(request):
    return render(request,'event.html')

def mypage(request):
    return render(request,'mypage.html')
