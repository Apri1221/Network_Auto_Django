from django.contrib import admin

# Register your models here.

# device masuk ke dalam database
from .models import Device

admin.site.register(Device)

