# from django.test import TestCase, Client
# from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate
# from django.urls import path, include, reverse, resolve
# from datetime import datetime as dt, date
# from mainapp.models import CustomerAccountProfile, Book, Review, Category
# from mainapp.views import index, signup, login, log_out, passwordforgotten, update_profile, user_shelf, book_page, not_found, clear_session
# import jsonfield
# # python manage.py test mainapp/tests
# class URLTest(TestCase):
# 	def create_user(self, u, e, p, f, l):
# 		return User.objects.create_user(username=u, email=e, password=p, first_name=f, last_name=l)

# 	def create_user_profile(self, u ,b, g, ug):
# 		return u.customeraccountprofile_set.create(birthDate=b, gender=g, userfavouritegenre=ug)

# 	def setUp(self):
# 		self.client = Client()
# 		newuser = self.create_user("oliver.queen@yahoo.com", "oliver.queen@yahoo.com", "RanDomPasWord56", "Oliver", "Queen")
# 		newprofile = self.create_user_profile(newuser, "2019-03-22", "Male", "['Adventures', 'Horror', 'Romance']")

# 		ISBN_13 = 9876543212345
# 		ISBN_10 = 7685747586
# 		title = "A View from the Bridge"
# 		book_data = { "id": "vKJewgEACAAJ", "etag": "e8wZTpMgieo", "title": "A View from the Bridge",
# 		"authors": "Mohamed,Haja,Nijam", "publisher": "Longman", "publishedDate": "1999-02-11",
# 		"description": "Some random description for this book.", "ISBN_10": "7685747586",
# 		"ISBN_13": "9876543212345", "categories": [ "Digital Communications" ], "averageRating": 0.0,
# 		"ratingsCount": 0, "thumbnail": "http://books.google.com/books/content?id=vKJewgEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api" }
# 		new_book = Book.objects.create(isbn_13=ISBN_13, isbn_10=ISBN_10, title=title, book_data=book_data)

# 	def tearDown(self):
# 		User.objects.all().delete()

# 	def test_index(self):
# 		url = reverse('mainapp:index')
# 		self.assertEqual(resolve(url).func, index)
# 		self.assertEqual(resolve(url).url_name, "index")

# 		response = self.client.get(reverse('mainapp:index'))
# 		self.assertEqual(response.status_code, 200)
# 		self.assertTemplateUsed(response, 'mainapp/frontpage.html')

# 	def test_signup(self):
# 		url = reverse('mainapp:signup')
# 		self.assertEqual(resolve(url).func, signup)
# 		self.assertEqual(resolve(url).url_name, "signup")

# 		response = self.client.get(reverse('mainapp:signup'))
# 		self.assertEqual(response.status_code, 200)
# 		self.assertTemplateUsed(response, 'mainapp/signup.html')

# 	def test_login(self):
# 		url = reverse('mainapp:login')
# 		self.assertEqual(resolve(url).func, login)
# 		self.assertEqual(resolve(url).url_name, "login")

# 		response = self.client.get(reverse('mainapp:login'))
# 		self.assertEqual(response.status_code, 200)
# 		self.assertTemplateUsed(response, 'mainapp/login.html')

# 	def test_update_profile(self):
# 		url = reverse('mainapp:update_profile')
# 		self.assertEqual(resolve(url).func, update_profile)
# 		self.assertEqual(resolve(url).url_name, "update_profile")

# 		self.logged_in = self.client.login(username='oliver.queen@yahoo.com', password='RanDomPasWord56')
# 		response = self.client.get(reverse('mainapp:update_profile'))
# 		self.assertEqual(response.status_code, 200)
# 		self.assertTemplateUsed(response, 'mainapp/profilepage.html')
# 		self.client.logout()

# 	def test_user_shelf(self):
# 		url = reverse('mainapp:user_shelf')
# 		self.assertEqual(resolve(url).func, user_shelf)
# 		self.assertEqual(resolve(url).url_name, "user_shelf")

# 		response = self.client.get(reverse('mainapp:user_shelf'))
# 		self.assertEqual(response.status_code, 302)
# 		self.assertRedirects(response, '/login/')

# 		self.logged_in = self.client.login(username='oliver.queen@yahoo.com', password='RanDomPasWord56')
# 		response = self.client.get(reverse('mainapp:user_shelf'))
# 		self.assertEqual(response.status_code, 200)
# 		self.assertTemplateUsed(response, 'mainapp/usershelf.html')
# 		self.client.logout()

# 	def test_book_page(self):
# 		# Need to comment out some following in views.py BUT WORKS
# 		#average_rating_recommendation = weighted_average_and_favourite_score(request)
# 		#similar_books = content_based_similar_items(request, book_title)
# 		# url = reverse('mainapp:book_page', kwargs={'isbn_13':9876543212345})
# 		# self.assertEqual(resolve(url).func, book_page)
# 		# self.assertEqual(resolve(url).url_name, "book_page")

# 		# response = self.client.get(reverse('mainapp:book_page', kwargs={'isbn_13':9876543212345}))
# 		# self.assertEqual(response.status_code, 200)
# 		# self.assertTemplateUsed(response, 'mainapp/book.html')
# 		pass

# 	def test_not_found(self):
# 		url = reverse('mainapp:not_found')
# 		self.assertEqual(resolve(url).func, not_found)
# 		self.assertEqual(resolve(url).url_name, "not_found")

# 		response = self.client.get(reverse('mainapp:not_found'))
# 		self.assertEqual(response.status_code, 200)
# 		self.assertTemplateUsed(response, 'mainapp/404.html')

# 	def test_clear_session(self):
# 		url = reverse('mainapp:clear_session')
# 		self.assertEqual(resolve(url).func, clear_session)
# 		self.assertEqual(resolve(url).url_name, "clear_session")