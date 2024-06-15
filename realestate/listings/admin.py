from django.contrib import admin
from .models import Location,PropertyType,Property

# Register your models here.
admin.site.register(Location)
admin.site.register(PropertyType)
admin.site.register(Property)
