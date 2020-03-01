# from django.test import TestCase, Client, RequestFactory, LiveServerTestCase
# from selenium.webdriver.common.keys import Keys
# import json, time
# # from mainapp.models import CustomerAccountProfile, Book, Review, Category
# from django.contrib.sessions.middleware import SessionMiddleware
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, WebDriverException
# from django.conf import settings
# from django.contrib.auth.models import User
# from selenium.webdriver.support.ui import Select
# # python manage.py test mainapp/tests

# class ErrorPageTest(LiveServerTestCase):
# 	def setUp(self):
# 		self.browser = webdriver.Chrome("chromedriver.exe")

# 	def tearDown(self):
# 		self.browser.close()

# 	def test_no_reason(self):
# 		self.browser.get(self.live_server_url)
# 		time.sleep(20)