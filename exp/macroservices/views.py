from django.shortcuts import render
import urllib.request
import urllib.parse
import json
from django.http import JsonResponse, HttpResponse
from kafka import KafkaProducer
from elasticsearch import Elasticsearch


# Create your views here.
def home(request):
	req = urllib.request.Request('http://models-api:8000/api/all_devices')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	return JsonResponse(resp, safe=False)

def details(request, id):
	req = urllib.request.Request('http://models-api:8000/api/getRecs/' + id)
	recs = urllib.request.urlopen(req).read().decode('utf-8')
	recs = recs.split(" ")

	recs_data = []
	for rec in recs:
		if rec == "None":
			break
		req = urllib.request.Request('http://models-api:8000/api/device/' + rec)
		resp_json = urllib.request.urlopen(req).read().decode('utf-8')
		resp = json.loads(resp_json)
		recs_data.append(resp)


	auth = request.POST['auth']
	req = urllib.request.Request('http://models-api:8000/api/userFromAuth?auth=' + auth)
	user_id = urllib.request.urlopen(req).read().decode('utf-8')
	
	req = urllib.request.Request('http://models-api:8000/api/device/' + id)
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	resp.append(recs_data)

	data = {'user_id': user_id, 'item_id': id}
	producer = KafkaProducer(bootstrap_servers='kafka:9092')
	producer.send('access-log-topic', json.dumps(data).encode('utf-8'))

	return JsonResponse(resp, safe=False)

def create_account(request):
	if(request.method == 'POST'):
                username = request.POST['username']
                password = request.POST['password']
                data = {'username':username, 'password': password}
                json_data = urllib.parse.urlencode(data).encode('utf-8')
                req = urllib.request.Request('http://models-api:8000/api/user/create', method='POST', data=json_data)
                resp = urllib.request.urlopen(req).read().decode('utf-8')
                return HttpResponse(resp)
                if(resp != "Error - username already taken"):
                        #create the user in the database and then log them in
                        return login(request)
                return HttpResponse(resp)


def login(request):
	if(request.method == 'POST'):
		username = request.POST['username']
		password = request.POST['password']
		data = {'username':username, 'password': password}
		
		json_data = urllib.parse.urlencode(data).encode('utf-8')
		req = urllib.request.Request("http://models-api:8000/create/authentication", data=json_data, method='POST')
	   

		resp = urllib.request.urlopen(req).read().decode('utf-8')
		return HttpResponse(resp)

def logout(request):
	if(request.method == 'POST'):
		authorization = request.POST['auth']
		data = {'auth': authorization}
		json_data = urllib.parse.urlencode(data).encode('utf-8')
		req = urllib.request.Request(
			"http://models-api:8000/api/logout", data=json_data, method='POST')
		resp_json = urllib.request.urlopen(req).read().decode('utf-8')
		return HttpResponse(resp_json)

def search(request):
	if(request.method == 'POST'):
		query = request.POST["query"]
		es = Elasticsearch(['es'])
		
		result = es.search(index='listing_index', body={'query': {'query_string': {'query': query}}, 'size': 10})
		return JsonResponse(result, safe=False)
		



def create_listing(request):
	
	if(request.method == 'POST'):
		auth = request.POST['auth']
		device_type = request.POST['device_type']
		manufacturer = request.POST['manufacturer']
		device_model = request.POST['device_model']
		rental_details = request.POST['rental_details']
		price = request.POST['price']
		is_available = True
		data = {'device_type': device_type, 'device_model': device_model, 'price': price, 'rental_details': rental_details, 'manufacturer': manufacturer, 'is_available': is_available, 'auth': auth}
		json_data = urllib.parse.urlencode(data).encode('utf-8')
		
		req = urllib.request.Request('http://models-api:8000/api/device/create', method='POST', data=json_data)
		resp = urllib.request.urlopen(req).read().decode('utf-8')
		
		#the django models/database layer gives each item a unique id. it also uses the authenticator to figure out who the user is, and then ties that owner to each object. we can these fields for elastic search, but to be able to do that, we have to get infrormation back from the models layer. 
		#we've edited the response from the models layer to include this information
		#the models now responds with a string that has the information in the form "id author" (separated by a space)
		#the data dictionary should have a field for id. we can add that by using the response from the database. 
		
		listFormOfResp = resp.split(" ")
		data['id'] = int(listFormOfResp[0])
		# data["author"] = listFormOfResp[1]
		#adding this listing to the kafka queue
		producer = KafkaProducer(bootstrap_servers='kafka:9092')
		producer.send('new-listings-topic', json.dumps(data).encode('utf-8'))
		
		
		return HttpResponse(resp)
	
