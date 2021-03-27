from django.contrib import admin
from .models import Task
# Register your models here


#Dang ki models trong database xuat hien trong trang admin
admin.site.register(Task)

