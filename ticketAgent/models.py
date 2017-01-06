from __future__ import unicode_literals
from django.core.validators import RegexValidator
from django.db import models


# Create your models here.
class SignUp(models.Model):
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120)
    email = models.EmailField()
    password = models.CharField(max_length=60, validators=[RegexValidator(regex='^[^;]{4,}$', message='Length has to be greater than 4 and ; char is not allowed', code='nomatch')])
    repeat_password = models.CharField(max_length=60, validators=[RegexValidator(regex='^[^;]{4,}$', message='Length has to be greater than 4 and ; char is not allowed', code='nomatch')])

    def __str__(self):
        return self.email

    def __unicode__(self):
        return self.email


class LogIn(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=60)

    def __str__(self):
        return self.email

    def __unicode__(self):
        return self.email


