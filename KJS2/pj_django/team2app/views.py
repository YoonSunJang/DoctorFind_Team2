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

from .models import Member
# def signup(request):
#     return render(request,'signup.html')
def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        pw = request.POST['pw']
        address = request.POST['address']
        print("이름:", name, "아이디(email):", email, "전화번호", phone, "비번", pw, "주소", address)
        
        member = Member(
            name=name,
            email=email,
            phone=phone,
            pw=pw,
            address=address
        )
        member.save()
        return HttpResponseRedirect('../login')
    else:
        return render(request,'signup.html')
    
def update(request,id):
    template = loader.get_template('update.html')
    member = Member.objects.get(id=id)
    context = {
        'id':id,
    }
    return HttpResponse(template.render(context,request))


def update_ok(request,id):
    new_name = request.POST['name']
    new_phone = request.POST['phone']
    new_pw = request.POST['pw']
    new_address = request.POST['address']
    member = Member.objects.get(id=id)
    member.name = new_name
    member.phone = new_phone
    member.pw = new_pw
    member.address = new_address
    member.save()
    return HttpResponseRedirect(reverse('../mypage/'))
    print("이름:", name, "아이디(email):", email, "전화번호", phone, "비번", pw, "주소", address)
    
    
def healthinfo(request):
    return render(request,'healthinfo.html')

def event(request):
    return render(request,'event.html')

def mypage(request):
    return render(request,'mypage.html')
