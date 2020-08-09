from django.contrib import admin
from blog.models import Article, Category, Tag, Tui


# Register your models here.


# 在models.py中存在一个Article的类，把它注册到管理后台
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # 文章列表里 在admin内 显示想要显示的字段
    #views, 是调用了ReadNumExpandMethod类下的views方法
    list_display = ('id',  'title','auther','category', 'tui', 'views','created_time','modified_time' )
    # 满50条数据就自动分页
    list_per_page = 50
    # 后台数据列表排序方式
    ordering = ('-created_time',)
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('id', 'title')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'index')
    list_display_links = ('id', 'name')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

@admin.register(Tui)
class TuiAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


