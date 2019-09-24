from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import urllib.request
import urllib.parse
import json
from django.urls import reverse
from frontend.forms import *
# Create your views here.

def home(request):
	auth = request.COOKIES.get('auth')
	req = urllib.request.Request('http://exp-api:8000/home')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	devices = json.loads(resp_json)
	price_order = sorted(devices, key=lambda k: k['fields']['price'])
	date_order = sorted(devices, key=lambda k: k['fields']['updated_at'], reverse=True)
	if auth:
		return render(request, 'home.html', {'date_order': date_order, 'price_order': price_order, 'auth': auth})
	return render(request, 'home.html', {'date_order': date_order, 'price_order': price_order})

def details(request, id):
	auth = request.COOKIES.get('auth')
	if not auth:
		return HttpResponseRedirect(reverse("login") + "?next=" + reverse("details", args=[id]))

	data = {'auth': auth}
	json_data = urllib.parse.urlencode(data).encode('utf-8')
	req = urllib.request.Request('http://exp-api:8000/details/' + id, method="POST", data=json_data)
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')


	context = json.loads(resp_json)
	
	return render(request, 'details.html', {'context': context[0], 'auth': auth, 'recs': context[-1]})

def login(request):
	# If we received a GET request instead of a POST request
	if request.method == 'GET':
		# display the login form page
		next = request.GET.get('next') or reverse('home')
		return render(request, 'login.html')
	f = login_form(request.POST)

	# Check if the form instance is invalid
	if not f.is_valid():
		# Form was bad -- send them back to login page and show them an error
		return render(request, 'login.html', {'error': True})
	
	username = f.cleaned_data['username']
	password = f.cleaned_data['password']
	
	# Get next page
	next = f.cleaned_data.get('next') or reverse('home')
	data = {'username': username, 'password': password}
	json_data = urllib.parse.urlencode(data).encode('utf-8')
	req = urllib.request.Request('http://exp-api:8000/login', method='POST', data=json_data)
	resp = urllib.request.urlopen(req).read().decode('utf-8')
	# Check if the experience layer said they gave us incorrect information
	if resp == "Incorrect Password or Username":
	  # Couldn't log them in, send them back to login page with error
		return render(request, 'login.html', {'error': True})
	authenticator = resp
	response = HttpResponseRedirect(next)
	response.set_cookie("auth", authenticator)
	return response
	

def create_account(request):
	if request.method == 'GET':
		next = request.GET.get('next') or reverse('home')
		return render(request, 'create_account.html')
	if request.method == "POST":
		f = create_account_form(request.POST)
		if not f.is_valid():
			# Form was bad -- send them back to create account page and show them an error
			return render(request, 'create_account.html', {'error': True})
		
		username = f.cleaned_data['username']
		password = f.cleaned_data['password']
		
		next = f.cleaned_data.get('next') or reverse('home')
		data = {'username': username, 'password': password}
		json_data = urllib.parse.urlencode(data).encode('utf-8')
		req = urllib.request.Request('http://exp-api:8000/create_account', method='POST', data=json_data)
		resp = urllib.request.urlopen(req).read().decode('utf-8')
		# Check if the experience layer said they gave us incorrect information
		if resp == "Error - username already taken":
		  # Couldn't create account, send them back to create account page with error
			return render(request, 'create_account.html', {'error': True})
		authenticator = resp
		response = HttpResponseRedirect(next)
		response.set_cookie("auth", authenticator)
		return response
		

def logout(request): #finish
	auth = request.COOKIES.get('auth')
	data = {'auth': auth}
	json_data = urllib.parse.urlencode(data).encode('utf-8')
	req = urllib.request.Request('http://exp-api:8000/logout', method='POST', data=json_data)
	#resp = urllib.request.urlopen(req).read().decode('utf-8')
	resp = HttpResponseRedirect(reverse('login'))
	resp.delete_cookie('auth')
	return resp
	
def create_listing(request):
	auth = request.COOKIES.get('auth')
	if not auth:
		return HttpResponseRedirect(reverse("login") + "?next=" + reverse("create_listing"))

	if request.method == 'GET':
		return render(request, 'create_listing.html')
	
	f = create_listing_form(request.POST)
	if not f.is_valid():
		# Form was bad -- send them back to create account page and show them an error
		return render(request, 'create_listing.html', {'error': True})
	device_type = f.cleaned_data['device_type']
	manufacturer = f.cleaned_data['manufacturer']
	device_model = f.cleaned_data['device_model']
	rental_details = f.cleaned_data['rental_details']
	price = f.cleaned_data['price']
	is_available = True
	data = {'device_type': device_type, 'device_model': device_model, 'price': price, 'rental_details': rental_details, 'manufacturer': manufacturer, 'is_available': is_available, 'auth': auth}
	json_data = urllib.parse.urlencode(data).encode('utf-8')
	req = urllib.request.Request('http://exp-api:8000/create_listing', method='POST', data=json_data)
	resp = urllib.request.urlopen(req).read().decode('utf-8')
	# Check if the experience layer said they gave us incorrect information
	if resp == "Invalid Authenticator":
		# Send back to login
		return HttpResponseRedirect(reverse("login") + "?next=" + reverse("create_listing"))
	if resp == "Error - invalid or incomplete form data":
		# Couldn't create listing, send them back to create listing page with error
		return render(request, 'create_listing.html', {'error': True})
	response = HttpResponseRedirect(reverse('home'))
	response.set_cookie("auth", auth)
	return response

def search(request):
	auth = request.COOKIES.get('auth')
	# if not auth:
	# 	return HttpResponseRedirect(reverse("login") + "?next=" + reverse("search"))

	if request.method == 'GET':
		return render(request, "search.html", {'auth': auth})

	f = search_form(request.POST)
	if not f.is_valid():
		return render(request, "search.html", {'error': True})
	query = f.cleaned_data["query"]
	data = { "query": query }
	json_data = urllib.parse.urlencode(data).encode('utf-8')
	req = urllib.request.Request('http://exp-api:8000/search', method='POST', data=json_data)
	resp = urllib.request.urlopen(req).read().decode('utf-8')
	response = json.loads(resp)
	#return JsonResponse(response, safe=False)
	r = response['hits']['hits']
	results = []
	for result in r:
		results.append(result['_source'])
	return render(request, 'search.html', {'results': results, 'auth': auth})
		

