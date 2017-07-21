# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.shortcuts import render, redirect, HttpResponse
import bcrypt
import re
import datetime

#LOGIN AND REGISTRATION MODELS
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

class UserManager(models.Manager):
    def register_validator(self, user_input):
        errors = {}
        input_email = user_input['email']
        input_username = user_input['username']
        input_birthday = user_input['birthday']
        check_email_list = User.objects.filter(email = input_email)
        check_username = User.objects.filter(username = input_username)
        if len(check_email_list) <> 0:
            errors['existing'] = 'This email is already registered. Log in.'
        if len(check_email_list) <> 0:
            errors['username'] = 'This username is already taken. Try another.'
        if len(user_input['first_name']) < 2:
            errors['first_name'] = 'First name must be at least 2 characters long'
        if not (user_input['first_name']).isalpha() or not (user_input['last_name']).isalpha():
            errors['name_chars'] = 'Name fields can only contain letters of the alphabet'
        if len(user_input['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters long'
        if len(user_input['username']) < 2:
            errors['username_length'] = 'Username must be at least 2 characters long'
        if user_input['password'] != user_input['confirm_pw']:
            errors['confirm_pw'] = 'Passwords do not match. Try again.'
        if len(user_input['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters long'
        if not len(user_input['birthday']):
            errors['birthday'] = 'Must input birthday.'
        if not EMAIL_REGEX.match(user_input['email']):
            errors['email'] = 'Email syntax not valid.'
        return errors 
    def login_validator(self, user_input):
        errors = {}
        input_email = user_input['email']
        input_password = user_input['password']
        check_user = User.objects.filter(email = input_email)
        if len(check_user) == 0:
            errors['not_registered'] = 'Email not in system. Register first before attempting login.'
        if not bcrypt.checkpw(input_password.encode(), check_user[0].password.encode()):
            errors['wrong_password'] = 'Incorrect password. Please try again.'
        return errors 

class QuoteManager(models.Manager):
    def quote_validator(self, quote_input):
        errors = {}
        input_speaker = quote_input['speaker']
        input_content = quote_input['content']
        if len(input_speaker) == 0:
            errors['speaker'] = "Let us know who said this! Input the speaker's name in the appropriate field."
        if len(input_content) == 0:
            errors['content'] = "While silence is golden, it's not a quote. Please fill out the content section."
        return errors 

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255, unique=True)
    email = models.CharField(max_length = 255, unique = True)
    password = models.CharField(max_length = 45)
    birthday = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()

class Quote(models.Model):
    speaker = models.CharField(max_length = 255)
    content = models.TextField()
    user = models.ForeignKey(User, related_name = "quotes")
    created_at = models.DateTimeField(auto_now_add = True)
    objects = QuoteManager()

class Favorite(models.Model):
    user = models.ForeignKey(User, related_name = "favorites")
    quote = models.ForeignKey(Quote, related_name = "favorited")
    created_at = models.DateTimeField(auto_now_add = True)
