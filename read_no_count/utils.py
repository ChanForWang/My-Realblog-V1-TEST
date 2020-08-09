import datetime
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.utils import timezone
from read_no_count.models import ReadNum, ReadDetail


#这是用户浏览文章实现阅读数增加的逻辑判断！！
#用在blog.views的def show上！
def read_no_count_once_read(request,obj):
    # 通过cookie来验证用户的存在，从而判断阅读数，而不是简单的刷新就增加
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" %(ct.model, obj.pk)
    if not request.COOKIES.get(key):
        # if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
        #     #存在记录， 那就提取出来
        #     # 返回一个<ReadNum: ReadNum object (1)>
        #     readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        # else:
        #     #不存在对应的记录, 那就创建相关记录
        #     readnum = ReadNum(content_type=ct, object_id=obj.pk)

        # 总阅读数+1
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.view += 1
        readnum.save()

        # 当天阅读数+1
        date = timezone.now().date()
        # if ReadDetail.objects.filter(content_type=ct, object_id=obj.pk, date=date).count():
        #     readDetail = ReadDetail.objects.get(content_type=ct, object_id=obj.pk, date=date)
        # else:
        #     readDetail = ReadDetail(content_type=ct, object_id=obj.pk, date=date)
        readDetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readDetail.view += 1
        readDetail.save()
    return key


#获取过去7天，"每天"  对应的浏览量
#用在blog.views的def index上， 将数据显示在主页
def get_seven_days_read_data(model):
    content_type = ContentType.objects.get_for_model(model)
    today = timezone.now().date()
    dates = []
    read_nums = []
    #记录前7天的阅读数
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        # 根据content_type:例如”blog|文章“ 和 对应“日期” 筛选出同一天和同一类型（blog|文章）的数据查询集
        #例： <QuerySet [<ReadDetail: ReadDetail object (2)>, <ReadDetail: ReadDetail object (3)>,等]
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(view_sum=Sum('view'))   #返回字典： 例：{'view_sum': 4}-----通过view把数据加起来,  view_sum这个参数可以自己随便命名

        read_nums.append(result['view_sum'] or 0)
    return dates, read_nums




#获取所有文章历史的累加浏览量！
#用来实现右侧导航栏的热门文章功能！！，应用在blog.views的hot!
def get_allTime_hot_data(model):
    content_type = ContentType.objects.get_for_model(model)   #返回model模型的类型， 例如model=Article则是 “<ContentType: blog | 文章>“
    read_nums = ReadNum.objects.filter(content_type=content_type).order_by('-view')[0:10]
    return read_nums         #返回10条根据-view 排序好的Query Set： [<ReadNum: ReadNum object (1)>, <ReadNum: ReadNum object (11)>。。等




# =================================================没用上================================

#返回 获取10篇最高浏览量属于 “今天” 的文章 read_details object
#此方法我没使用
def get_today_hot_data(model):
    content_type = ContentType.objects.get_for_model(model)
    today = timezone.now().date()   # 返回ie：datetime.date(2020, 8, 2)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-view')[0:10]
    return read_details  #返回 获取10篇最高浏览量属于 “今天” 的文章 read_details object  例如Query Set [<ReadDetail: ReadDetail object (1)>, <ReadDetail: ReadDetail object (11)>。。等


#返回 获取7篇最高浏览量属于 “昨天” 的文章 read_details object
def get_yesterday_hot_data(model):
    content_type = ContentType.objects.get_for_model(model)
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)   #if today = datetime.date(2020.8.2), then yesterday= datetime.date(2020.8.1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-view')[:7]
    return read_details

#返回 获取10篇最高浏览量属于 “过去一周内range” 的文章, 不包括今天  read_details object
# 这方法有瑕疵，就是最后在前段调用时，调用不到文章title， 所以“再敲一行代码第21集”有个更好的
def get_7_days_hot_data(model):
    content_type = ContentType.objects.get_for_model(model)
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    # 不包括今天lt, 包括第7天gte
    read_details = ReadDetail.objects \
                        .filter(content_type=content_type, date__lt=today, date__gte=date) \
                        .values('content_type', 'object_id') \
                        .annotate(view_sum=Sum('view')) \
                        .order_by('-view_sum')[:10]
    return read_details
#   查询Json，字典  <QuerySet [{'content_type': 10, 'object_id': 22, 'view_sum': 7}, {'content_type': 10, 'object_id': 8, 'view_sum': 1}, {'content_type': 10, 'object_id': 9, 'view_sum': 1}
# , {'content_type': 10, 'object_id': 15, 'view_sum': 1}, {'content_type': 10, 'object_id': 11, 'view_sum': 1}]>



