from django.conf.urls import url
from django.urls import path
from comment import views

app_name = 'comment'
urlpatterns = [
    path('upload_comment/', views.upload_comment, name="upload_comment"),
]