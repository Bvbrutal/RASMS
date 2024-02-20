"""
URL configuration for RASMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.views.generic import TemplateView

from app import views

urlpatterns = [
    # path("admin/", admin.site.urls),
    # 主页
    path("", views.index),
    path("index/", views.index),

    # 404页面
    path('404/', TemplateView.as_view(template_name='page/404.html'), name='404'),

    #注册登录
    path("login/", views.login),
    path("register/", views.register),

    # 个人信息
    path("profile/", views.profile),

    # 事件记录
    path("select_event/", views.select_event),

    # 老年人信息管理
    path("add_old/", views.add_old),
    path("select_old/", views.select_old),
    path("modify_old/", views.modify_old),
    path("analyze_old/", views.analyze_old),

    # 工作人员信息管理
    path("add_worker/", views.add_worker),
    path("select_worker/", views.select_worker),
    path("modify_worker/", views.modify_worker),
    path("analyze_worker/", views.analyze_worker),


    # 义工信息管理
    path("add_volunteer/", views.add_volunteer),
    path("select_volunteer/", views.select_volunteer),
    path("modify_volunteer/", views.modify_volunteer),
    path("analyze_volunteer/", views.analyze_volunteer),
    path("volunteer_info/", views.volunteer_info),


    # 数据管理
    path("old_table/", views.old_table),
    path("worker_table/", views.worker_table),
    path("volunteer_table/", views.volunteer_table),
    path("event_table/", views.event_table),
    path("manager_table/", views.manager_table),
]
