from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'sfoj_system'
"""
urls.py Ground rule
1. url path는 rendering 함수의 이름을 활용한다. 
2. 기본적으로 모두 소문자로 통일한다.
"""
urlpatterns = [
    path('', views.index, name='index'), #config의 'sfoj_system/'이 추가된 후 이곳의 url이 추가됨
    path('login/', auth_views.LoginView.as_view(template_name='common:login'), name='login'),
    path('list/',views.list, name = 'list'),
    path('list/<int:board_index>/', views.detail, name = 'detail'),
    path('uploads/',views.uploads, name='uploads'),
    path('signup/',views.signup, name='signup'),
]