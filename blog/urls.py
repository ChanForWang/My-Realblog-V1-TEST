from django.conf.urls import url
from django.urls import path
from blog import views

app_name = 'blog'
urlpatterns = [
    #根据设计需求， 总共有6个页面要实现
    path('', views.index, name='index'),#网站首页
    path('blog/', views.blog, name='blog'),
    path('diary/', views.diary, name= 'diary'),
    path('inspiration/',views.inspiration, name="inspiration"),
    path('list-<int:lid>.html', views.list, name='list'),  # 分类列表页
    path('show-<int:sid>.html', views.show, name='show'),  # 内容页
    path('tag/<tag>', views.tag, name='tag'),  # 标签列表页
    path('s/', views.search, name='search'),  # 搜索列表页
    path('about/', views.about, name='about'),  # 联系我们单页
]