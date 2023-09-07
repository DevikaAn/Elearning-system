from django.core.exceptions import PermissionDenied
from . models import *
import learn.views
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect



def logged_inn2(function):
    def _function(request,*args,**kwargs):
        m = Registration.objects.get(user = request.user)
        if m.User_role != 'admin':
            try:
                del request.session['logg']
                messages.success(request, 'Please login as admin')
                return HttpResponseRedirect('home')
            except:
                messages.success(request, 'Please login as admin')
                return HttpResponseRedirect('home')
        else:
            return function(request, *args, **kwargs)
    return _function


def logged_inn3(function):
    def _function(request,*args,**kwargs):
        m = Registration.objects.get(user = request.user)
        if m.User_role != 'student':
            try:
                del request.session['logg']
                messages.success(request, 'Please login as student')
                return HttpResponseRedirect('home')
            except:
                messages.success(request, 'Please login as student')
                return HttpResponseRedirect('home')
        else:
            return function(request, *args, **kwargs)
    return _function


def logged_inn4(function):
    def _function(request,*args,**kwargs):
        m = Registration.objects.get(user = request.user)
        if m.User_role != 'teacher':
            try:
                del request.session['logg']
                messages.success(request, 'Please login as teacher')
                return HttpResponseRedirect('home')
            except:
                messages.success(request, 'Please login as teacher')
                return HttpResponseRedirect('home')
        else:
            return function(request, *args, **kwargs)
    return _function