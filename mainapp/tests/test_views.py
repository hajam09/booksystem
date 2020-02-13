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
		# payload = {"fullname": "Anthony Josh", "email": "josh.brolin@gmail.com", "password": "123", "listofgenre": "['Crime', 'Comics', 'Action']"}
		# response = self.client.put(reverse('mainapp:update_profile'), payload)
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
	# Need to test session
	# Need to test PUT request for different functionality
	# Need to test for redirect, HttpResponse
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

		ISBN_13 = 9876543212345
		ISBN_10 = 7685747586
		title = "A View from the Bridge"
		book_data = { "id": "vKJewgEACAAJ", "etag": "e8wZTpMgieo", "title": "A View from the Bridge",
		"authors": "Mohamed,Haja,Nijam", "publisher": "Longman", "publishedDate": "1999-02-11",
		"description": "Some random description for this book.", "ISBN_10": "7685747586",
		"ISBN_13": "9876543212345", "categories": [ "Digital Communications" ], "averageRating": 0.0,
		"ratingsCount": 0, "thumbnail": "http://books.google.com/books/content?id=vKJewgEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api" }
		new_book = Book.objects.create(isbn_13=ISBN_13, isbn_10=ISBN_10, title=title, book_data=book_data)
		self.book = new_book

	def test_redirects(self):
		self.client.logout()

		response = self.client.get(reverse('mainapp:user_shelf'))
		self.assertEquals(response.status_code, 302)
		self.assertRedirects(response, '/login/')

		newuser = self.create_user("joshu.brolin@gmail.com", "joshu.brolin@gmail.com", "RanDomPasWord56", "Josh", "Brolin")
		self.logged_in = self.client.login(username='joshu.brolin@gmail.com', password='RanDomPasWord56')
		response = self.client.get(reverse('mainapp:user_shelf'))
		self.assertEquals(response.status_code, 302)
		self.assertRedirects(response, '/not_found/')

		#Incorrect ISBN 13
		payload = {"functionality": "remove-from-favourites", "isbn_13": 9876555512345, "isbn_10": 7685747586}
		response = self.client.put(reverse('mainapp:user_shelf'), payload)
		self.assertEquals(response.status_code, 302)
		self.assertRedirects(response, '/not_found/')

		#Function is not receiving payload for put request

	def test_ajax_put(self):
		pass

class BookPageTest(TestCase):
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

		ISBN_13 = "9876543212345"
		ISBN_10 = "7685747586"
		title = "A View from the Bridge"
		book_data = { "id": "vKJewgEACAAJ", "etag": "e8wZTpMgieo", "title": "A View from the Bridge",
		"authors": "Mohamed,Haja,Nijam", "publisher": "Longman", "publishedDate": "1999-02-11",
		"description": "Some random description for this book.", "ISBN_10": "7685747586",
		"ISBN_13": "9876543212345", "categories": [ "Digital Communications" ], "averageRating": 0.0,
		"ratingsCount": 0, "thumbnail": "http://books.google.com/books/content?id=vKJewgEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api" }
		new_book = Book.objects.create(isbn_13=ISBN_13, isbn_10=ISBN_10, title=title, book_data=book_data)
		self.book = new_book

	def test_redirects(self):

		response = self.client.get(reverse('mainapp:book_page', kwargs={'isbn_13': 7876543212345}))
		self.assertEquals(response.status_code, 302)
		self.assertRedirects(response, '/not_found/')

		self.client.logout()

		payload = {"functionality": "remove-from-favourites", "isbn_13": 9876543212345, "isbn_10": 7685747586}
		response = self.client.put(reverse('mainapp:book_page', kwargs={'isbn_13':9876543212345}), payload)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.content.decode("utf-8"), "not_authenticated")

		payload = {"functionality": "remove-from-favourites", "isbn_13": 9876543212345, "isbn_10": 7685747586}
		response = self.client.post(reverse('mainapp:book_page', kwargs={'isbn_13':"9876543212345"}), payload)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.content.decode("utf-8"), "not_authenticated")

	def test_create_review(self):
		# Need to comment out some following in views.py BUT WORKS
		#average_rating_recommendation = weighted_average_and_favourite_score(request)
		#similar_books = content_based_similar_items(request, book_title)
		# payload = {"functionality": "create-review", "isbn_13": "9876543212345", "isbn_10": "7685747586", 'user_review': "Some review for this book", "user_rating": 4}
		# self.logged_in = self.client.login(username='josh.brolin@gmail.com', password='RanDomPasWord56')
		# response = self.client.post(reverse('mainapp:book_page', kwargs={'isbn_13':"9876543212345"}), payload, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		# self.assertEquals(response.status_code, 200)
		# the_response = response.content.decode("utf-8").split("&nbsp;")
		# self.assertEquals(the_response[0], "revew_created_successfully")
		# the_user = User.objects.get(email="josh.brolin@gmail.com")
		# self.assertEquals(the_response[1], the_user.first_name+" "+the_user.last_name)
		# self.assertEquals(the_response[2], payload["user_review"])
		# self.assertEquals(int(the_response[3]), payload["user_rating"])
		pass

	#Need to test for put request for 4 buttons
	def test_put_favourites(self):
		# payload not received for put request
		# self.logged_in = self.client.login(username='josh.brolin@gmail.com', password='RanDomPasWord56')
		# payload = {"functionality": "add-to-favourites", "isbn_13": "9876543212345"}
		# response = self.client.put(reverse('mainapp:book_page', kwargs={'isbn_13':"9876543212345"}), payload)
		# self.assertEquals(response.status_code, 200)
		pass

class NotFoundTest(TestCase):
	def test_404_page(self):
		response = self.client.get(reverse('mainapp:not_found'))
		self.assertEquals(response.status_code, 200)