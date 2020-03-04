from django.contrib import admin
from .models import CustomerAccountProfile, Book, Review, Metrics
# Register your models here.

admin.site.register(CustomerAccountProfile)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Metrics)