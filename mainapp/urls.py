from django.urls import path, include
from mainapp import views

app_name = "mainapp"
urlpatterns = [
	path('', views.index, name='index'),
	path('signup/', views.signup, name='signup'),
	path('login/', views.login, name='login'),
	path('log_out/', views.log_out, name='log_out'),
	path('passwordforgotten/', views.passwordforgotten, name='passwordforgotten'),#NoteDone
	path('update_profile/', views.update_profile, name='update_profile'),
]