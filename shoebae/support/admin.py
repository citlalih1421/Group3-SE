from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

# Register your models here.

class IssueAdmin(DjangoMpttAdmin):
    list_display = ['name','parent']
    search_fields = ['name','parent']
class TicketAdmin(DjangoMpttAdmin):
    list_display = ['title','parent']
    search_fields = ['title', 'parent']
admin.site.register('support.Issue', IssueAdmin)
admin.site.register('support.Ticket', TicketAdmin)

