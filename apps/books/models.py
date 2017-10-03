from __future__ import unicode_literals
from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors["name"] = "First name should be more than 2 characters"
        if len(postData['alias']) < 2:
            errors["alias"] = "Alias should be more than 2 characters"
        if not re.match(EMAIL_REGEX, postData['email'] ):
            errors["email"] = "Email needs to be valid"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be 8 charcters or more"
        if postData['password'] != postData['confirm']:
            errors['confirm'] = 'Password has to match confirmation'
        return errors
class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
class Review(models.Model):
    content = models.TextField()
    rating = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name = "reviews")
    book = models.ForeignKey(Book, related_name = "reviews")
