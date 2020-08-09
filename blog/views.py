from django.shortcuts import render
from .models import Article, Category, Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from read_no_count.utils import read_no_count_once_read, get_seven_days_read_data,get_allTime_hot_data

# Create your views here.

# 右侧aside栏
# def global_variable(request):
#     # 置顶推荐
#     tui = Article.objects.filter(tui__id=1).order_by("-id")[0:3] #拿推荐位id为1的3篇文章， 所以后台要设置 置顶推荐 的tui的id = 1
#     #热门十篇文章
#     hot = Article.objects.all().order_by('views')[0:10]  # 通过浏览数进行排序， 提取出热门文章---右侧热门10篇文章排行
#     # 文章分类
#     allcategory = Category.objects.all()
#     # 文章标签
#     tags = Tag.objects.all()
#     return locals()


# 首页
def index(request):
    allcategory = Category.objects.filter(index=1).order_by("-id")[0:3]
    allarticle = Article.objects.all().order_by('-id')[0:3]

    dates, read_nums = get_seven_days_read_data(Article)  #用来统计过去七天每天的流量

    return render(request, 'index.html', locals())



def blog(request):
    Allarticle = Article.objects.exclude(category__name__icontains='日记').order_by('-id')  # ---最新文章：中间10篇文章
    tui = Article.objects.filter(tui__id=1).order_by("-id")[0:3]  # 拿推荐位id为1的3篇文章， 所以后台要设置 置顶推荐 的tui的id = 1
    # hot = Article.objects.all().order_by('-views()')[0:10]  # 通过浏览数进行排序， 提取出热门文章---右侧热门10篇文章排行
    allcategory = Category.objects.all()# 文章分类
    tags = Tag.objects.all()# 文章标签

    hot = get_allTime_hot_data(Article)  #返回一堆QuerySet【<ReadNum: ReadNum object (1)>, <ReadNum: ReadNum object (2)>。。。等， 就是后台--浏览--模型内的所有！1】


    page =request.GET.get("page")  #在网址中获取page的参数值
    paginator = Paginator(Allarticle,10)   #10篇翻一页
    try:
        allarticle = paginator.page(page)   # 获取当前页码的记录
    except PageNotAnInteger:
        allarticle = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        allarticle = paginator.page(paginator.num_pages) # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    return render(request, 'blog.html', locals())



def list(request, lid):
    List = Article.objects.filter(category_id=lid).order_by('-id') # 获取通过URL传进来的lid，然后筛选出对应分类id的文章
    category_name = Category.objects.get(id=lid) # 获取当前文章的分类名
    tui = Article.objects.filter(tui__id=1).order_by("-id")[0:3]  # 拿推荐位id为1的3篇文章， 所以后台要设置 置顶推荐 的tui的id = 1
    # hot = Article.objects.all().order_by('-views()')[0:10]  # 通过浏览数进行排序， 提取出热门文章---右侧热门10篇文章排行
    allcategory = Category.objects.all()  # 文章分类
    tags = Tag.objects.all()  # 文章标签


    hot = get_allTime_hot_data(Article)



    page = request.GET.get('page')  # 在网址URL中获取当前页面数
    paginator = Paginator(List, 10)  # 对查询到的数据对象list进行分页，设置超过5条数据就分页
    try:
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    return render(request, 'list.html',locals())



def show(request, sid):
    tui = Article.objects.filter(tui__id=1).order_by("-id")[0:3]  # 拿推荐位id为1的3篇文章， 所以后台要设置 置顶推荐 的tui的id = 1
    allcategory = Category.objects.all()  # 文章分类
    tags = Tag.objects.all()  # 文章标签
    interestTopic = Article.objects.all().order_by('?')[0:5]  # 内容下面的您可能感兴趣的文章，随机推荐
    # 右侧热门文章的逻辑(历史累计热门)
    hot = get_allTime_hot_data(Article)


    show = Article.objects.get(id=sid)  # 查询指定ID的文章-----找到对应内容的文章
    previous_blog = Article.objects.filter(created_time__gt=show.created_time,
                                           category=show.category.id).first()  # create time大于本文的定义为上一篇
    netx_blog = Article.objects.filter(created_time__lt=show.created_time,
                                       category=show.category.id).last()  # 小于本文的定义为下一篇。  category=show.category.id，则是指定查询的文章为  当前分类下  的文章。

    #阅读量方法函数的引入和使用
    read_coockie_key = read_no_count_once_read(request,show)  #这返回的是一个key， 计算文章的总阅读量

    response = render(request, 'show.html',locals())
    response.set_cookie(read_coockie_key,'true')
    return response



def tag(request, tag):
    List = Article.objects.filter(tags__name=tag).order_by('-id') # 通过文章标签进行查询文章--提取对应tag的文章
    tag_name = Tag.objects.get(name=tag) # 返回当前搜索的标签的标签名
    tui = Article.objects.filter(tui__id=1).order_by("-id")[0:3]  # 拿推荐位id为1的3篇文章， 所以后台要设置 置顶推荐 的tui的id = 1
    # hot = Article.objects.all().order_by('-views()')[0:10]  # 通过浏览数进行排序， 提取出热门文章---右侧热门10篇文章排行
    allcategory = Category.objects.all()  # 文章分类
    tags = Tag.objects.all()  # 文章标签

    # 右侧热门文章的逻辑(历史累计热门)
    hot = get_allTime_hot_data(Article)


    page = request.GET.get('page')
    # tags = Tag.objects.all()
    paginator = Paginator(List, 10)
    try:
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    return render(request, 'tag.html', locals())



def search(request):
    tui = Article.objects.filter(tui__id=1).order_by("-id")[0:3]  # 拿推荐位id为1的3篇文章， 所以后台要设置 置顶推荐 的tui的id = 1
    # hot = Article.objects.all().order_by('-views()')[0:10]  # 通过浏览数进行排序， 提取出热门文章---右侧热门10篇文章排行
    allcategory = Category.objects.all()  # 文章分类
    tags = Tag.objects.all()  # 文章标签

    # 右侧热门文章的逻辑(历史累计热门)
    hot = get_allTime_hot_data(Article)


    ss = request.GET.get('search')  # 获取搜索的关键词
    List = Article.objects.filter(title__icontains=ss)  # 获取到搜索关键词通过标题进行匹配---找到对应的搜索文章

    page = request.GET.get('page')
    # tags = Tag.objects.all()
    paginator = Paginator(List, 10)
    try:
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    return render(request, 'search.html',locals())



def diary(request):
    tui = Article.objects.filter(tui__id=1).order_by("-id")[0:3]  # 拿推荐位id为1的3篇文章， 所以后台要设置 置顶推荐 的tui的id = 1
    # hot = Article.objects.all().order_by("-views()")[0:10]  # 通过浏览数进行排序， 提取出热门文章---右侧热门10篇文章排行
    allcategory = Category.objects.all()  # 文章分类
    tags = Tag.objects.all()  # 文章标签

    # 右侧热门文章的逻辑(历史累计热门)
    hot = get_allTime_hot_data(Article)


    List = Article.objects.filter(category__name='日记').order_by('-id')

    page = request.GET.get('page')
    paginator = Paginator(List, 10)
    try:
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    return render(request, 'diary.html',locals())



def about(request):
    return render(request, 'about.html',locals())

