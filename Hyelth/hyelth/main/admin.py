from django.contrib import admin
from .models import Medicine, MedicineDetail
admin.site.register(MedicineDetail)

@admin.register(Medicine)
class FoundPostAdmin(admin.ModelAdmin):
    list_display=['id','name','image','expiration','quantity','category','description']
    list_filter = ['name','expiration','quantity','category','description']
    search_fields = ['name','expiration','quantity','category','description']