from django.contrib import admin
from read_no_count.models import ReadNum, ReadDetail
# Register your models here.


@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('id','view', 'content_object','object_id','content_type')
    list_display_links = ('id', 'view','content_object')


@admin.register(ReadDetail)
class ReadDetailAdmin(admin.ModelAdmin):
    list_display = ('id','date','view', 'content_object','object_id','content_type')
    list_display_links = ('id','date', 'view','content_object')