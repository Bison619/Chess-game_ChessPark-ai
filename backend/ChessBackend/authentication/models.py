from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=100,unique=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.username