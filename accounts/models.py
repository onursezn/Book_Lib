from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class UserProfileManager(BaseUserManager):

    def create_users(self, email, username, first_name, last_name, password = None):
        """create new user profile"""
        if not email or not username:
            raise ValueError('User must have an email address and username')

        email = self.normalize_email(email)
        user = self.model(email = email, first_name = first_name, 
                          last_name = last_name, username = username)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, first_name, last_name=None, password = None):
        user = self.create_users(email, username, first_name, last_name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    first_login = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add = True)
    last_login = models.DateTimeField(auto_now = True, null = True)

    objects = UserProfileManager()
        
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        """string representation of the user"""
        return self.username

    def check_password(self, raw_password):
        
        return check_password(raw_password, self.password)

