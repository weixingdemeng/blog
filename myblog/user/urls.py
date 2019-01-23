from django.urls import path

from user import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('index/', views.index, name='index'),
    path('del_user/<int:id>/', views.del_user, name='del_user')

]