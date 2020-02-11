from django.test import TestCase, Client
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.urls import path, include, reverse, resolve
from datetime import datetime as dt, date
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
		newprofile = self.create_user_profile(newuser, "2019-03-22", "Male", "['Adventures', 'Horror', 'Romance']")

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
		self.assertEqual(user_profile.userfavouritegenre, "['Adventures', 'Horror', 'Romance']")

	def test_user_exist(self):
		num_results = User.objects.filter(email="oliver.queen@yahoo.com").count()
		self.assertEqual(1,num_results)

	def test_profile_exist(self):
		user = User.objects.get(email="oliver.queen@yahoo.com")
		user_profile = CustomerAccountProfile.objects.filter(userid=user).count()
		self.assertEqual(1,user_profile)

	def test_update_db(self):
		user = User.objects.get(email="oliver.queen@yahoo.com")
		user.first_name = "William"
		user.save()
		user = User.objects.get(email="oliver.queen@yahoo.com")
		self.assertEqual(user.first_name,"William")

	def test_user_genre(self):
		user = User.objects.get(email="oliver.queen@yahoo.com")
		user_profile = CustomerAccountProfile.objects.get(userid=user)
		user_genre = user_profile.userfavouritegenre
		self.assertEqual(user_genre, "['Adventures', 'Horror', 'Romance']")
		self.assertIsInstance(user_genre, str)
		self.assertIsInstance(eval(user_genre), list)

class BookTest(TestCase):
	def setUp(self):
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

	def tearDown(self):
		Book.objects.all().delete()

	def test_isbns_length(self):
		self.assertEqual(len(str(self.book.isbn_13)),13)
		self.assertEqual(len(str(self.book.isbn_10)),10)

	def test_book_date(self):
		self.assertTrue(isinstance(self.book.book_data, dict))
		self.assertEqual(len(self.book.book_data.keys()), 13)

class ReviewTest(TestCase):
	def create_book(self):
		ISBN_13 = 9876543212345
		ISBN_10 = 7685747586
		title = "A View from the Bridge"
		book_data = { "id": "vKJewgEACAAJ", "etag": "e8wZTpMgieo", "title": "A View from the Bridge",
		"authors": "Mohamed,Haja,Nijam", "publisher": "Longman", "publishedDate": "1999-02-11",
		"description": "Some random description for this book.", "ISBN_10": "7685747586",
		"ISBN_13": "9876543212345", "categories": [ "Digital Communications" ], "averageRating": 0.0,
		"ratingsCount": 0, "thumbnail": "http://books.google.com/books/content?id=vKJewgEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api" }
		return Book.objects.create(isbn_13=ISBN_13, isbn_10=ISBN_10, title=title, book_data=book_data)

	def create_user(self, u, e, p, f, l):
		return User.objects.create_user(username=u, email=e, password=p, first_name=f, last_name=l)

	def create_user_profile(self, u ,b, g, ug):
		return u.customeraccountprofile_set.create(birthDate=b, gender=g, userfavouritegenre=ug)

	def setUp(self):
		self.book = self.create_book()
		newuser = self.create_user("oliver.queen@yahoo.com", "oliver.queen@yahoo.com", "RanDomPasWord56", "Oliver", "Queen")
		newprofile = self.create_user_profile(newuser, "2019-03-22", "Male", "[Adventures, Horror, Romance]")
		user_review = "A review for this book!!!!"
		user_rating = 4
		created_date = dt.now()
		self.user_profile = newprofile
		self.new_review = Review.objects.create(bookID=self.book, customerID=newprofile, description=user_review, rating_value=user_rating, created_at=created_date)

	def test_reviewed_user(self):
		self.assertEqual(self.new_review.customerID, self.user_profile)

	def test_reviewed_book(self):
		self.assertEqual(self.new_review.bookID, self.book)

	def test_rating_value(self):
		self.assertLessEqual(self.new_review.rating_value, 5)
		self.assertTrue(self.checkifless(self.new_review.rating_value))#Same as above.

	def checkifless(self, rating_value):
		return rating_value<=5

	def test_review_date(self):
		self.assertLessEqual(self.new_review.created_at, dt.now())
		self.assertTrue(self.checkdate(self.new_review.created_at))#Same as above.

	def checkdate(self, created_at):
		return created_at<=dt.now()