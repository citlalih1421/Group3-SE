from django.db import models
from django.contrib.auth import get_user_model
from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()

# Create your models here.
class Issue(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name','parent']

    def __str__(self):
        return self.name

class Ticket(MPTTModel):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ticket')
    title = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, related_name='parent_ticket')
    issue = models.CharField(
        max_length=100,
        default='other'
    )
    product_id = models.ForeignKey('store.Shoe', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(max_length=500)
    
    class MPTTMeta:
        order_insertion_by = ['title','parent']
        
    def __str__(self):
        return self.title