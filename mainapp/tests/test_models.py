from django.test import TestCase, Client
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.urls import path, include, reverse, resolve
from datetime import datetime, date
from mainapp.models import CustomerAccountProfile, Book, Review, Category
import jsonfield
# python manage.py test mainapp/tests
class CustomerAccountProfileTest(TestCase):
	def create_user(self, u, e, p, f, l):
		return User.objects.create_user(username=u, email=e, password=p, first_name=f, last_name=l)

	def create_user_profile(self, u ,b, g, ug):
		return u.customeraccountprofile_set.create(birthDate=b, gender=g, userfavouritegenre=ug)

	def setUp(self):
		newuser = self.create_user("oliver.queen@yahoo.com", "oliver.queen@yahoo.com", "RanDomPasWord56", "Oliver", "Queen")
		newprofile = self.create_user_profile(newuser, "2019-03-22", "Male", "[Adventures, Horror, Romance]")

	def tearDown(self):
		User.objects.all().delete()

	def test_user_attributes(self):
		user = User.objects.get(email="oliver.queen@yahoo.com")
		self.assertEqual(user.username,"oliver.queen@yahoo.com")
		self.assertEqual(user.first_name,"Oliver")
		self.assertEqual(user.last_name,"Queen")

	def test_profile_attribute(self):
		user = User.objects.get(email="oliver.queen@yahoo.com")
		user_profile = CustomerAccountProfile.objects.get(userid=user)
		self.assertEqual(user_profile.gender, "Male")
		self.assertEqual(user_profile.userfavouritegenre, "[Adventures, Horror, Romance]")

	def test_user_exist(self):
		num_results = User.objects.filter(email="oliver.queen@yahoo.com").count()
		self.assertEqual(1,num_results)

	def test_profile_exist(self):
		user = User.objects.get(email="oliver.queen@yahoo.com")
		user_profile = CustomerAccountProfile.objects.filter(userid=user).count()
		self.assertEqual(1,user_profile)


class BookTest(TestCase):
	pass

class ReviewTest(TestCase):
	pass

class CategoryTest(TestCase):
	pass