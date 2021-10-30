import json


from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import pyrebase
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
    return render(request,"home.html",{"x":"Login/Register"})
def login(request):
    return render(request,"login.html")
def login_firebase(request):
    return render(request,"login_firebase.html")
def postsign(request):
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
    return render(request,"home.html",{"x":users[session_id]['details']['name']})
def logout(request):
    auth.logout(request)
    return request(request,'home.html',{'x':"Login/Register"})
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