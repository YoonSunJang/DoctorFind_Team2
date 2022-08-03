from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

def index(request):
    return render(request,'index.html')

def search(request):
    return render(request,'search.html')

def review(request):
    return render(request,'review.html')

def map(request):
    return render(request,'map.html')

def login(request):
    return render(request,'login.html')

