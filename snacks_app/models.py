from django.db import models
from login_app.models import User

class SnackManager(models.Manager):
    def addValidation(self, post_data):
        errors={}
        if  len(post_data['title']) < 5:
            errors['title'] = 'Title must be at least 5 characters.'
        if len(post_data['description']) < 10:
            errors['description'] = 'Description must be at least 10 characters'
        return errors

class Snack(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    creator = models.ForeignKey(User, related_name='snacks', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_snacks')
    dislikes = models.ManyToManyField(User, related_name='disliked_snacks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SnackManager()



