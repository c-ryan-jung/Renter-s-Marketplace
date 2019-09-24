from django.contrib import admin

# Register your models here.
from .models import User, Device, Transaction

admin.site.register(User)
admin.site.register(Device)
admin.site.register(Transaction)