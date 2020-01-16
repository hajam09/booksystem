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
from .models import CustomerAccountProfile, Book
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
				title = title.replace(",", "/cma/")
				try:
					authors = book['volumeInfo']['authors']
					authors = authors[0].replace(",", "|")
				except:
					authors = "None"
				
				try:
					publisher = book['volumeInfo']['publisher']
					publisher = publisher.replace(",", "|")
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
				#In the response ISBN10 and ISBN13 position may change
				ISBN_13 = None
				ISBN_10 = None
				if(book['volumeInfo']['industryIdentifiers'][0]['type'] == "ISBN_10"):
					ISBN_10 = book['volumeInfo']['industryIdentifiers'][0]['identifier']
				elif(book['volumeInfo']['industryIdentifiers'][0]['type'] == "ISBN_13"):
					ISBN_13 = book['volumeInfo']['industryIdentifiers'][0]['identifier']

				if(book['volumeInfo']['industryIdentifiers'][1]['type'] == "ISBN_10"):
					ISBN_10 = book['volumeInfo']['industryIdentifiers'][1]['identifier']
				elif(book['volumeInfo']['industryIdentifiers'][1]['type'] == "ISBN_13"):
					ISBN_13 = book['volumeInfo']['industryIdentifiers'][1]['identifier']

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
				except:
					description = "None"

				#Need to add leading zero's to ISBN 10 and 13.
				remaining_zero = "0"*(10-len(ISBN_10))
				ISBN_10 = remaining_zero+ISBN_10
				remaining_zero = ""
				remaining_zero = "0"*(13-len(ISBN_13))
				ISBN_13 = remaining_zero+ISBN_13
				
				#Add book to system if not exist
				checkBookExist = Book.objects.filter(isbn_13=ISBN_13, isbn_10=ISBN_10)
				if(len(checkBookExist)==0):
					print("New book")
					Book.objects.create(isbn_13=ISBN_13, isbn_10=ISBN_10, title=title)
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

@csrf_exempt
def user_shelf(request):

	user_pk = request.user.pk

	customer_account = User.objects.get(pk=user_pk)
	customer_details = CustomerAccountProfile.objects.get(userid=customer_account)

	#Need to check if the Book are already in favourites, reading now, to read and have read.
	favourite_Book = Book.objects.filter(favourites__id=customer_details.pk)
	reading_Book = Book.objects.filter(readingnow__id=customer_details.pk)
	to_read_Book = Book.objects.filter(toread__id=customer_details.pk)
	have_read_Book = Book.objects.filter(haveread__id=customer_details.pk)

	

	# Ajax requests when the buttons are clicked to remove the books from the list.
	#Need to change this to delete REQUEST
	if request.method == "PUT":
		put = QueryDict(request.body)
		functionality = put.get("functionality")
		objective = put.get("objective")
		isbn_13 = put.get("isbn_13")
		isbn_10 = put.get("isbn_10")
		print(isbn_10, isbn_13)

		#Need to add leading zero's to ISBN 10 and 13.
		remaining_zero = "0"*(10-len(isbn_10))
		isbn_10 = remaining_zero+isbn_10
		remaining_zero = ""
		remaining_zero = "0"*(13-len(isbn_13))
		isbn_13 = remaining_zero+isbn_13

		b1 = Book.objects.get(isbn_13=isbn_13, isbn_10=isbn_10)

		if(functionality=="remove-from-favourites"):
			if(b1 in favourite_Book):
				customer_details.favourites.remove(b1)
				return HttpResponse("remove_object_success")
			return HttpResponse("remove_object_failure")
		elif(functionality=="remove-from-reading-now"):
			if(b1 in reading_Book):
				customer_details.readingnow.remove(b1)
				return HttpResponse("remove_object_success")
			return HttpResponse("remove_object_failure")
		elif(functionality=="remove-from-toread"):
			if(b1 in to_read_Book):
				customer_details.toread.remove(b1)
				return HttpResponse("remove_object_success")
			return HttpResponse("remove_object_failure")
		elif(functionality=="remove-from-haveread"):
			if(b1 in have_read_Book):
				customer_details.haveread.remove(b1)
				return HttpResponse("remove_object_success")
			return HttpResponse("remove_object_failure")


	#Get categories and average_rating for favourite_books from csv
	favourite_book = []
	reading_now_book = []
	toread_book = []
	haveread_book = []
	for i in favourite_Book:
		line = get_row_from_csv(i.isbn_13, i.isbn_10)

		categories = replace_last_occurence(line[7], '|', ' & ', 1)
		categories = re.sub("[|]", ", ", categories)

		book_attributes = {"isbn_13": i.isbn_13, "isbn_10": i.isbn_10, "title": i.title, "categories": categories, "average_rating": line[8]}
		#favourite_Book[i] = book_attributes
		favourite_book.append(book_attributes)

	for j in reading_Book:
		line = get_row_from_csv(j.isbn_13, j.isbn_10)

		categories = replace_last_occurence(line[7], '|', ' & ', 1)
		categories = re.sub("[|]", ", ", categories)

		book_attributes = {"isbn_13": j.isbn_13, "isbn_10": j.isbn_10, "title": j.title, "categories": categories, "average_rating": line[8]}
		#reading_Book[i] = book_attributes
		reading_now_book.append(book_attributes)

	for k in to_read_Book:
		line = get_row_from_csv(k.isbn_13, k.isbn_10)

		categories = replace_last_occurence(line[7], '|', ' & ', 1)
		categories = re.sub("[|]", ", ", categories)

		book_attributes = {"isbn_13": k.isbn_13, "isbn_10": k.isbn_10, "title": k.title, "categories": categories, "average_rating": line[8]}
		#to_read_Book[i] = book_attributes
		toread_book.append(book_attributes)

	for l in have_read_Book:
		line = get_row_from_csv(l.isbn_13, l.isbn_10)

		categories = replace_last_occurence(line[7], '|', ' & ', 1)
		categories = re.sub("[|]", ", ", categories)

		book_attributes = {"isbn_13": l.isbn_13, "isbn_10": l.isbn_10, "title": l.title, "categories": categories, "average_rating": line[8]}
		#have_read_Book[i] = book_attributes
		haveread_book.append(book_attributes)

	context = {'favourite_Book':favourite_book, 'reading_Book':reading_now_book, 'to_read_Book':toread_book, 'have_read_Book':haveread_book}
	return render(request,'mainapp/usershelf.html', context)

def get_row_from_csv(isbn_13, isbn_10):
	csv_file = csv.reader(open('book_info.csv', "r"), delimiter=",")
	for row in csv_file:
		if(row[1]==isbn_13 and row[2]==isbn_10):
			return row
	return None


@csrf_exempt
def book_page(request, isbn_13, isbn_10):
	print(isbn_13, isbn_10)
	user_pk = request.user.pk

	if request.method == "PUT":
		if(not user_pk):
			return redirect('mainapp:login')

	#Need to add leading zero's to ISBN 10 and 13.
	remaining_zero = "0"*(10-len(isbn_10))
	isbn_10 = remaining_zero+isbn_10
	remaining_zero = ""
	remaining_zero = "0"*(13-len(isbn_13))
	isbn_13 = remaining_zero+isbn_13

	print(isbn_13, isbn_10)

	csv_file = csv.reader(open('book_info.csv', "r"), delimiter=",")
	line = None

	#Need threading to improve search efficiency
	for row in csv_file:
		if(row[1]==isbn_13 and row[2]==isbn_10):
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

	categories = replace_last_occurence(line[7], '|', ' & ', 1)
	categories = re.sub("[|]", ", ", categories)

	#Set of books to display for suggestions.
	item_based_recommendation = get_item_based_recommendation(csv_file)

	if user_pk:
		#If user is logged we can get more personal data
		customer_account = User.objects.get(pk=user_pk)
		customer_details = CustomerAccountProfile.objects.get(userid=customer_account)

		b1 = Book.objects.get(isbn_13=isbn_13, isbn_10=isbn_10)

		# Ajax requests when the buttons are clicked on the book.html
		if request.method == "PUT":
			put = QueryDict(request.body)
			functionality = put.get("functionality")
			isbn_13 = put.get("isbn_13")
			isbn_10 = put.get("isbn_10")

			if(functionality=="add-to-favourites"):
				favourite_Book = Book.objects.filter(favourites__id=customer_details.pk)
				if(b1 not in favourite_Book):
					customer_details.favourites.add(b1)
					return HttpResponse("new_object")
				else:
					customer_details.favourites.remove(b1)
					return HttpResponse("remove_object")
			elif(functionality=="reading-now"):
				reading_Book = Book.objects.filter(readingnow__id=customer_details.pk)
				if(b1 not in reading_Book):
					customer_details.readingnow.add(b1)
					return HttpResponse("new_object")
				else:
					customer_details.readingnow.remove(b1)
					return HttpResponse("remove_object")
			elif(functionality=="to-read"):
				toread_Book = Book.objects.filter(toread__id=customer_details.pk)
				if(b1 not in toread_Book):
					customer_details.toread.add(b1)
					return HttpResponse("new_object")
				else:
					customer_details.toread.remove(b1)
					return HttpResponse("remove_object")
			elif(functionality=="have-read"):
				have_read_Book = Book.objects.filter(haveread__id=customer_details.pk)
				if(b1 not in have_read_Book):
					customer_details.haveread.add(b1)
					return HttpResponse("new_object")
				else:
					customer_details.haveread.remove(b1)
					return HttpResponse("remove_object")

		#Need to check if the Book are already in favourites, reading now, to read and have read.
		in_favourite_Book = Book.objects.filter(favourites__id=customer_details.pk)
		in_reading_Book = Book.objects.filter(readingnow__id=customer_details.pk)
		in_to_read_Book = Book.objects.filter(toread__id=customer_details.pk)
		in_have_read_Book = Book.objects.filter(haveread__id=customer_details.pk)

		in_favourite_Book = True if b1 in in_favourite_Book else False
		in_reading_Book = True if b1 in in_reading_Book else False
		in_to_read_Book = True if b1 in in_to_read_Book else False
		in_have_read_Book = True if b1 in in_have_read_Book else False

		context = {'isbn_13':line[1], 'isbn_10': line[2],
					'title': line[3], 'authors': line[4],
					'publisher': line[5].replace("|", ","), 'publishedDate': line[6] ,
					'categories': categories, 'averageRating': line[8],
					'ratingsCount': line[9], 'thumbnail': line[10],
					'description': description_line, 'in_favourite_Book': in_favourite_Book,
					'in_reading_Book': in_reading_Book, 'in_to_read_Book': in_to_read_Book,
					'in_have_read_Book': in_have_read_Book, 'item_based_recommendation': item_based_recommendation}
		return render(request,'mainapp/book.html', context)

	context = {'isbn_13':line[1], 'isbn_10': line[2],
				'title': line[3], 'authors': line[4],
				'publisher': line[5], 'publishedDate': line[6] ,
				'categories': categories, 'averageRating': line[8],
				'ratingsCount': line[9], 'thumbnail': line[10],
				'description': description_line, 'in_favourite_Book': False,
				'in_reading_Book': False, 'in_to_read_Book': False,
				'in_have_read_Book': False, 'item_based_recommendation': item_based_recommendation}
	return render(request,'mainapp/book.html', context)

def get_item_based_recommendation(csv_file):
	csv_file = csv.reader(open('book_info.csv', "r"), delimiter=",")
	books_Objects = []
	counter = 0
	for line in csv_file:
		counter+=1
		if(len(books_Objects)==11):
			return books_Objects[1:]
		book_item = {'isbn_13':line[1], 'isbn_10': line[2], 'title': line[3].replace("/cma/", ","), 'thumbnail': line[10]}
		books_Objects.append(book_item)
		counter+=1
	return []

def replace_last_occurence(s, old, new, occurrence):
	li = s.rsplit(old, occurrence)
	return new.join(li)