from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

@admin.register(Medicine)
class FoundPostAdmin(admin.ModelAdmin):
    list_display=['id','name','image','expiration','quantity','category','description']
    list_filter = ['name','expiration','quantity','category','description']
    search_fields = ['name','expiration','quantity','category','description']
    
admin.site.register(CustomUser)
admin.site.register(Prescriptions)