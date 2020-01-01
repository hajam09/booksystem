from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class CustomerAccountProfile(models.Model):
	userid = models.ForeignKey(User, on_delete=models.CASCADE)
	birthDate = models.DateField()
	gender = models.CharField(max_length=1000)
	userfavouritegenre =  models.CharField(max_length=1000)

class Book(models.Model):
	isbn_13 = models.CharField(max_length=15)
	isbn_10 = models.CharField(max_length=15)
	title =  models.CharField(max_length=1000, default=None)
	favourites = models.ManyToManyField(CustomerAccountProfile, related_name='favourites', default="none")
	readingnow = models.ManyToManyField(CustomerAccountProfile, related_name='readingnow', default="none")
	toread = models.ManyToManyField(CustomerAccountProfile, related_name='toread', default="none")
	haveread = models.ManyToManyField(CustomerAccountProfile, related_name='haveread' ,default="none")