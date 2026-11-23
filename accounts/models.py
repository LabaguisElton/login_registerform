from django.db import models
from django.contrib.auth.models import User


class Account(User):
    class Meta:
        proxy = True
        verbose_name = 'account'
        verbose_name_plural = 'accounts'
