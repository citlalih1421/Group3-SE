from django.contrib import admin
from .models import UserType

# Register your models here.

class UserTypes(admin.ModelAdmin):
    list_display = ['name', 'description']
admin.site.register(UserType, UserTypes)