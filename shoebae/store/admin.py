from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
#from .models import Condition, Brand, Category, Shoe

# Register your models here.
class CategoryAdmin(DjangoMpttAdmin):
    list_display = ['name','parent']
    search_fields = ['name','parent']
admin.site.register('store.Category', CategoryAdmin)
admin.site.register('store.Condition')
admin.site.register('store.Brand')
admin.site.register('store.Shoe')