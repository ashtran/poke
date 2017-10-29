from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from .models import *
from django.contrib.messages import error
from django.contrib import messages

#<--- Homepage --->#
def index(request):
    return render(request, 'poke_app/index.html')
#<--- Process Create New User --->#
def createuser(request):
    errors= User.objects.validate_registration(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            error(request, message, extra_tags=field)
        return redirect('/')
    else:
        user= User.objects.create_user(request.POST)
        request.session['user_id']=user.id
        return redirect('/dashboard')
#<--- Process User Login --->#
def login(request):
    errors= User.objects.validate_login(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            error(request, message, extra_tags=field)
        return redirect('/')
    else:
        user= User.objects.filter(username=request.POST['username'])[0]
        request.session['user_id']=user.id
        return redirect('/dashboard')

#<--- User Dashboard --->#
def dashboard(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    user_id=request.session['user_id']
    friend=User.objects.exclude(id=request.session['user_id'])
    context={
        'user':User.objects.get(id=user_id),
        'summary':User.objects.exclude(id=request.session['user_id']),
        'others':friend,
        'pokes':Poke.objects.filter(user_id=friend.values('id')).count(),
    }
    return render(request, 'poke_app/pokes.html', context)

#<--- Process poke Plan --->#
def poke(request,friend_id):
    poke= Poke.objects.count_poke(request.session['user_id'])
    joinpoke= Poke.objects.add_pokes(request.session['user_id'],friend_id)
    return redirect('/dashboard')


#<--- Process Logout --->#
def logout(request):
    del request.session['user_id']
    return redirect('/')
