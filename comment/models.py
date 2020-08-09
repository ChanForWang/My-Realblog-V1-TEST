from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
class Comment(models.Model):
    # 通过以下3句来进行模型对模型的数据关联！
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(User, related_name='comments', on_delete=models.DO_NOTHING,verbose_name='用户')
    comment_text = models.TextField(verbose_name='评论内容')
    comment_time = models.DateTimeField(verbose_name='评论时间',auto_now_add=True)

    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.DO_NOTHING)
    parent = models.ForeignKey('self', related_name='parent_comment', null=True, on_delete=models.DO_NOTHING)
    reply_to = models.ForeignKey(User, related_name='replies', null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.comment_text

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

