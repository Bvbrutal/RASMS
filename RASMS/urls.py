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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from app import account_views, user_views, elder_views
from app import manager_views
from app.management_views import old_management_views, worker_management_views, volunteer_management_views, table_views, \
    api_views, activity_views, announcement_views, account_management_views, regional_views, medication_views, \
    service_views

urlpatterns = [
                  path("admin/", admin.site.urls),

                  # 主页
                  path("", user_views.index, name="index_1"),
                  path("index/", user_views.index, name="index_2"),
                  path("older/index/", user_views.older_index, name="index_3"),
                  path("volunteer_information/", user_views.volunteer_information, name="volunteer_information"),
                  path("staff_information/", user_views.staff_information, name="staff_information"),

                  # 404页面
                  path('404/', TemplateView.as_view(template_name='account/404.html'), name='404'),

                  # 注册登录
                  path("login/", account_views.login, name="login"),
                  path("register/", account_views.register, name="register"),
                  path("logout/", account_views.logout, name='logout'),
                  path("modify_password/", account_views.modify_password, name="modify_password"),

                  # api
                  path("api/accont_api/", api_views.accont_api, name="accont_api"),
                  path("api/update_profile/", api_views.update_profile, name="update_profile"),
                  path("api/logging/", api_views.logging, name="logging"),
                  path('api/image_upload/', api_views.image_upload, name='image_upload'),
                  path('api/service_status/', api_views.service_status, name='service_status'),
                  path('api/services/data/', api_views.service_type_distribution, name='service_type_data'),
                  path('api/orders/data/', api_views.order_status_distribution, name='order_status_data'),
                  path('api/daily_orders_stats/', api_views.daily_orders_stats, name='daily_orders_stats'),
                  path('api/update_photo/', api_views.update_photo, name='update_photo'),
                  path('api/save_service/', api_views.save_service, name='save_service'),
                  path('api/accepted_service/', api_views.accepted_service, name='accepted_service'),

                  # 单项功能
                  path("management/select_event/", manager_views.select_event, name="select_event"),
                  path("management/profile/", manager_views.profile, name="profile_user"),
                  path("management/library/", manager_views.library, name="library"),
                  path("management/logging_record/", manager_views.logging_record, name="logging_record"),
                  path("management/event_add/", manager_views.event_add, name="event_add"),

                  # 老年人信息管理
                  path("management/list_old/", old_management_views.list_old, name="list_old"),
                  path("management/add_old/", old_management_views.add_old, name="add_old"),
                  path("management/select_old/", old_management_views.select_old, name="select_old"),
                  path("management/modify_old/", old_management_views.modify_old, name="modify_old"),
                  path("management/analyze_old/", old_management_views.analyze_old, name="analyze_old"),
                  path("management/old_info/", old_management_views.old_info, name="old_info"),
                  path("management/modify_old_basic/", old_management_views.modify_old_basic, name='modify_old_basic'),
                  path("management/modify_old_guardian/", old_management_views.modify_old_guardian,
                       name='modify_old_guardian'),

                  # 工作人员信息管理
                  path("management/add_worker/", worker_management_views.add_worker, name="add_worker"),
                  path("management/list_worker/", worker_management_views.list_worker, name="list_worker"),
                  path("management/modify_worker/", worker_management_views.modify_worker, name='modify_worker'),
                  path("management/analyze_worker/", worker_management_views.analyze_worker, name="analyze_worker"),
                  path("management/select_worker/", worker_management_views.select_worker, name='select_worker'),
                  path("management/worker_info/", worker_management_views.worker_info, name="worker_info"),
                  path("management/modify_worker_basic/", worker_management_views.modify_worker_basic,
                       name='modify_worker_basic'),

                  # 义工信息管理
                  path("management/add_volunteer/", volunteer_management_views.add_volunteer, name="add_volunteer"),
                  path("management/list_volunteer/", volunteer_management_views.list_volunteer, name="list_volunteer"),
                  path("management/select_volunteer/", volunteer_management_views.select_volunteer,
                       name="select_volunteer"),
                  path("management/modify_volunteer/", volunteer_management_views.modify_volunteer,
                       name="modify_volunteer"),
                  path("management/analyze_volunteer/", volunteer_management_views.analyze_volunteer,
                       name="analyze_volunteer"),
                  path("management/volunteer_info/", volunteer_management_views.volunteer_info, name="volunteer_info"),
                  path("management/modify_volunteer_basic/", volunteer_management_views.modify_volunteer_basic,
                       name="modify_volunteer_basic"),

                  # 数据管理
                  path("management/old_table/", table_views.old_table, name="old_table"),
                  path("management/worker_table/", table_views.worker_table, name="worker_table"),
                  path("management/volunteer_table/", table_views.volunteer_table, name="volunteer_table"),
                  path("management/event_table/", table_views.event_table, name="event_table"),
                  path("management/manager_table/", table_views.manager_table, name="management"),

                  # 用户界面
                  path("user/profile/", user_views.profile, name="profile_admin"),
                  path("user/modify_profile/", user_views.modify_profile, name="modify_profile"),
                  path("user/community_activity/", user_views.community_activity, name="community_activity"),

                  # 公告信息管理
                  path("management/announcement_list/", announcement_views.announcement_list,
                       name="announcement_list"),
                  path("management/announcement_info/", announcement_views.announcement_info,
                       name="announcement_info"),
                  path("management/announcement_add/", announcement_views.announcement_add,
                       name="announcement_add"),
                  path("management/announcement_modify/", announcement_views.announcement_modify,
                       name="announcement_modify"),
                  path("management/announcement_modify_basic/", announcement_views.announcement_modify_basic,
                       name="announcement_modify_basic"),

                  # 社区活动管理
                  path("management/activity_list/", activity_views.activity_list, name="activity_list"),
                  path("management/activity_info/", activity_views.activity_info, name="activity_info"),
                  path("management/activity_add/", activity_views.activity_add, name="activity_add"),
                  path("management/activity_modify/", activity_views.activity_modify, name="activity_modify"),
                  path("management/activity_modify_basic/", activity_views.activity_modify_basic,
                       name="activity_modify_basic"),

                  # 账号信息管理
                  path("management/account_analyze/", account_management_views.account_analyze, name="account_analyze"),
                  path("management/account_info/", account_management_views.account_info, name="account_info"),
                  path("management/account_add/", account_management_views.account_add, name="account_add"),
                  path("management/account_modify/", account_management_views.account_modify, name="account_modify"),

                  # 区域排班
                  path("management/regional_list/", regional_views.regional_list, name="regional_list"),
                  path("management/modify_regional/", regional_views.modify_regional, name="modify_regional"),
                  path("management/add_regional/", regional_views.add_regional, name="add_regional"),
                  path("management/modify_shift/", regional_views.modify_shift, name="modify_shift"),
                  path("management/shift_info/", regional_views.shift_info, name="shift_info"),

                  # 用药信息
                  path("management/medication_list/", medication_views.medication_list, name="medication_list"),
                  path("management/medication_add/", medication_views.medication_add, name="medication_add"),
                  path("management/medication_modify/", medication_views.medication_modify, name="medication_modify"),

                  # 服务订单
                  path("management/modify_service/", service_views.modify_service, name="modify_service"),
                  path("management/add_service/", service_views.add_service, name="add_service"),
                  path("management/analyze_service/", service_views.analyze_service, name="analyze_service"),
                  path("management/service_info/", service_views.service_info, name="service_info"),
                  path("management/serviceorder_info/", service_views.serviceorder_info, name="serviceorder_info"),
                  path("management/add_service_type/", service_views.add_service_type, name="add_service_type"),
                  path("management/modify_service_type/", service_views.modify_service_type,
                       name="modify_service_type"),
                  path("management/service_list/", service_views.service_list,
                       name="service_list"),
                  path("management/cancel_service/", service_views.cancel_service,
                       name="cancel_service"),
                  path("management/submit_feedback/", service_views.submit_feedback,
                       name="submit_feedback"),

                  # 老人页面
                  path("elder/modify_regional/", elder_views.modify_regional, name="modify_regional_elder"),
                  path("elder/activity_list/", elder_views.activity_list, name="activity_list_elder"),
                  path("elder/announcement_list/", elder_views.announcement_list,
                       name="announcement_list_elder"),
                  path("elder/medication_list/", elder_views.medication_list, name="medication_list_elder_elder"),
                  path("elder/modify_service/", elder_views.modify_service, name="modify_service_elder"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
