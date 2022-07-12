from django.contrib import admin
from django.urls import path, re_path

from blog.views import *

urlpatterns = [
    path('', BlogHome.as_view(), name="home"),
    path('addpage/', AddPage.as_view(), name='addpage'),
    path('logout/', logout_user, name='logout'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('cats/<slug:cat>', categories),
    path('post/<slug:post_slug>', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>', PostCategory.as_view(), name='category'),
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive),  # регулярное выражение
]
