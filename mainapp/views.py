from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse, Http404, QueryDict
from django.template import RequestContext, loader
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login as auth_login
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomerAccountProfile, Books
import string, random, csv, re
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import PasswordChangeForm
# Create your views here.

@csrf_exempt
def index(request):
	if request.method == 'POST':
		book_result = eval(request.POST['book'].replace("true", "True").replace("false", "False"))
		#Creating a model for each book if not exist and add to csv
		for book in book_result:
			if(len(book['volumeInfo']['industryIdentifiers'])==2):
				uid = book['id']
				etag = book['etag']
				title = book['volumeInfo']['title']
				authors = book['volumeInfo']['authors']
				authors.sort()
				authors = "/".join(authors)
				try:
					publisher = book['volumeInfo']['publisher']
				except:
					publisher = "None"
				try:
					publishedDate = book['volumeInfo']['publishedDate']
				except:
					publishedDate = "None"
				try:
					description = book['volumeInfo']['description']
				except:
					description = "None"
				ISBN_13 = book['volumeInfo']['industryIdentifiers'][0]['identifier']
				ISBN_10 = book['volumeInfo']['industryIdentifiers'][1]['identifier']
				try:
					categories = book['volumeInfo']['categories']
					categories = "".join(categories)
					categories = re.sub("[,&]", "|", categories)
				except:
					categories = "None"
				
				try:
					averageRating = book['volumeInfo']['averageRating']
				except:
					averageRating = 0.0
				averageRating = round(averageRating,1)
				try:
					ratingsCount = book['volumeInfo']['ratingsCount']
				except:
					ratingsCount = 0

				try:
					thumbnail = book['volumeInfo']['imageLinks']['thumbnail']
				except:
					thumbnail = "None"

				try:
					description = book['volumeInfo']['description']
				except Exception as e:
					description = "None"
				
				#Add book to system if not exist
				checkBookExist = Books.objects.filter(isbn_13=ISBN_13, isbn_10=ISBN_10)
				if(len(checkBookExist)==0):
					print("New book")
					Books.objects.create(isbn_13=ISBN_13, isbn_10=ISBN_10, title=title)
					with open('book_info.csv', 'a') as csv_file:
						towrite = "\n"+uid+","+ISBN_13+","+ISBN_10+","+title+","+authors+","+publisher+","+publishedDate+","+categories+","+str(float(averageRating))+","+str(ratingsCount)+","+thumbnail
						csv_file.write(towrite)

					text_file = open("book_descriptions.txt", "a")
					item_to_write = ISBN_13 + "|" + ISBN_10 + "|" + description + "\n"
					text_file.write(item_to_write)
					text_file.close()
	return render(request,'mainapp/frontpage.html',{})

@csrf_exempt
def signup(request):
	if request.method == 'POST':
		fullname = request.POST['fullname']
		email = request.POST['email']
		password = request.POST['password']
		birthDate = request.POST['birthDate']
		gender = request.POST['gender']
		listOfUserGenre = str(request.POST['listofgenre'].split(","))

		#Check if the account with same email id exist before creating a new one
		checkAccountExist = User.objects.filter(email=email)
		if(len(checkAccountExist)==0):
			fullname = fullname.split(" ")
			fname = " ".join(fullname[:len(fullname)-1])
			sname = "".join(fullname[len(fullname)-1])

			#Creating an account for the user
			user = User.objects.create_user(username=email, email=email, password=password, first_name=fname, last_name=sname)

			#Creating the profile for the user
			user.customeraccountprofile_set.create(birthDate=birthDate, gender=gender, userfavouritegenre=listOfUserGenre)
			return render(request,'mainapp/login.html', {})
		return HttpResponse("An account already exists for this email address, please try again!")
	return render(request,'mainapp/signup.html', {})

def login(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']

		user = authenticate(username=email, password=password)
		if user:
			auth_login(request, user)
		else:
			return HttpResponse("Sorry! Username and Password didn't match, Please try again!")
	return render(request,'mainapp/login.html', {})

@csrf_exempt
def log_out(request):
    """Log out - note that the session will be deleted"""
    request.session.flush()
    logout(request)
    return redirect('mainapp:index')

def passwordforgotten(request):
	#Not DONE
	if request.method == 'POST':
		try:
			if(request.POST["email"]):
				print("EmailSent")
				
				print(confirmationid)
				return HttpResponse("Email has been sent to {}".format(request.POST["email"]))
		except Exception as e:
			if(request.POST["idvalue"]):
				print("CODE entered")
				print("A")
				if(confirmationid==request.POST["idvalue"]):
					return HttpResponse("codevalid")
				return HttpResponse("codeinvalid")
	return render(request,'mainapp/forgotpassword.html',{})

@csrf_exempt
def update_profile(request):
	user_pk = request.user.pk
	if(not user_pk):
		return redirect('mainapp:login')

	customer_account = User.objects.get(pk=user_pk)
	customer_details = CustomerAccountProfile.objects.get(userid=customer_account)
	fullname =  str(customer_account.first_name +" "+ customer_account.last_name)
	print("user_pk value is {} and customer_details is {}".format(user_pk, customer_details.pk))
	context = {"fullname": fullname,
				"email": customer_account.email,
				"userfavouritegenre": customer_details.userfavouritegenre}

	if request.method == "PUT":
		put = QueryDict(request.body)

		fullname = put.get('fullname').split(" ")
		fname = " ".join(fullname[:len(fullname)-1])
		sname = "".join(fullname[len(fullname)-1])
		email = put.get('email')
		listofgenre = str(put.get('listofgenre').split(","))

		User.objects.filter(pk=int(user_pk)).update(username=email, email=email, first_name=fname, last_name=sname)
		u = User.objects.get(pk=int(user_pk))

		if(put.get('password')):
			#User changed the password
			u.set_password(put.get('password'))
			u.save()

		#Updating the user profile
		CustomerAccountProfile.objects.filter(pk=int(customer_details.pk)).update(userfavouritegenre=listofgenre)
		return HttpResponse("Your details are updated!")
	print("AA")
	return render(request,'mainapp/profilepage.html', context)

def user_shelf(request):
	context = {}
	return render(request,'mainapp/usershelf.html', context)

def book_page(request, isbn_13, isbn_10):
	csv_file = csv.reader(open('book_info.csv', "r"), delimiter=",")
	line = None
	#Need threading to improve search efficiency
	for row in csv_file:
		if((row[1]==isbn_13 or row[1]=="0"+isbn_13)  and (row[2]==isbn_10 or row[2]=="0"+isbn_10)):
			line = row
			break

	#Need to read file book_description file to get the description
	file = open("book_descriptions.txt", "r").readlines()
	description_line = None
	for row in file:
		c_line = row.split("|")
		if((c_line[0]==isbn_13 or c_line[0]=="0"+isbn_13) and (c_line[1]==isbn_10 or c_line[1]=="0"+isbn_10)):
			description_line = c_line[2].strip()
			break

	context = {'isbn_13':line[1], 'isbn_10': line[2],
				'title': line[3], 'authors': line[4],
				'publisher': line[5], 'publishedDate': line[6] ,
				'categories': line[7], 'averageRating': line[8],
				'ratingsCount': line[9], 'thumbnail': line[10],
				'description': description_line}
	return render(request,'mainapp/book.html', context)