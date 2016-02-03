#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.db import models
from django.utils import timezone
#from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


'''
class UserManager(BaseUserManager):
    def create_user(self, email):
        User.objects.create(email=email)
        
    def create_superuser(self, email, password):
        self.create_user(email)
'''

        
class User(models.Model):
    email = models.EmailField(unique=True)
    last_login = models.DateTimeField(default=timezone.now)
    REQUIRED_FIELDS = ()
    USERNAME_FIELD = 'email'
