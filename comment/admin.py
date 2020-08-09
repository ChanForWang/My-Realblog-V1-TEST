from django.contrib import admin
from comment.models import Comment


# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','comment_text','comment_time','content_object','object_id','content_type','root','parent')
    list_display_links = ('id', 'user','content_object','object_id')