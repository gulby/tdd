#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import HttpResponse


def persona_login(request):
    authenticate(assertion=request.POST['assertion'])
    return HttpResponse()
    