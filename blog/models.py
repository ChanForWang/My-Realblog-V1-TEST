from django.db import models
from django.contrib.auth.models import User
from DjangoUeditor.models import UEditorField
from django.contrib.contenttypes.fields import GenericRelation
from read_no_count.models import ReadNumExpandMethod,ReadDetail

# Create your models here.

class Category(models.Model):
    name = models.CharField('博客分类', max_length=100)
    index = models.IntegerField(default=1, verbose_name='分类')
    excerpt = models.TextField('摘要', max_length=200, blank=True,null=True)
    img = models.ImageField(upload_to='category_img/%Y/%m/%d/', verbose_name='首页分类图片', blank=True, null=True)

    class Meta:
        #这是后台admin会显示的名字
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

#文章标签
class Tag(models.Model):
    name = models.CharField('文章标签', max_length=100)
    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

#推荐位
class Tui(models.Model):
    name = models.CharField('推荐位',max_length=100)

    class Meta:
        verbose_name = '推荐位'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

#文章
#继承了类ReadNumExpanMethod内的方法views,才可以在后台的 文章 内显示浏览数！
class Article(models.Model, ReadNumExpandMethod):
    title = models.CharField('标题', max_length=70)
    excerpt = models.TextField('摘要', max_length=200, blank=True)
    #使用外键关联分类表与分类是一对多关系，可以为blank
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类', blank=True)
    #使用外键关联标签表与标签是多对多关系
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)


    img = models.ImageField(upload_to='article_img/%Y/%m/%d/', verbose_name='文章图片   ',blank=True,null=True)
    # 存储比较短的字符串可以使用 CharField，但对于文章的正文来说可能会是一大段文本，因此使用 TextField 来存储大段文本。
    # body = models.TextField()     #通过以下富文本编辑器(百度的)来更好的添加文本
    content = UEditorField('内容', width=800, height=700,toolbars='full', imagePath='upimg/',filePath='upfile/',
                        upload_settings={'imageMaxSize': 1204000},
                        settings={}, command=None, blank=True)
    """
        留意里面的imagePath="upimg/", filePath="upfile/" 这两个是图片和文件上传的路径，
        我们上传文件，会自动上传到项目根目录media文件夹下对应的upimg和upfile目录里，
        这个目录名可以自行定义。有的人问，为什么会上传到media目录里去呢？那是因为之前我们在基础配置文章里，
        设置了上传文件目录media。
    """

    #外键，文章作者关联用户模型，系统自带的
    """
         文章作者，这里User是从django.contrib.auth.models导入的。
         专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
         这里我们通过 ForeignKey 把文章和 User 关联了起来。
         因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似。
    """
    auther = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')


    tui = models.ForeignKey(Tui, on_delete=models.DO_NOTHING, verbose_name='推荐位', blank=True, null=True)

    created_time = models.DateTimeField('发布时间', auto_now_add=True)  #创建时间，用来标识这条记录的创建时间，具有auto_now_add属性，创建记录时会自动填充当前时间到此字段
    modified_time = models.DateTimeField('修改时间', auto_now=True)     #修改时间，用来标识这条记录最后一次的修改时间，具有auto_now属性，当记录发生变化时填充当前时间到此字段

    # 通过GenericRelation来跟另外一个app内的模型model建立关系！
    read_details = GenericRelation(ReadDetail)



    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

