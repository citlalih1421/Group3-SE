from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import Condition, Brand, Category, Shoe

# Register your models here.
class CategoryAdmin(DjangoMpttAdmin):
    list_display = ['category_name','parent']
    search_fields = ['name','parent']
admin.site.register(Category, CategoryAdmin)
admin.site.register(Condition)
admin.site.register(Brand)
admin.site.register(Shoe)