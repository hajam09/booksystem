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
	path('user_shelf/', views.user_shelf, name='user_shelf'),
	path('book_page/<slug:isbn_13>/', views.book_page, name='book_page'),
	path('not_found/', views.not_found, name='not_found'),
]