from django.db import models

# Create your models here.


class Role(models.Model):
    role = models.CharField(max_length=250)

