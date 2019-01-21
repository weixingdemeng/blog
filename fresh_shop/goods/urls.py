from django.urls import path, re_path

from fresh_shop import urls
from goods import views

urlpatterns = [
    # 首页
    path('index/', views.index, name='index'),
    # 详情
    path('detail/<int:id>/', views.detail, name='detail'),
    path('list/', views.list, name='list'),

]