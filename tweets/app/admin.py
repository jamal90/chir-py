from django.contrib import admin
from .models import Tweet, Following

# Register your models here.
admin.site.register(Tweet)
admin.site.register(Following)