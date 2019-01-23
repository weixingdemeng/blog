from django.urls import path

from article import views

urlpatterns = [
    path('article/', views.article, name='article'),
    path('category/', views.category, name='category'),
    path('add_article/', views.add_article, name='add_article'),
    path('change_article/<int:id>/', views.change_article, name='change_article'),
    path('del_article/<int:id>/', views.del_article, name='del_article'),
    path('update_article/', views.update_article,name='update_article'),
]