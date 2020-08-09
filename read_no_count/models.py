from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from django.utils import timezone

# Create your models here.

# 不是一个模型，因为没有继承（models.Model），就是单纯的一个 类！
#这个类用在blog.models的Article上
class ReadNumExpandMethod():
    # 此为对应某文章浏览数提取的方法,   并不是用户浏览文章而增加浏览数的逻辑判断，     self为Article模型
    def views(self):
        try:
            ct = ContentType.objects.get_for_model(self)   #返回  "blog|文章"  就是Article (as 在blog.models下定义了Article的verbose_name=文章)
            readNum = ReadNum.objects.get(content_type=ct, object_id=self.id)  #返回 该对应文章的readnum object
            return readNum.view   #返回对应文章的实际 浏览数
        except exceptions.ObjectDoesNotExist:
            return 0


#文章累计浏览数模型---通过设置另外的模型来关联  文章<-->浏览数， 更灵活的将此浏览数模型套用到其他需要用 “浏览数功能”的app中
class ReadNum(models.Model):
    view = models.PositiveIntegerField(verbose_name='浏览数', default=0)

    # 以下三句目的： 把浏览数view关联到某一种contentType类型的模型中，这也是ContentType的设计目的！
    # 比如我们用它把view浏览数关联到Artice模型中
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


    class Meta:
        verbose_name = '浏览'
        verbose_name_plural = verbose_name


#文章按日期浏览数模型
class ReadDetail(models.Model):
    # 相比较ReadNum, 这多加了个date, 目的： 为了了解 按日子为需求的浏览数！！
    date = models.DateField(verbose_name='DateTime',default=timezone.now)
    view = models.PositiveIntegerField(verbose_name='浏览数', default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = "每日不同文章浏览流量"
        verbose_name_plural = verbose_name


