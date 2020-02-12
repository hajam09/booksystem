from django.test import TestCase, Client, RequestFactory
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from django.urls import path, include, reverse, resolve
from datetime import datetime as dt, date
from mainapp.models import CustomerAccountProfile, Book, Review, Category
from mainapp.views import index, signup, login, log_out, passwordforgotten, update_profile, user_shelf, book_page, not_found, clear_session
import jsonfield, requests, json, random
# python manage.py test mainapp/tests
# Need to test for http response from ajax

class IndexTest(TestCase):
	pass

class SignupTest(TestCase):
	def create_user(self, u, e, p, f, l):
		return User.objects.create_user(username=u, email=e, password=p, first_name=f, last_name=l)

	def create_user_profile(self, u ,b, g, ug):
		return u.customeraccountprofile_set.create(birthDate=b, gender=g, userfavouritegenre=ug)

	def setUp(self):
		client = Client()

		start_dt = date.today().replace(day=1, month=1).toordinal()
		end_dt = date.today().toordinal()
		self.birthDate = str(date.fromordinal(random.randint(start_dt, end_dt)))

	def test_ajax_post_weak_password(self):
		payload = {'fullname': 'Barry Allen', 'email': 'barry.allen14@yahoo.com',
		'password': "weakpassword", "birthDate": self.birthDate, "gender": "Male",
		"listofgenre": "['Action', 'Adventures', 'Horror']"}
		response = self.client.post(reverse('mainapp:signup'), payload, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.content.decode("utf-8"), "Password is not secure enough!")

	def test_ajax_post_user_exist(self):
		newuser = self.create_user("oliver.queen@yahoo.com", "oliver.queen@yahoo.com", "RanDomPasWord56", "Oliver", "Queen")
		newprofile = self.create_user_profile(newuser, "2019-03-22", "Male", "['Adventures', 'Horror', 'Romance']")

		payload = {'fullname': 'Oliver Queen', 'email': 'oliver.queen@yahoo.com',
		'password': "StrongPassword2020", "birthDate": self.birthDate, "gender": "Male",
		"listofgenre": "['Action', 'Adventures', 'Horror']"}
		response = self.client.post(reverse('mainapp:signup'), payload, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.content.decode("utf-8"), "An account already exists for this email address, please try again!")

	def test_ajax_post_success_creation(self):
		pass


class LoginTest(TestCase):
	def setUp(self):
		self.client = Client()
		user = User.objects.create_user(username='josh.brolin@gmail.com', email='josh.brolin@gmail.com', password='Maideen69', first_name='Josh', last_name='Brolin')

	def test_ajax_post(self):
		#Incorrect e-mail / password
		payload = {'email': 'josh.brolin@gmail.com', 'password': 'Ma8hgv6een89'}
		response = self.client.post(reverse('mainapp:login'), payload, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.content.decode("utf-8"), "Sorry! Username and Password didn't match, Please try again!")

		#Correct e-mail / password
		payload = {'email': 'josh.brolin@gmail.com', 'password': 'Maideen69'}
		response = self.client.post(reverse('mainapp:login'), payload,follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.assertEquals(response.status_code, 200)
		self.assertTrue(response.context['user'].is_authenticated)

class LogoutTest(TestCase):
	pass

class UpdateProfileTest(TestCase):
	def create_user(self, u, e, p, f, l):
		return User.objects.create_user(username=u, email=e, password=p, first_name=f, last_name=l)

	def create_user_profile(self, u ,b, g, ug):
		return u.customeraccountprofile_set.create(birthDate=b, gender=g, userfavouritegenre=ug)

	def setUp(self):
		self.client = Client()
		self.factory = RequestFactory()
		newuser = self.create_user("josh.brolin@gmail.com", "josh.brolin@gmail.com", "RanDomPasWord56", "Josh", "Brolin")
		newprofile = self.create_user_profile(newuser, "2019-03-22", "Male", "['Adventures', 'Horror', 'Romance']")
		self.logged_in = self.client.login(username='josh.brolin@gmail.com', password='RanDomPasWord56')

	def test_ajax_put(self):
		#payload not passed to the view function
		# payload = {'fullname': 'Anthony Josh', 'email': 'josh.brolin@gmail.com', 'password': "123", 'listofgenre': "['Crime', 'Comics', 'Action']"}
		# response = self.client.put(reverse('mainapp:update_profile'), payload, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		# self.assertEquals(response.status_code, 200)
		# self.assertEquals(response.content.decode("utf-8"), "Passsword is not secure enough!")
		pass

	def test_redirects(self):
		self.client.logout()

		response = self.client.get(reverse('mainapp:update_profile'))
		self.assertEquals(response.status_code, 302)
		self.assertRedirects(response, '/login/')
		#self.assertEquals(response.url, '/login/')

		newuser = self.create_user("joshu.brolin@gmail.com", "joshu.brolin@gmail.com", "RanDomPasWord56", "Josh", "Brolin")
		self.logged_in = self.client.login(username='joshu.brolin@gmail.com', password='RanDomPasWord56')
		response = self.client.get(reverse('mainapp:update_profile'))
		self.assertEquals(response.status_code, 302)
		self.assertRedirects(response, '/not_found/')
		# self.assertEquals(response.url, '/not_found/')

class UserShelfTest(TestCase):
	pass

class BookPageTest(TestCase):
	pass

class NotFoundTest(TestCase):
	pass