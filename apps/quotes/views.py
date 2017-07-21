# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt
import re
from django.core.urlresolvers import reverse
import datetime

def index(request):
    if 'current_user_name' not in request.session:
        request.session['current_user_id'] = 0
    if 'action' not in request.session:
        request.session['action'] = ''
    return render(request, 'quotes/index.html')

def register_user(request):
    if request.method == 'POST':
        errors = User.objects.register_validator(request.POST)
        request.session['action'] = 'register'
        if len(errors):
            for error, error_message in errors.iteritems():
                messages.error(request, error_message, extra_tags = error)
            return redirect('/')
        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            secret_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            birthday = request.POST['birthday']
            new_user = User.objects.create(first_name = first_name, last_name = last_name, username = username, email = email, password = secret_password, birthday = birthday)
            new_user.save()
            request.session['current_user_id'] = new_user.id
            request.session['action'] = 'register success'
            return redirect('/')
    else:
        return redirect('/')

def login_user(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        request.session['action'] = 'login'
        if len(errors):
            for error, error_message in errors.iteritems():
                messages.error(request, error_message, extra_tags = error)
            return redirect('/')
        else:
            email = request.POST['email']
            this_user = User.objects.get(email = email)
            this_user.save()
            request.session['current_user_id'] = this_user.id
            return redirect('/quotes') 
    else:
        return redirect('/')

def load_home(request):
    user = User.objects.get(id = request.session['current_user_id'])
    all_quotes = Quote.objects.all()
    favorite_list = Favorite.objects.filter(user = user)
    left_display_quotes = []
    for i in range(len(all_quotes)):
        favorited = False
        for j in range(len(favorite_list)):
            if all_quotes[i].id == favorite_list[j].quote.id:
                favorited = True
                break
        if favorited == False:
            left_display_quotes.insert(0, all_quotes[i])
    context = {
        'user' : user,
        'favorite_list' : favorite_list,
        'quote_list' : left_display_quotes,
    }
    return render(request, 'quotes/welcome_wall.html', context)

def add_quote(request):
    if request.method == 'POST':
        errors = Quote.objects.quote_validator(request.POST)
        if len(errors):
            for error, error_message in errors.iteritems():
                messages.error(request, error_message, extra_tags = error)
            return redirect('/quotes')
        else:
            speaker = request.POST['speaker']
            content = request.POST['content']
            user = User.objects.get(id = request.session['current_user_id'])
            new_quote = Quote.objects.create(speaker = speaker, content = content, user = user)
            new_quote.save()
            return redirect('/quotes')
    else:
        return redirect('/quotes')

def add_favorite(request, quote_id):
    quote = Quote.objects.get(id = quote_id)
    user = User.objects.get(id = request.session['current_user_id'])
    new_favorite = Favorite.objects.create(quote = quote, user = user)
    new_favorite.save()
    return redirect('/quotes')

def remove_favorite(request, favorite_id):
    bye_favorite = Favorite.objects.get(id = favorite_id)
    bye_favorite.delete()
    return redirect('/quotes')

def user_page(request, user_id):
    user = User.objects.get(id = user_id)
    user_posts = Quote.objects.filter(user__id = user_id)
    post_count = len(user_posts)
    context = {
        'user' : user,
        'posts' : user_posts,
        'count' : post_count
    }
    return render(request, "quotes/show_user.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')
