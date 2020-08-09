from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('login/', views.login, name='login'),  #登录页面
    path('register/', views.register, name='register'), #注册页面
    path('logout/',views.logout, name='logout'), #登出
    path('user_info/', views.user_info, name='user_info'), #用户信息
]