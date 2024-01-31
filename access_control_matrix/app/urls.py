
from django.urls import path
from . import views
urlpatterns = [

#            Basics 
    path('',views.main_fun),


#           user

    path('logout_user',views.logout_user),
    path('add_user',views.add_user),
    path('login_user',views.login_user),
    path('emp_home',views.emp_home),
    path('user_view_files',views.user_view_files),
    path('user_decrypt_folder/<int:id>',views.user_decrypt_folder),
    path('user_encrypt_folder/<int:id>',views.user_encrypt_folder),



#           ADMIN 


    path('add_domain',views.add_domain),
    path('admin_home',views.admin_home),
    path('add_job_type',views.add_job_type),
    path('view_employees',views.view_employees),
    path('upload_file',views.upload_file),
    path('view_uploaded_files',views.view_uploaded_files),
    path('view_added_domains',views.view_added_domains),
    path('view_added_job_types',views.view_added_job_types),
    path('edit_domain/<domain>',views.edit_domain),
    path('edit_type/<position>',views.edit_type),
    path('admin_decrypt_folder',views.admin_decrypt_folder),
    path('encrypt_file',views.encrypt_single_file),
    path('add_access',views.add_access),
    path('access_details',views.edit_access),
    path('editing_access/<id>',views.editing_access),
    path('delete_domain/<domain>',views.delete_domain),
    path('delete_type/<position>',views.delete_type),

]
