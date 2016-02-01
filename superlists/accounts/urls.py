#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.conf.urls import url
from accounts.views import persona_login

urlpatterns = [
    url(r'^login$', persona_login, name='persona_login'),
]
