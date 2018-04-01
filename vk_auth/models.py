from django.db import models

# Create your models here.


class AuthModel(models.Model):
    token = models.CharField(max_length=128)
    expires_at = models.DateTimeField()
    user_id = models.CharField(max_length=128)
