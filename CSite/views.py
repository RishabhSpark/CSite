import json

import pandas as pd
from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Courses
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import pyrebase
x="Login/Register"
d = dict()
for i in range(1, 6):
    d['I' + str(i + 1)] = ''
    d['T' + str(i + 1)] = ''
    d['U' + str(i + 1)] = ''
    d['D' + str(i + 1)] = ''

config={
  "apiKey": "AIzaSyBogsww2UQLHaGZ1_4kDJCduj4nN1Pcx2o",
  "authDomain": "fir-tutorial-19f11.firebaseapp.com",
  "projectId": "fir-tutorial-19f11",
  "storageBucket": "fir-tutorial-19f11.appspot.com",
  "messagingSenderId": "615848795705",
  "appId": "1:615848795705:web:6f8a187f0d432c4333f7e8",
  "measurementId": "G-6DJF6MXXHX",
"databaseURL":"https://fir-tutorial-19f11-default-rtdb.firebaseio.com/",
}
df=pd.read_excel('C:\\Users\\Lenovo\\PycharmProjects\\djangoProject\\CSite\\templates\\Book1.xlsx')
firebase=pyrebase.initialize_app(config)
db=firebase.database()
# data={"user":{"email":"","username":"","Ongoing":"","Completed":""}}
authe=firebase.auth()
# def signIn(request):
#     return render()
def login_firebase(request):
    return render(request,"login_firebase.html")
@csrf_exempt
def firebase_login_save(request):
    username=request.POST.get("username")
    email = request.POST.get("email")
    provider = request.POST.get("provider")
    token = request.POST.get("token")
    print(username,email,provider,token)
    return HttpResponse("OK")
def home(request):
    return render(request,"home.html",{"x":x})
def login(request):
    return render(request,"login.html")
def login_firebase(request):
    return render(request,"login_firebase.html")
def postsign(request):
    global x
    email=request.POST.get('email')
    passw=request.POST.get('pass')
    try:
        user=authe.sign_in_with_email_and_password(email,passw)
    except:
        message="Invalid credentials"
        return render(request,"login.html",{"msg":message})
    print(user['localId'])
    session_id=user['localId']
    request.session['uid']=str(session_id)
    users = dict(db.child("users").get().val())
    x=users[session_id]['details']['name']
    return render(request,"home.html",{"x":x})
def logout(request):
    auth.logout(request)
    return request(request,'home.html',{'x':x})
def postreg(request):
    name=request.POST.get('n1')+" "+request.POST.get('n2')
    email=request.POST.get('email1')
    passw=request.POST.get("pass1")
    conf=request.POST.get("pass2")
    if(conf!=passw):
        message="Passwords are not the same"
        return render(request,"login.html",{"msg":message})
    try:
        user=authe.create_user_with_email_and_password(email,passw)
    except:
        message="This email already exists"
        return render(request,"login.html",{"msg":message})
    uid=user['localId']
    data={"name":name,"courses":0}
    db.child('users').child(uid).child("details").set(data)
    return render(request,"login.html")
def discover(request):
    global d
    return discover1(request)
def discover1(request,lang="Python"):
    global df,d,x
    m = df.loc[df['Language'] ==lang]
    d['x'] = x
    for i in range(len(m)):
        if(pd.isna(m.iloc[i]['ImageURL'])):
            d['I' + str(i + 1)] = 'https://media.gcflearnfree.org/content/5e31ca08bc7eff08e4063776_01_29_2020/ProgrammingIllustration.png'
        else:
            d['I'+str(i+1)]=m.iloc[i]['ImageURL']
        d['T' + str(i + 1)] = m.iloc[i]['Title']
        d['U' + str(i + 1)] = m.iloc[i]['CourseURL']
        d['V'+str(i+1)]='visible'
        if(len(m.iloc[i]['Description'])>400):
            d['D' + str(i + 1)] = m.iloc[i]['Description'][:400]+'...'
        else:
            d['D' + str(i + 1)] = m.iloc[i]['Description']
        print(m.iloc[i]['ImageURL'])
    for i in range(len(m),6):
        d['I' + str(i + 1)] = ''
        d['T' + str(i + 1)] = ''
        d['U' + str(i + 1)] = ''
        d['D' + str(i + 1)] = ''
        d['V' + str(i + 1)] = 'hidden'
    return render(request,"discover.html",d)
def about_us(request):
    return render(request,"about us.html",{'x':x})