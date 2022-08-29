from django.contrib import admin
from .models import Clients,Departments,Managers,Sales, Tasks


admin.site.register(Clients)
admin.site.register(Departments)
admin.site.register(Managers)
admin.site.register(Sales)
admin.site.register(Tasks)