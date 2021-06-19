from django.db import models
from datetime import date, time, datetime, timedelta
import re
import bcrypt


class UserManager(models.Manager):
  def addValidation(self, post_data):
    errors = {}
    email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if len(post_data['first_name']) < 1:
      errors['first_name'] = 'First name must be at least 1 characters'
    if len(post_data['last_name']) < 1:
      errors['last_name'] = 'Last name must be at least 1 characters'
    if not email_regex.match(post_data['email']):
      errors['email'] = "Invalid email address!"
    else:
      try:
        self.get(email=post_data['email'])
        errors['email'] = "This email already exists!"
      except:
        pass
    if len(post_data['password']) < 8:
      errors['password'] = 'Password must be at least 8 characters'
    else:
      if post_data['password'] != post_data['c_password']:
        errors['password'] = 'Passwords do not match!'
    return errors

  def loginValidation(self, post_data):
    errors = {}
    email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if not post_data['password']:
      errors['password'] = 'Password is missing!'
    if not email_regex.match(post_data['email']):
      errors['email'] = "Invalid email address!"
    return errors

  def resetValidation(self, post_data):
    errors = {}
    email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if not post_data['password']:
      errors['password'] = 'Password is missing!'
    if not email_regex.match(post_data['email']):
      errors['email'] = "Invalid email address!"
    if len(post_data['password']) < 8:
      errors['password'] = 'Password must be at least 8 characters'
    else:
      if post_data['password'] != post_data['c_password']:
        errors['password'] = 'Passwords do not match!'
    return errors

  def editValidator(self, post_data, user):
    errors = {}
    if post_data['crnt_password']:
      if not bcrypt.checkpw(post_data['crnt_password'].encode(), user.password.encode()):
        errors['first_name'] = 'Current Password does not match... cannot edit profile!'
        return errors
    else:
      errors['password'] = 'Current Password cannot be blank!'
    if post_data['first_name']:
      if len(post_data['first_name']) < 1:
        errors['first_name'] = 'First name must be at least 1 characters'
    if post_data['last_name']:
      if len(post_data['last_name']) < 1:
        errors['last_name'] = 'Last name must be at least 1 characters'
    if post_data['email']:
      email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
      if not email_regex.match(post_data['email']):
        errors['email'] = "Invalid email address!"
      else:
        if post_data['email'] != user.email:
          try:
            self.get(email=post_data['email'])
            errors['email'] = "This email already exists!"
          except:
            pass
    
      if post_data['new_password']:
        if len(post_data['new_password']) < 8:
          errors['password'] = 'Password must be at least 8 characters'
        else:
          if post_data['new_password'] != post_data['c_new_password']:
            errors['password'] = 'Passwords do not match!'
    return errors

class User(models.Model):
  first_name = models.CharField(max_length=55)
  last_name = models.CharField(max_length=55)
  email = models.EmailField(unique=True)
  password = models.CharField(max_length=128)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager()
