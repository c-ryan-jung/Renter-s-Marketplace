from django.db import models
#import os
#import hmac
#from django.conf import settings

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Device(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    device_type = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=50)
    device_model = models.CharField(max_length=50)
    price = models.FloatField()
    rental_details = models.CharField(max_length=400)
    is_available = models.BooleanField(default=True)
    updated_at = models.DateTimeField('Created Time',
                                      auto_now=True, null=True)

    def __str__(self):
        return self.device_model

class Transaction(models.Model):
    item = models.ForeignKey(Device, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    details = models.CharField(max_length=400)
    transaction_time = models.DateTimeField('Time of Transaction Initiation',
                                      auto_now=True, null=True)

    
class Authenticator(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    authenticator = models.CharField(primary_key=True, max_length=100)
    #hmac.new(
        #key = settings.SECRET_KEY.encode('utf-8'),
        #msg = os.random(32),
        #digestmod = 'sha256',
    #).hexdigest()
    date_created = models.DateField(auto_now_add=True)


class Recommendation(models.Model):
    item_id = models.CharField(max_length=50)
    recommended_items = models.CharField(max_length=200)


