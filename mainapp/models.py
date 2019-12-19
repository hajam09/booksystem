from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class CustomerAccountProfile(models.Model):
	userid = models.ForeignKey(User, on_delete=models.CASCADE)
	birthDate = models.DateField()
	gender = models.CharField(max_length=1000)
	userfavouritegenre =  models.CharField(max_length=1000)

class Books(models.Model):
	isbn_13 = models.CharField(max_length=15)
	isbn_10 = models.CharField(max_length=15)
	title =  models.CharField(max_length=1000, default=None)
