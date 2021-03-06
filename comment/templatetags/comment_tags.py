from django import template
from django.contrib.contenttypes.models import ContentType

from ..models import Comment
from ..forms import CommentForm

register = template.Library()

@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.id).count()

@register.simple_tag
def get_comment_from(obj):
    content_type = ContentType.objects.get_for_model(obj)
    data = {}
    data['content_type'] = content_type.model
    data['object_id'] = obj.id
    data['reply_comment_id'] = 0
    form = CommentForm(initial=data)
    return form

@register.simple_tag
#获取该文章的所有评论,最新的最先显示
def get_comment_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.id, parent=None).order_by('-comment_time')
    return comments