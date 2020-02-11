from django.test import TestCase, Client
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.urls import path, include, reverse, resolve
from datetime import datetime as dt, date
from mainapp.models import CustomerAccountProfile, Book, Review, Category
from mainapp.views import index, signup, login, log_out, passwordforgotten, update_profile, user_shelf, book_page, not_found, clear_session
import jsonfield
# python manage.py test mainapp/tests
class URLTest(TestCase):
	def create_user(self, u, e, p, f, l):
		return User.objects.create_user(username=u, email=e, password=p, first_name=f, last_name=l)

	def create_user_profile(self, u ,b, g, ug):
		return u.customeraccountprofile_set.create(birthDate=b, gender=g, userfavouritegenre=ug)

	def setUp(self):
		self.client = Client()
		newuser = self.create_user("oliver.queen@yahoo.com", "oliver.queen@yahoo.com", "RanDomPasWord56", "Oliver", "Queen")
		newprofile = self.create_user_profile(newuser, "2019-03-22", "Male", "['Adventures', 'Horror', 'Romance']")

	def tearDown(self):
		User.objects.all().delete()

	def test_index(self):
		url = reverse('mainapp:index')
		self.assertEqual(resolve(url).func, index)
		self.assertEqual(resolve(url).url_name, "index")

		response = self.client.get(reverse('mainapp:index'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'mainapp/frontpage.html')

	def test_signup(self):
		url = reverse('mainapp:signup')
		self.assertEqual(resolve(url).func, signup)
		self.assertEqual(resolve(url).url_name, "signup")

		response = self.client.get(reverse('mainapp:signup'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'mainapp/signup.html')

	def test_login(self):
		url = reverse('mainapp:login')
		self.assertEqual(resolve(url).func, login)
		self.assertEqual(resolve(url).url_name, "login")

		response = self.client.get(reverse('mainapp:login'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'mainapp/login.html')

	def test_update_profile(self):
		url = reverse('mainapp:update_profile')
		self.assertEqual(resolve(url).func, update_profile)
		self.assertEqual(resolve(url).url_name, "update_profile")

		response = self.client.get(reverse('mainapp:update_profile'))
		self.assertEqual(response.status_code, 302)# Because the user needs to be logged in in order to get 200., find way to login user in back end. Then undo below.
		#self.assertTemplateUsed(response, 'mainapp/profilepage.html')

	def test_user_shelf(self):
		url = reverse('mainapp:user_shelf')
		self.assertEqual(resolve(url).func, user_shelf)
		self.assertEqual(resolve(url).url_name, "user_shelf")

		response = self.client.get(reverse('mainapp:user_shelf'))
		self.assertEqual(response.status_code, 302)
		#self.assertTemplateUsed(response, 'mainapp/usershelf.html')

	# def test_book_page(self):
	# 	url = reverse('mainapp:book_page', kwargs={'isbn_13':9781447218296})
	# 	self.assertEqual(resolve(url).func, book_page)
	# 	self.assertEqual(resolve(url).url_name, "book_page")

	# 	response = self.client.get(reverse('mainapp:book_page', kwargs={'isbn_13':9781447218296}))
	# 	self.assertEqual(response.status_code, 200)
	# 	self.assertTemplateUsed(response, 'mainapp/book.html')

	def test_not_found(self):
		url = reverse('mainapp:not_found')
		self.assertEqual(resolve(url).func, not_found)
		self.assertEqual(resolve(url).url_name, "not_found")

		response = self.client.get(reverse('mainapp:not_found'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'mainapp/404.html')

	def test_clear_session(self):
		url = reverse('mainapp:clear_session')
		self.assertEqual(resolve(url).func, clear_session)
		self.assertEqual(resolve(url).url_name, "clear_session")