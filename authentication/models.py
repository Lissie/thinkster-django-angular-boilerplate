from django.contrib.auth.models import BaseUserManager

class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username.')

        account = self.model(
         #refers to the model attribute of BaseUserManager, refers to setting.AUTH_USER_MODEL
            email = self.normalize_email(email),
            username = kwargs.get('username')
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)

        account.is_admin = True
        account.save()

        return account


from django.contrib.auth.models import AbstractBaseUser
from django.db import models

class Account(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)

    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    tagline = models.CharField(max_length=140, blank=True)

    is_admin = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    #auto_now_add = True => This field should be automatically set when the object is created and non-editable after that
    updated_at = models.DateTimeField(auto_now=True)
    #updated_at is automatically set by Django. The difference is, that it causes the field to update each time the object is saved.

    objects = AccountManager()

    USERNAME_FIELD = 'email' #To set the email as username
    REQUIRED_FIELDS = ['username']

    def __unicode__(self): #More or less, changes the base print of the class, when printed, will print the email
        return self.email

    def get_full_name(self): #Django convention
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self): #Django conventions
        return self.first_name
