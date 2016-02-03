#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import requests
from django.contrib.auth import get_user_model
User = get_user_model()

PERSONA_VERIFY_URL = 'https://verifier.login.persona.org/verify'
DOMAIN = 'localhost'


class PersonaAuthenticationBackend(object):

    def authenticate(self, assertion):
        response = requests.post(
            PERSONA_VERIFY_URL,
            data={'assertion': assertion, 'audience': DOMAIN}
        )
        if response.ok and response.json()['status'] == 'okay':
            email = response.json()['email']
            user = None
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = User.objects.create(email=email)
            return user
        else:
            return None

    def get_user(self, pk):
        user = None
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            user = None
            
        return user
        