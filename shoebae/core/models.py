from django.db import models
from django.contrib.auth.models import User
#was going to use django-mptt but it does not work for some reason, so manual implementation

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def add_child(self, child_name=str):
        return Category(name=child_name, parent=self)
    
    def get_parent(self):
        return self.parent
    
    def get_children(self):
        return Category.objects.filter(parent=self) if (self.id) else (Category.objects.none())
    
    def get_siblings(self):
        return Category.objects.filter(parent=self.parent).exclude(id=self.id) if (self.parent) else (Category.objects.none())
    #To-Do
    def get_depth(self):
        pass
    def pre_order(self):
        pass
    def in_order(self):
        pass
    def post_order(self):
        pass

class Brand(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='brand_logos/', blank=True)

#class Condition():
   # pass

class Shoe(models.Model):
    #seller foreign key
    name = models.CharField(max_length=150)
    details = models.TextField(max_length=500)
    category = models.TextChoices(Category, on_delete=models.CASCADE,choices=[(category.id, category.name) for category in Category.objects.all()])
    
    image = models.ImageField(upload_to='shoe_images/', null=True)
    size = models.DecimalField(max_digits=3, decimal_places=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    #To-Do
    ''' seller, brand, category, condition, color, *reviews'''
