from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from support.models import Issue, Ticket

# Register your models here.

class IssueAdmin(DjangoMpttAdmin):
    list_display = ['name','parent']
    search_fields = ['name','parent']
class TicketAdmin(DjangoMpttAdmin):
    list_display = ['title','parent']
    search_fields = ['title', 'parent']
admin.site.register(Issue, IssueAdmin)
admin.site.register(Ticket, TicketAdmin)

