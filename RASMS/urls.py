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

from app import account, user_views
from app import manager_views

urlpatterns = [
    # path("admin/", admin.site.urls),
    # 主页
    path("", manager_views.index),
    path("index/", user_views.index),
    path("manager/index/", manager_views.index),

    # 404页面
    path('404/', TemplateView.as_view(template_name='page/404.html'), name='404'),

    # 注册登录
    path("login/", account.login),
    path("register/", account.register),
    path("logout/", account.logout),
    path("modify_password/", account.modify_password),

    # 事件记录
    path("management/select_event/", manager_views.select_event),

    # 老年人信息管理
    path("management/add_old/", manager_views.add_old),
    path("management/select_old/", manager_views.select_old),
    path("management/modify_old/", manager_views.modify_old),
    path("management/analyze_old/", manager_views.analyze_old),

    # 工作人员信息管理
    path("management/add_worker/", manager_views.add_worker),
    path("management/select_worker/", manager_views.select_worker),
    path("management/modify_worker/", manager_views.modify_worker),
    path("management/analyze_worker/", manager_views.analyze_worker),

    # 义工信息管理
    path("management/add_volunteer/", manager_views.add_volunteer),
    path("management/select_volunteer/", manager_views.select_volunteer),
    path("management/modify_volunteer/", manager_views.modify_volunteer),
    path("management/analyze_volunteer/", manager_views.analyze_volunteer),
    path("management/volunteer_info/", manager_views.volunteer_info),

    # 数据管理
    path("management/old_table/", manager_views.old_table),
    path("management/worker_table/", manager_views.worker_table),
    path("management/volunteer_table/", manager_views.volunteer_table),
    path("management/event_table/", manager_views.event_table),
    path("management/manager_table/", manager_views.manager_table),

    path("manager_views/profile/", manager_views.profile),

    # 用户界面
    path("profile/", user_views.profile),
    path("user/modify_profile/", user_views.modify_profile),
    path("user/community_activity/", user_views.community_activity),

    # api
    path("user/accont_api/", user_views.accont_api),
    path("user/update_profile", user_views.update_profile),

]
