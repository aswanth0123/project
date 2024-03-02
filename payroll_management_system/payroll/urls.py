
from django.urls import path
from . import views
urlpatterns = [


    path('',views.main_fun),
    path('login_user',views.login_user),
    path('logout_user',views.logout_user),
    path('admin_home',views.admin_home),
    path('add_user',views.add_user),
    path('add_job_type',views.add_job_type),
    path('view_added_job_types',views.view_added_job_types),
    path('mark_attendence',views.mark_attendence),
    path('attendance_details',views.attendance_details),
]