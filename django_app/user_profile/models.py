from django.db import models
from django.contrib.auth.models import User

class PhotoForUser(models.Model):
    photo = models.ImageField(upload_to='media/users', height_field=None, width_field=None, max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)