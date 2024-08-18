from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    email = models.CharField(max_length=150, unique=True, default='default@example.com')

    def __str__(self):
        return self.username
