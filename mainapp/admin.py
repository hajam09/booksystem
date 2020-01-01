from django.contrib import admin
from .models import CustomerAccountProfile, Book
# Register your models here.

admin.site.register(CustomerAccountProfile)
admin.site.register(Book)