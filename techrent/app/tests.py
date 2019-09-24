from django.test import TestCase, Client, RequestFactory
from .models import User, Device, Transaction
from .views import *
from django.urls import reverse
# Create your tests here.


class NewTestCase(TestCase):
    fixtures = ['db.json']
    def setUp_User(self):
        self.client = Client()
        self.data = {'username': "TEST", 'password': 'password'}

    def setUp_Device(self):
        self.client = Client()
        self.data = {'owner' : 1, 'device_type' : "TESTTYPE", 'manufacturer' : "TESTMAN", 'device_model' : "TESTMODEL", "price" : 10, "rental_details" : "test", 'is_available' : True}

    def setUp_Transaction(self):
        self.client = Client()
        self.data = {'item': 1, 'buyer': 1, 'seller': 2, 'details': "test"}

    def test_user_read(self):
        self.setUp_User()
        response = self.client.get('/api/user/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['fields']['username'], "ryan")

    def test_user_create(self):
        self.setUp_User()
        response = self.client.post('/api/user/create', self.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'success')
        
    # def test_device_create(self):
    #     self.setUp_Device()
    #     response = self.client.post('/api/device/create', self.data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json()[0]['fields']['owner'], 1)
    #     self.assertEqual(response.json()[0]['fields']['device_type'], "TESTTYPE")
    #     self.assertEqual(response.json()[0]['fields']['manufacturer'], "TESTMAN")
    #     self.assertEqual(response.json()[0]['fields']['device_model'], "TESTMODEL")
    #     self.assertEqual(response.json()[0]['fields']['price'], "10")
    #     self.assertEqual(response.json()[0]['fields']['rental_details'], "test")
    #     self.assertTrue(response.json()[0]['fields']['is_available'])

    def test_transaction_create(self):
        self.setUp_Transaction()
        response = self.client.post('/api/transaction/create', self.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['fields']['details'],"test")

    def test_get_and_update_device(self):
        self.setUp_Device()
        device = self.client.get('/api/device/1')
        self.assertEqual(1, device.json()[0]['fields']['owner'])
        updatedDevice = self.client.post('/api/device/1', {'owner' : 2})
        self.assertEqual(2, updatedDevice.json()[0]['fields']['owner'])

    def test_get_and_update_user(self):
        self.setUp_User()
        user = self.client.get('/api/user/1')
        self.assertEqual("ryan", user.json()[0]['fields']['username'])
        updatedUser = self.client.post('/api/user/1', {'username' : 'Tested'})
        self.assertEqual("Tested", updatedUser.json()[0]['fields']['username'])

    def test_get_and_update_transaction(self):
        self.setUp_Transaction()
        response = self.client.get('/api/transaction/1')
        self.assertEqual(response.json()[0]['fields']['details'], "testing")
        update = self.client.post('/api/transaction/1', {'details': "tested"})
        self.assertEqual("tested", update.json()[0]['fields']['details'])

    def test_delete_user(self):
        self.setUp_User()
        response = self.client.post('/api/user/1/delete')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'user 1 deleted')
        try:
            response = self.client.get('/api/user/1')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(1, 1)

    def test_delete_device(self):
        self.setUp_Device()
        response = self.client.post('/api/device/1/delete')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'device 1 deleted')
        try:
            response = self.client.get('/api/device/1')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(1, 1)

    def test_delete_transaction(self):
        self.setUp_User()
        response = self.client.post('/api/transaction/1/delete')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'transaction 1 deleted')
        try:
            response = self.client.get('/api/transaction/1')
            self.assertEqual(1, 0)
        except:
            self.assertEqual(1, 1)

    def test_all_devices(self):
        self.setUp_Device()
        response = self.client.get('/api/all_devices')
        self.assertEqual(len(response.json()), 7)
        self.assertEqual(response.json()[0]['model'], "app.device")
